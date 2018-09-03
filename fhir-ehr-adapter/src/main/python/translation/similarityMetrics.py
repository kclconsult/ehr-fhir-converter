from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer

from translation.translationConstants import TranslationConstants
from utils.utilities import Utilities

class SimilarityMetrics(object):
    
    @staticmethod
    def textMatch(ehr, fhir, highestCompositeResult=True, textSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD):
    
        if (SimilarityMetrics.compositeStringSimilarity(ehr, fhir, SimilarityMetrics.textSimilarity, highestCompositeResult) * TranslationConstants.TEXT_SIMILARITY_WEIGHTING >= textSimilarityThreshold):
            return True;
        
        else:
            return False;
    
    @staticmethod
    def morphologicalMatch(ehr, fhir, highestCompositeResult=True, morphologicalSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD):
    
        if (SimilarityMetrics.compositeStringSimilarity(ehr, fhir, SimilarityMetrics.morphologicalSimilarity, highestCompositeResult) * TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING >= morphologicalSimilarityThreshold):
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
        
        return fuzz.ratio(ehrAttribute.lower(), fhirAttribute.lower()) / 100.0;
    
    wordsToTypes = {};
    synsetToDefinitionTerms = {};
    
    # Similarity Metric B
    @staticmethod
    def semanticSimilarity(ehrAttribute, fhirAttribute, useDefinition=True, alsoUseMorphologicalSimilarity=True):
        
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
                                    
                                    #print str(lemma) + " " + str(lemma.count());
                                    if lemma.count() > highestLemmaPopularity: 
                                        highestLemmaPopularity = lemma.count();
                                        chosenSynset = set;
                            
                            SimilarityMetrics.wordsToTypes[word] = chosenSynset.pos();
                            
                        if ( SimilarityMetrics.wordsToTypes[word] == setType ):
                            
                            associatedSynonyms.append(word);
                    
                    SimilarityMetrics.synsetToDefinitionTerms[set] = associatedSynonyms;
                
                synonyms = synonyms + SimilarityMetrics.synsetToDefinitionTerms[set];
                
            for synonym in synonyms:
                
                textSimilarity = SimilarityMetrics.compositeStringSimilarity(Utilities.separationToCapital(synonym), fhirAttribute, SimilarityMetrics.textSimilarity, False);
                
                # Synonyms may also be grammatical variants as opposed to just text matches.
                if ( alsoUseMorphologicalSimilarity ):
                    morphologicalSimilarity = SimilarityMetrics.compositeStringSimilarity(Utilities.separationToCapital(synonym), fhirAttribute, SimilarityMetrics.morphologicalSimilarity, False);
                
                else:
                    morphologicalSimilarity = 0;
                    
                # Get similarity between synonym for ehrAttribute and fhirAttribute (not synonyms that are the ehr attribute itself). If this is over a given threshold, AND it is greater than previously marked highest values, update highest similarity.
                if not SimilarityMetrics.textSimilarity(synonym, ehrAttribute) == 1.0 and max(textSimilarity, morphologicalSimilarity) > highestSimilarity:
                    
                    textMatch = SimilarityMetrics.textMatch(Utilities.separationToCapital(synonym), fhirAttribute);
                    
                    if ( alsoUseMorphologicalSimilarity ):
                        morphologicalMatch = SimilarityMetrics.morphologicalMatch(Utilities.separationToCapital(synonym), fhirAttribute);
                        
                    else:
                        morphologicalMatch = 0;
                        
                    # Only update highest similarity if it is significant.
                    if ( textMatch > morphologicalMatch ):
                        highestSimilarity = textSimilarity;
                    
                    else:
                        highestSimilarity = morphologicalSimilarity;
                        
        return highestSimilarity;    
    
     # Similarity Metric C
    @staticmethod
    def morphologicalSimilarity(ehrAttribute, fhirAttribute):
        
        if SimilarityMetrics.textMatch(ehrAttribute, fhirAttribute): return 0;
        
        highestSimilarity = 0;
        
        for lemma in Utilities.lemmas(ehrAttribute):
            
            if SimilarityMetrics.textSimilarity(lemma, fhirAttribute, True) > highestSimilarity and SimilarityMetrics.textMatch(lemma, fhirAttribute, True, TranslationConstants.MORPHOLOGICAL_SIMILARITY_THRESHOLD):
                highestSimilarity = SimilarityMetrics.textSimilarity(lemma, fhirAttribute, True);
        
        return highestSimilarity;
    
    # Similarity Metric D - Sentence progression? e.g. "Done at" and "Location"
    
    ######
           
    # With highest result False, there needs to be a stricter connection between the class or fields. Probably best for child fields to have stricter match rules.
    @staticmethod
    def compositeStringSimilarity(ehrClassField, fhirClassField, comparisonMethod, highestResult=True):
        
        # If ehrClass string is composite, compare each word with the FHIR target using all of the metrics, and 
        # then use chosen combination method to produce a value.
        # For each word, add these values, and then divide by number of words to get an average match across all words (or max?).
        highestSimilarity = 0;
        totalSimilarity = 0;
        
        ehrWords = Utilities.listFromCapitals(ehrClassField);
        fhirWords = Utilities.listFromCapitals(fhirClassField);
        
        for ehrWord in ehrWords:
            
            highestSimilarityForEHRWord = 0;
            
            for fhirWord in fhirWords:
                
                similarity = comparisonMethod(ehrWord, fhirWord);
                
                if( similarity > highestSimilarity ): highestSimilarity = similarity;
                    
                if ( similarity > highestSimilarityForEHRWord ): highestSimilarityForEHRWord = similarity;
            
            totalSimilarity += highestSimilarityForEHRWord;
            
        if ( highestResult ):
            return highestSimilarity;
        
        else:
            return totalSimilarity / len(ehrWords); #max(float(len(ehrWords)), float(len(fhirWords)));
    
    ######
    
   
        
    