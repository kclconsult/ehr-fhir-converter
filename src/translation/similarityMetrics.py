from __future__ import division
from builtins import object
from past.utils import old_div
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer

from translation.translationConstants import TranslationConstants
from utils.utilities import Utilities

class SimilarityMetrics(object):

    @staticmethod
    def textMatch(ehr, fhir, highestCompositeResult=True, textSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD):

        if (SimilarityMetrics.compositeStringSimilarity(ehr, fhir, SimilarityMetrics.textSimilarity, [], highestCompositeResult) * TranslationConstants.TEXT_SIMILARITY_WEIGHTING >= textSimilarityThreshold):

            return True;

        else:
            return False;

    @staticmethod
    def morphologicalMatch(ehr, fhir, highestCompositeResult=True, morphologicalSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD):

        if (SimilarityMetrics.compositeStringSimilarity(ehr, fhir, SimilarityMetrics.morphologicalSimilarity, [], highestCompositeResult) * TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING >= morphologicalSimilarityThreshold):
            return True;

        else:
            return False;

    # Similarity Metric A
    @staticmethod
    def textSimilarity(ehrAttribute, fhirAttribute, stem=False):

        if stem:
            stemmer = PorterStemmer()
            ehrAttribute = stemmer.stem(ehrAttribute);
            fhirAttribute = stemmer.stem(fhirAttribute);

        textSimilarity = fuzz.ratio(ehrAttribute.lower(), fhirAttribute.lower()) / 100.0;

        return textSimilarity;

    wordsToTypes = {};
    synsetToDefinitionTerms = {};

    # Similarity Metric B
    @staticmethod
    def morphologicalSimilarity(ehrAttribute, fhirAttribute, lemmaSimilarityThreshold=TranslationConstants.MORPHOLOGICAL_SIMILARITY_THRESHOLD):

        if SimilarityMetrics.textMatch(ehrAttribute, fhirAttribute): return 0;

        highestSimilarity = 0;

        for lemma in Utilities.lemmas(ehrAttribute):

            if SimilarityMetrics.textSimilarity(lemma, fhirAttribute, True) > highestSimilarity and SimilarityMetrics.textMatch(lemma, fhirAttribute, True, lemmaSimilarityThreshold):
                highestSimilarity = SimilarityMetrics.textSimilarity(lemma, fhirAttribute, True);

        return highestSimilarity;

    # Similarity Metric C
    @staticmethod
    def semanticSimilarity(ehrAttribute, fhirAttribute, useDefinition=False, alsoUseMorphologicalSimilarity=False, morphologicalSimilarityThreshold=TranslationConstants.MORPHOLOGICAL_SIMILARITY_THRESHOLD, compositeSynonyms=False, highestResult=True ):

        # If these attributes would be associated via a text match instead, then don't also reevaluate their similarity via the text similarity below.
        if SimilarityMetrics.textMatch(ehrAttribute, fhirAttribute, False): return 0;

        highestSimilarity = 0;

        # wordnet requires word separation by underscore, whereas EHR XML responses (for TPP at least) use camelCase (this won't be an issue if used with composite string similarity, where only one word is used at a time).
        for set in wordnet.synsets(Utilities.capitalToSeparation(ehrAttribute)):

            synonyms = set.lemma_names();

            if useDefinition:

                setType = set.pos();
                associatedSynonyms = [];

                if ( set not in SimilarityMetrics.synsetToDefinitionTerms ):

                    # We also include words from the definition of this word, that are of the same grammatical type (e.g. noun or verb), as potential synonyms.
                    for word in set.definition().split(" "):

                        if ( len(word) <= 3 or word in associatedSynonyms or "." in word ): continue;

                        if ( word not in SimilarityMetrics.wordsToTypes ):

                            wordSynset = wordnet.synsets(word);

                            if not len(wordSynset): continue;

                            # Find most popular interpretation of this word, so can find right grammatical form.
                            chosenSynset = wordSynset[0];
                            highestLemmaPopularity = 0;

                            for set in wordSynset:

                                for lemma in set.lemmas():

                                    if lemma.count() > highestLemmaPopularity:
                                        highestLemmaPopularity = lemma.count();
                                        chosenSynset = set;

                            SimilarityMetrics.wordsToTypes[word] = chosenSynset.pos();

                        if ( SimilarityMetrics.wordsToTypes[word] == setType ):

                            associatedSynonyms.append(word);

                    SimilarityMetrics.synsetToDefinitionTerms[set] = associatedSynonyms;

                synonyms = synonyms + SimilarityMetrics.synsetToDefinitionTerms[set];

            for synonym in synonyms:

                # Do we want the highest value across all components of the synonym, or just the synonym directy.
                if ( compositeSynonyms ):

                    textSimilarity = SimilarityMetrics.compositeStringSimilarity(Utilities.separationToCapital(synonym), fhirAttribute, SimilarityMetrics.textSimilarity, [], highestResult);

                else:

                    textSimilarity = SimilarityMetrics.textSimilarity(synonym, fhirAttribute);


                # Synonyms may also be grammatical variants as opposed to just text matches.
                if ( alsoUseMorphologicalSimilarity ):

                    if ( compositeSynonyms ):

                        morphologicalSimilarity = SimilarityMetrics.compositeStringSimilarity(Utilities.separationToCapital(synonym), fhirAttribute, SimilarityMetrics.morphologicalSimilarity, [morphologicalSimilarityThreshold], highestResult);

                    else:

                        morphologicalSimilarity = SimilarityMetrics.morphologicalSimilarity(synoynm, fhirAttribute);

                else:
                    morphologicalSimilarity = 0;

                # Get similarity between synonym for ehrAttribute and fhirAttribute (not synonyms that are the ehr attribute itself). If this is over a given threshold, AND it is greater than previously marked highest values, update highest similarity.
                if not SimilarityMetrics.textSimilarity(synonym, ehrAttribute) == 1.0 and max(textSimilarity, morphologicalSimilarity) > highestSimilarity:

                    highestSimilarity = max(textSimilarity, morphologicalSimilarity);

        return highestSimilarity;

    # Similarity Metric D - Sentence progression? e.g. "Done at" and "Location"

    ######

    # With highest result False, there needs to be a stricter connection between the class or fields. Probably best for child fields to have stricter match rules.
    @staticmethod
    def compositeStringSimilarity(ehrClassField, fhirClassField, comparisonMethod, comparisonMethodArgs=[], highestResult=True):

        # If ehrClass string is composite, compare each word with the FHIR target using all of the metrics, and then use chosen combination method to produce a value, e.g. for each word, add these values, and then divide by number of words to get an average match across all words or return highest.
        highestSimilarity = 0;
        highestSimilarityWord = "";

        totalSimilarity = 0;

        ehrWords = Utilities.listFromCapitals(ehrClassField);
        fhirWords = Utilities.listFromCapitals(fhirClassField);

        for ehrWord in ehrWords:

            highestSimilarityForEHRWord = 0;

            for fhirWord in fhirWords:

                similarity = comparisonMethod(ehrWord, fhirWord, *comparisonMethodArgs);

                if ( similarity > highestSimilarity ):

                    highestSimilarity = similarity;
                    highestSimilarityWord = ehrWord;

                if ( similarity > highestSimilarityForEHRWord ): highestSimilarityForEHRWord = similarity;

            totalSimilarity += highestSimilarityForEHRWord;

        if ( highestResult and len(highestSimilarityWord) > TranslationConstants.LENGTH_TO_IGNORE_IN_COMPOSITE_HIGHEST ):

            return highestSimilarity;

        else:

            return old_div(totalSimilarity, len(ehrWords)); #max(float(len(ehrWords)), float(len(fhirWords)));

    ######
