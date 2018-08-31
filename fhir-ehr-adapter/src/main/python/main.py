import sys

from Translation.FHIRTranslation import FHIRTranslation
from Utils.Utilities import Utilities

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
        FHIRTranslation.translatePatient();
        #print ft.childSimilarity("ClinicalCode", "models_subset.coding.Coding", None, None, ft.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Medication", "models_full.medicationrequest.MedicationRequest", None, None, FHIRTranslation.getPatient("4917111072"), True);
        #print FHIRTranslation.childSimilarity("Medication", "models_full.sequence.SequenceStructureVariantInner", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Demographics", "models_full.patient.Patient", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Demographics", "models_full.activitydefinition.ActivityDefinition", None, None, FHIRTranslation.getPatient("4917111072"));              
