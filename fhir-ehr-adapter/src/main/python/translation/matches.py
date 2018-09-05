from translation.similarityMetrics import SimilarityMetrics
from translation.translationConstants import TranslationConstants
from utils.utilities import Utilities

class Matches(object):
    
    @staticmethod
    def match(ehrClassField, fhirClassField, textSimilarity=SimilarityMetrics.textSimilarity, textSimilarityArgs=[], textSimilarityWeighting=TranslationConstants.TEXT_SIMILARITY_WEIGHTING, semanticSimilarity=SimilarityMetrics.semanticSimilarity, semanticSimilarityArgs=[], semanticSimilarityWeighting=TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, morphologicalSimilarity=SimilarityMetrics.morphologicalSimilarity, morphologicalSimilarityArgs=[], morphologicalSimilarityWeighting=TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, morphologicalSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, overallSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True, firstPastThreshold=True, highestStrength=False, combined=False, average=False):
        
        textSimilarityValue = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, textSimilarity, textSimilarityArgs, highestCompositeResult) * textSimilarityWeighting;
        
        # This should change if highest result is not being used, perhaps to number of words that match?
        
        if ( firstPastThreshold and textSimilarityValue >= textSimilarityThreshold  ):
            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, textSimilarity, textSimilarityArgs, highestCompositeResult);
        
        # 
        
        semanticSimilarityValue = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, semanticSimilarity, semanticSimilarityArgs, highestCompositeResult) * semanticSimilarityWeighting;
        
        if ( firstPastThreshold and semanticSimilarityValue >= semanticSimilarityThreshold):
            
            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, semanticSimilarity, semanticSimilarityArgs, highestCompositeResult);
        
        #
        
        morphologicalSimilarityValue = SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, morphologicalSimilarity, morphologicalSimilarityArgs, highestCompositeResult) * morphologicalSimilarityWeighting;
        
        if (firstPastThreshold and morphologicalSimilarityValue >= morphologicalSimilarityThreshold):
            return SimilarityMetrics.compositeStringSimilarity(ehrClassField, fhirClassField, morphologicalSimilarity, morphologicalSimilarityArgs, highestCompositeResult);
        
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
    
    @staticmethod
    def fuzzyMatch(ehrClass, fhirClass):
        
        # To create fuzzy effect: for now, we introduce morphological matches, as well as text matches, when calling semantic similarity, and also use a lower morphological similarity threshold when doing so.
        return Matches.match(ehrClass, fhirClass, SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [TranslationConstants.TEXT_SIMILARITY_THRESHOLD, True, True, 0.75]);
           
    # See if there is a match at all, based on thresholds.
    @staticmethod
    def matches(ehr, fhir, textSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, morphologicalSimilarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, similarityThreshold=TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True, firstPastThreshold=True, highestStrength=False, combined=False, average=False):
        
        if ( Matches.match(ehr, fhir, SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [], TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold, semanticSimilarityThreshold, morphologicalSimilarityThreshold, similarityThreshold, highestCompositeResult, firstPastThreshold, highestStrength, combined, average) > 0 ):
            return True;
        
        else:
            return False;
        
    