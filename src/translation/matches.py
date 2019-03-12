import sys

from translation.similarityMetrics import SimilarityMetrics
from translation.translationConstants import TranslationConstants
from utils.utilities import Utilities

class Matches(object):

    @staticmethod
    def match(ehrClassField, fhirClassField,
    textSimilarity=SimilarityMetrics.textSimilarity, textSimilarityArgs=[], textSimilarityWeighting=TranslationConstants.TEXT_SIMILARITY_WEIGHTING,
    morphologicalSimilarity=SimilarityMetrics.morphologicalSimilarity, morphologicalSimilarityArgs=[], morphologicalSimilarityWeighting=TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING,
    semanticSimilarity=SimilarityMetrics.semanticSimilarity, semanticSimilarityArgs=[], semanticSimilarityWeighting=TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING,
    textSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD,
    semanticSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD,
    morphologicalSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD,
    overallSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD,
    highestCompositeResult=TranslationConstants.COMPOSITE_STRING_SIMILARITY_HIGHEST_COMPOSITE_RESULT,
    firstPastThreshold=TranslationConstants.METRICS_FIRST_PAST_THRESHOLD,
    highestStrength=TranslationConstants.METRICS_HIGHEST_STRENGTH,
    combined=TranslationConstants.METRICS_COMBINED,
    average=TranslationConstants.METRICS_AVERAGE):

        textSimilarityValue = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, textSimilarity, textSimilarityArgs, highestCompositeResult) * textSimilarityWeighting;

        if ( firstPastThreshold and textSimilarityValue >= textSimilarityThreshold  ):
            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, textSimilarity, textSimilarityArgs, highestCompositeResult);

        #

        morphologicalSimilarityValue = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, morphologicalSimilarity, morphologicalSimilarityArgs, highestCompositeResult) * morphologicalSimilarityWeighting;

        if (firstPastThreshold and morphologicalSimilarityValue >= morphologicalSimilarityThreshold):
            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, morphologicalSimilarity, morphologicalSimilarityArgs, highestCompositeResult);

        #

        semanticSimilarityValue = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, semanticSimilarity, semanticSimilarityArgs, highestCompositeResult) * semanticSimilarityWeighting;

        if ( firstPastThreshold and semanticSimilarityValue >= semanticSimilarityThreshold):

            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, semanticSimilarity, semanticSimilarityArgs, highestCompositeResult);

        #

        strength = max(textSimilarityValue, max(semanticSimilarityValue, morphologicalSimilarityValue));

        if ( highestStrength and strength >= overallSimilarityThreshold):
            return strength;

        strength = textSimilarityValue + semanticSimilarityValue + morphologicalSimilarityValue;

        if ( combined and strength >= overallSimilarityThreshold ):
            return strength;

        strength = (textSimilarityValue + semanticSimilarityValue + morphologicalSimilarityValue) / 3.0;

        if ( average and strength >= overallSimilarityThreshold ):
            return strength;

        return 0;

    # Simple abstraction over match (note also reordered params for convenience in expressing thresholds): see if there is a match at all, based on thresholds.
    @staticmethod
    def matches(ehr, fhir,
        textSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD,
        morphologicalSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD,
        semanticSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD,
        similarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD,
        textSimilarity = SimilarityMetrics.textSimilarity, textSimilarityArgs=[], textSimilarityWeighting = TranslationConstants.TEXT_SIMILARITY_WEIGHTING, \
        morphologicalSimilarity = SimilarityMetrics.morphologicalSimilarity, morphologicalSimilarityArgs=[], morphologicalSimilarityWeighting = TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, \
        semanticSimilarity = SimilarityMetrics.semanticSimilarity, semanticSimilarityArgs=[], semanticSimilarityWeighting = TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, \
        highestCompositeResult=TranslationConstants.COMPOSITE_STRING_SIMILARITY_HIGHEST_COMPOSITE_RESULT,
        firstPastThreshold=TranslationConstants.METRICS_FIRST_PAST_THRESHOLD,
        highestStrength=TranslationConstants.METRICS_HIGHEST_STRENGTH,
        combined=TranslationConstants.METRICS_COMBINED,
        average=TranslationConstants.METRICS_AVERAGE
    ):

        if ( Matches.match(ehr, fhir, \
            textSimilarity, textSimilarityArgs, textSimilarityWeighting, \
            morphologicalSimilarity, morphologicalSimilarityArgs, morphologicalSimilarityWeighting, \
            semanticSimilarity, semanticSimilarityArgs, semanticSimilarityWeighting, \
            textSimilarityThreshold, \
            semanticSimilarityThreshold, \
            morphologicalSimilarityThreshold, \
            similarityThreshold, \
            highestCompositeResult, \
            firstPastThreshold, \
            highestStrength, \
            combined, \
            average \
        ) > 0 ):

            return True;

        else:

            return False;

    # Abstraction for convenience. Uses no thresholds to derive raw match strength, and assumes use of highestStrength.
    @staticmethod
    def matchStrength(
        ehrChild, fhirChild,
        textSimilarity = SimilarityMetrics.textSimilarity, textSimilarityArgs=[], textSimilarityWeighting = TranslationConstants.TEXT_SIMILARITY_WEIGHTING, \
        morphologicalSimilarity = SimilarityMetrics.morphologicalSimilarity, morphologicalSimilarityArgs=[], morphologicalSimilarityWeighting = TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, \
        semanticSimilarity = SimilarityMetrics.semanticSimilarity, semanticSimilarityArgs=[], semanticSimilarityWeighting = TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, \
        highestCompositeResult=TranslationConstants.COMPOSITE_STRING_SIMILARITY_HIGHEST_COMPOSITE_RESULT,
        firstPastThreshold=False,
        highestStrength=True,
        combined=TranslationConstants.METRICS_COMBINED,
        average=TranslationConstants.METRICS_AVERAGE
    ):

        if ( firstPastThreshold == False and not highestStrength and not combined and not average ):

            raise ValueError("If firstPastThreshold is False, one of highestStrength, combined or average must be true in order to derive a match strength. highestStrength suggested.");

        return Matches.match(
            ehrChild, fhirChild,
            textSimilarity, textSimilarityArgs, textSimilarityWeighting,
            morphologicalSimilarity, morphologicalSimilarityArgs, morphologicalSimilarityWeighting,
            semanticSimilarity, semanticSimilarityArgs, semanticSimilarityWeighting,
            0, 0, 0, 0,
            highestCompositeResult,
            firstPastThreshold,
            highestStrength,
            combined,
            average
        );

    @staticmethod
    def fuzzyMatch(ehrClass, fhirClass):

        # To create fuzzy effect: for now, we introduce morphological matches, as well as text matches, when calling semantic similarity, and also use a lower morphological similarity threshold when doing so.
        return Matches.match(ehrClass, fhirClass, SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [False, True, 0.75, True]);

    @staticmethod
    def fuzzyMatchStrength(ehrClass, fhirClass):

        return Matches.matchStrength(ehrClass, fhirClass, SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [False, True, 0.75, True]);
