import sys

from translation.FHIRTranslation import FHIRTranslation
from translation.matches import Matches
from translation.translationConstants import TranslationConstants
from translation.similarityMetrics import SimilarityMetrics
from utils.utilities import Utilities

if __name__ == "__main__":

    ft = FHIRTranslation();

    if len(sys.argv) == 2:
        ft.translatePatient(0, sys.argv[1]);

    elif len(sys.argv) == 4:
        if ( sys.argv[1] == "-c" ):
            action = 1;
        elif ( sys.argv[1] == "-m" ):
            action = 2;
        elif ( sys.argv[1] == "-M" ):
            action = 3;
        elif ( sys.argv[1] == "-s" ):
            action = 4;
        elif ( sys.argv[1] == "-g" ):
            action = 5;

        ft.translatePatient(action, None, sys.argv[2], sys.argv[3]);

    else:
        FHIRTranslation.translatePatient("");
        #print FHIRTranslation.textSimilarity("medicine", "medication", True);
        #print Matches.match("drug", "medication", TranslationConstants.TEXT_SIMILARITY_WEIGHTING,  TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING,  TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);
        #print FHIRTranslation.matches("scheme", "system", FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD);
        #print Matches.fuzzyMatch("Drug", "Medication");
        #print ft.childSimilarity("Demographics", "models_subset.patient.Patient", None, None, ft.getPatient("4917111072"), True);
        #print ft.childSimilarity("ClinicalCode", "models_subset.codeableconcept.CodeableConcept", None, None, ft.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Medication", "models_full.medicationrequest.MedicationRequest", None, None, FHIRTranslation.getPatient("4917111072"), True);
        #print FHIRTranslation.childSimilarity("Medication", "models_full.sequence.SequenceStructureVariantInner", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Demographics", "models_full.patient.Patient", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Demographics", "models_full.activitydefinition.ActivityDefinition", None, None, FHIRTranslation.getPatient("4917111072"));
