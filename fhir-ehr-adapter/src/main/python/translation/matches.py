from translation.similarityMetrics import SimilarityMetrics
from translation.translationConstants import TranslationConstants
from utils.utilities import Utilities

class Matches(object):
    
    @staticmethod
    def match(ehrClassField, fhirClassField, textSimilarityWeighting=TranslationConstants.TEXT_SIMILARITY_WEIGHTING, semanticSimilarityWeighting=TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, morphologicalSimilarityWeighting=TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, morphologicalSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, overallSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True, firstPastThreshold=True, highestStrength=False, combined=False, average=False):
        
        textSimilarity = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, SimilarityMetrics.textSimilarity, highestCompositeResult) * textSimilarityWeighting;
        
        # This should change if highest result is not being used, perhaps to number of words that match?
        
        if ( firstPastThreshold and textSimilarity >= textSimilarityThreshold  ):
            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, SimilarityMetrics.textSimilarity, highestCompositeResult);
        
        # 
        
        semanticSimilarity = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, SimilarityMetrics.semanticSimilarity, highestCompositeResult) * semanticSimilarityWeighting;
        
        if ( firstPastThreshold and semanticSimilarity >= semanticSimilarityThreshold):
            
            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, SimilarityMetrics.semanticSimilarity, highestCompositeResult);
        
        #
        
        morphologicalSimilarity = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, SimilarityMetrics.morphologicalSimilarity, highestCompositeResult) * morphologicalSimilarityWeighting;
        
        if (firstPastThreshold and morphologicalSimilarity >= morphologicalSimilarityThreshold):
            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, SimilarityMetrics.morphologicalSimilarity, highestCompositeResult);
        
        strength = max(textSimilarity, max(semanticSimilarity, morphologicalSimilarity));
        
        if ( highestStrength and strength >= overallSimilarityThreshold):
            return strength;
        
        strength = textSimilarity + semanticSimilarity + morphologicalSimilarity;
        
        if ( combined and strength >= overallSimilarityThreshold ):
            return strength;
        
        strength = (textSimilarity + semanticSimilarity + morphologicalSimilarity) / 3.0;
        
        if ( average and strength >= overallSimilarityThreshold ):
            return strength; 
        
        return 0;
        
    # See if there is a match at all, based on thresholds.
    @staticmethod
    def matches(ehr, fhir, textSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, morphologicalSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, similarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True, firstPastThreshold=True, highestStrength=False, combined=False, average=False):
        
        if ( Matches.match(ehr, fhir, TranslationConstants.TEXT_SIMILARITY_WEIGHTING,  TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING,  TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold, semanticSimilarityThreshold, morphologicalSimilarityThreshold, similarityThreshold, highestCompositeResult, firstPastThreshold, highestStrength, combined, average) > 0 ):
            return True;
        
        else:
            return False;
        
    