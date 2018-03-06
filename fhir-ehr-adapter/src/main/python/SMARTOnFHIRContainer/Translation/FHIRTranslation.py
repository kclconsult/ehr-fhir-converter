import json, inspect, collections, xml.etree.ElementTree, sys
from pprint import pprint
from difflib import SequenceMatcher
from nltk.corpus import wordnet

from Utils.Utilities import Utilities
from models.patient import Patient
from EHR.SystmOne import SystmOne

class FHIRTranslation():
    
    # Could adjust based on user feedback if, for example, matches are too generous.
    # A user-friendly way of asking about this 'do you feel you've got too many results?'.
    TEXT_SIMILARITY_THRESHOLD = 0.8;
    
    @staticmethod
    def getXMLElements(root, set, childrenOnly=False):
        
        if childrenOnly:
            if len(root.getchildren()) == 0:
                set.add(root.tag);
        else:
            set.add(root.tag);
    
        for elem in root.getchildren():
            FHIRTranslation.getXMLElements(elem, set, childrenOnly);
            
        return set
       
    # Perhaps don't replace matches outright e.g. address (XML) matching to address (JSON) might suggest that the content of address (JSON) should be replaced with the content of address (XML), but in reality address has sub-JSON fields which are better for this e.g. postcode. Check if any children have been filled, and if they have don't replace parent? -- Only looking at child elements might help with this.
    
    # Similarity Metric A
    @staticmethod
    def textSimilarity(ehrAttribute, fhirAttribute):
        return SequenceMatcher(None, ehrAttribute, fhirAttribute).ratio()
    
    # Similarity Metric B
    @staticmethod
    def semanticSimilarity(ehrAttribute, fhirAttribute):
        
        # https://docs.python.org/2/library/sys.html#sys.maxint
        highestSimilarity = -sys.maxint - 1;
       
        # wordnet requires word separation by underscore, whereas EHR XML responses (for TPP at least) use camelCase.
        for set in wordnet.synsets(Utilities.capitalToSeparation(ehrAttribute)):
           
            for word in set.lemma_names():
                
                # Get similarity between synonym for ehrAttribute and fhirAttribute. If this is over a given threshold, mark as a semantic match.
                if FHIRTranslation.textSimilarity(word, fhirAttribute) > highestSimilarity:
                    highestSimilarity = FHIRTranslation.textSimilarity(word, fhirAttribute);
        
        return highestSimilarity;
    
    # Similarity Metric C
    # Splits ehr and fhir attributes into individual words, and sees how many match. Tackles cases such as DateOfBirth and BirthDate.
    @staticmethod
    def wordSimilarity(ehrAttribute, fhirAttribute):
        
        matches = 0;
        
        for ehrAttributeWord in Utilities.listFromCapitals(ehrAttribute):
            
            for fhirAttributeWord in Utilities.listFromCapitals(fhirAttribute):
                
                if FHIRTranslation.textSimilarity(ehrAttributeWord, fhirAttributeWord) >= FHIRTranslation.TEXT_SIMILARITY_THRESHOLD:
                    
                    matches = matches + 1;
        
        return matches / float(max(len(Utilities.listFromCapitals(ehrAttribute)), len(Utilities.listFromCapitals(fhirAttribute))));       
        
    @staticmethod
    def translatePatient():
        
        # Get JSON representation of FHIR resource (Patient).
        patientJSON = Utilities.JSONfromFHIRClass(Patient, False);
        
        # Get patient record from EHR
        # SystmOne().getPatientRecord("4917111072");
        
        # Find mappings between EHR and FHIR (needs some sort of preference in light of multiple suggestions for the same EHR item).
        print FHIRTranslation.similarity(FHIRTranslation.semanticSimilarity, 0.8, patientJSON);
        print FHIRTranslation.similarity(FHIRTranslation.textSimilarity, 0.8, patientJSON);
        print FHIRTranslation.similarity(FHIRTranslation.wordSimilarity, 0.5, patientJSON);
        
        # Match components of patient record from EHR to components from JSON representation
        
        # Replace values
        # Utilities.getReplaceJSONKeys(patientJSON, None, list(), 'id', 'abc');
        
        # return.
        #return patientJSON
        
    @staticmethod
    def similarity(similarityMethod, threshold, patientJSON):
        
        mappings = [];
        
        # Find candidate in FHIR representation for each EHR XML attribute.
        for ehrAttribute in FHIRTranslation.getXMLElements(xml.etree.ElementTree.parse('../../../../resources/ehr-response-extract.xml').find("Response"), set(), True):
            
            highestSimilarity = -sys.maxint - 1;
            mapping = [0] * 2;
            
            # json.load(open('../../../../resources/patient-fhir.json')
            for fhirAttribute in Utilities.getReplaceJSONKeys(patientJSON, ""):
                
                if ( similarityMethod(ehrAttribute, fhirAttribute) > highestSimilarity ):
                    
                    mapping[0] = ehrAttribute;
                    mapping[1] = fhirAttribute;
                    highestSimilarity = similarityMethod(ehrAttribute, fhirAttribute);
                   
            if highestSimilarity > -sys.maxint - 1 and highestSimilarity > threshold:    
                mappings.append(mapping);
        
        return mappings;
                