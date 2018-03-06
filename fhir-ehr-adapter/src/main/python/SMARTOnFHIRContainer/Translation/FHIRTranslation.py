import json, inspect, collections, xml.etree.ElementTree, sys
from pprint import pprint
from difflib import SequenceMatcher
from nltk.corpus import wordnet

from Utils.Utilities import Utilities
from models.patient import Patient
from EHR.SystmOne import SystmOne

class FHIRTranslation():
    
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
    def containsWords(ehrAttribute, fhirAttribute, similarityThreshold):
        
        matches = 0;
        
        for ehrAttributeWord in Utilities.listFromCapitals(ehrAttribute):
            
            for fhirAttributeWord in Utilities.listFromCapitals(fhirAttribute):
                
                if FHIRTranslation.textSimilarity(ehrAttributeWord, fhirAttributeWord) > similarityThreshold:
                    
                    matches = matches + 1;
        
        return matches / float(max(len(Utilities.listFromCapitals(ehrAttribute)), len(Utilities.listFromCapitals(fhirAttribute))));       
        
    @staticmethod
    def translatePatient():
        
        # Get JSON representation of FHIR resource (Patient).
        #patientJSON = Utilities.JSONfromFHIRClass(Patient, False);
        
        # Get patient record from EHR
        # SystmOne().getPatientRecord("4917111072");
        
        print FHIRTranslation.containsWords("CareStartDate", "state_address", 0.6);
        
        # Find candidate in FHIR representation for each EHR XML attribute.
        for ehrAttribute in FHIRTranslation.getXMLElements(xml.etree.ElementTree.parse('../../../../resources/ehr-response-extract.xml').find("Response"), set(), True):
            
            for fhirAttribute in Utilities.getReplaceJSONKeys(json.load(open('../../../../resources/patient-fhir-extract.json')), ""):
                
                # Order for metric importance.
                if ( FHIRTranslation.semanticSimilarity(ehrAttribute, fhirAttribute) > 0.8 ):
                    print ehrAttribute + " " + fhirAttribute;
                    break;
                
                if ( FHIRTranslation.textSimilarity(ehrAttribute, fhirAttribute) > 0.8 ):
                    print ehrAttribute + " " + fhirAttribute;
                    break; 
                
                if ( FHIRTranslation.containsWords(ehrAttribute, fhirAttribute, 0.6) > 0.5 ):
                    print ehrAttribute + " " + fhirAttribute;
                    break;
                
        # Match components of patient record from EHR to components from JSON representation
        
        # Replace values
        #Utilities.getReplaceJSONKeys(patientJSON, None, list(), 'id', 'abc');
        
        # return.
        #return patientJSON
       