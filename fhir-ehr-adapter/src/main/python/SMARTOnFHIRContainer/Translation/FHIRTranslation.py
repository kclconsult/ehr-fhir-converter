import json, inspect, collections, xml.etree.ElementTree
from pprint import pprint
from difflib import SequenceMatcher
from nltk.corpus import wordnet

from Utils.Utilities import Utilities
from models.patient import Patient
from EHR.SystmOne import SystmOne

class FHIRTranslation():
    
    @staticmethod
    def getXMLElements(root, set):
        
        set.add(root.tag)
        
        for elem in root.getchildren():
            FHIRTranslation.getXMLElements(elem, set)
            
        return set
       
    # Perhaps don't replace matches outright e.g. address (XML) matching to address (JSON) might suggest that the content of address (JSON) should be replaced with the content of address (XML), but in reality address has sub-JSON fields which are better for this e.g. postcode. Check if any children have been filled, and if they have don't replace parent?
    
    # Similarity Metric A
    @staticmethod
    def textSimilarity(ehrAttribute, fhirAttribute):
        return SequenceMatcher(None, ehrAttribute, fhirAttribute).ratio()
    
    # Similarity Metric B
    @staticmethod
    def semanticSimilarity(ehrAttribute, fhirAttribute, textSimilarityThreshold):
       
        similarityMatches = 0
        generatedSynonyms = 0;
       
        # wordnet requires word separation by underscore, whereas EHR XML responses (for TPP at least) use camelCase.
        for set in wordnet.synsets(Utilities.captialToSeparation(ehrAttribute)):
           
            for word in set.lemma_names():
               
               # Get similarity between synonym for ehrAttribute and fhirAttribute. If this is over a given threshold, mark as a semantic match.
                if FHIRTranslation.textSimilarity(word, fhirAttribute) > textSimilarityThreshold:
                    similarityMatches = similarityMatches + 1
                   
                generatedSynonyms = generatedSynonyms + 1;
               
        # Take synonyms that matched over total possible synonyms as this metric:
        if generatedSynonyms > 0:
            return similarityMatches / generatedSynonyms
        
        else:
            return 0
    
    # Similarity Metric C
    # Split ehr and fhir attributes into individual words, and see how many match. Would tackle cases such as DateOfBirth and BirthDate.
    def containsWords(self):
        pass
        
    @staticmethod
    def translatePatient():
        
        # Get JSON representation of FHIR resource (Patient).
        patientJSON = Utilities.JSONfromFHIRClass(Patient, False);
        
        # Get patient record from EHR
        # SystmOne().getPatientRecord("4917111072");
        
        #Find candidate in FHIR representation for each EHR XML attribute.
        for ehrAttribute in FHIRTranslation.getXMLElements(xml.etree.ElementTree.parse('../../../../resources/ehr-response-extract.xml').getroot(), set()):
            
            for fhirAttribute in Utilities.getReplaceJSONKeys(json.load(open('../../../../resources/patient-fhir-extract.json')), ""):
            
                if ( FHIRTranslation.semanticSimilarity(ehrAttribute, fhirAttribute, 0.5) > 0.5 ) :
                    
                    print ehrAttribute + " " + fhirAttribute
                
            
        # Match components of patient record from EHR to components from JSON representation
        
        # Replace values
        #Utilities.getReplaceJSONKeys(patientJSON, None, list(), 'id', 'abc');
        
        # return.
        #return patientJSON
       