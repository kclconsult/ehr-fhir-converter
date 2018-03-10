import json, inspect, collections, xml.etree.ElementTree, sys
from pprint import pprint
from difflib import SequenceMatcher
import Levenshtein
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet

from Utils.Utilities import Utilities
from models.patient import Patient
import models;
from EHR.SystmOne import SystmOne
import pkgutil

class FHIRTranslation():
    
    # Could adjust based on user feedback if, for example, matches are too generous.
    # A user-friendly way of asking about this 'do you feel you've got too many results?'.
    TEXT_SIMILARITY_THRESHOLD = 0.8;
    
    # Perhaps don't replace matches outright e.g. address (XML) matching to address (JSON) might suggest that the content of address (JSON) should be replaced with the content of address (XML), but in reality address has sub-JSON fields which are better for this e.g. postcode. Check if any children have been filled, and if they have don't replace parent? -- Only looking at child elements might help with this.
    
    # Similarity Metric A
    @staticmethod
    def textSimilarity(ehrAttribute, fhirAttribute):
        return fuzz.partial_ratio(ehrAttribute, fhirAttribute) / 100.0;
    
    # Similarity Metric B
    @staticmethod
    def semanticSimilarity(ehrAttribute, fhirAttribute):
        
        # https://docs.python.org/2/library/sys.html#sys.maxint
        highestSimilarity = 0;
       
        # wordnet requires word separation by underscore, whereas EHR XML responses (for TPP at least) use camelCase.
        for set in wordnet.synsets(Utilities.capitalToSeparation(ehrAttribute)):
           
            for word in set.lemma_names():
                
                # Get similarity between synonym for ehrAttribute and fhirAttribute. If this is over a given threshold, mark as a semantic match.
                if word != ehrAttribute and FHIRTranslation.textSimilarity(word, fhirAttribute) > highestSimilarity:
                    
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
     
    # Similarity Metric D
    @staticmethod
    def grammaticalSimilarity(ehrAttribute, fhirAttribute):
        
        highestSimilarity = 0;
        
        for lemma in Utilities.lemmas(ehrAttribute):
            
            if FHIRTranslation.textSimilarity(lemma, fhirAttribute) > highestSimilarity:
                
                highestSimilarity = FHIRTranslation.textSimilarity(lemma, fhirAttribute);
                    
        return highestSimilarity;
    
    # Similarity Metric E
    # Finds different grammatical forms of the words in compound (CamelCase) EHR attributes and then uses
    # wordSimilarity to compare (essentially makes the wordSimilarity metric more flexible).
    @staticmethod
    def wordGrammaticalSimilarty(ehrAttribute, fhirAttribute):
        
        highestSimilarity = 0;
        
        for form in Utilities.differentWordForms(ehrAttribute):
            
            if FHIRTranslation.wordSimilarity(form, fhirAttribute) > highestSimilarity:
                
                highestSimilarity = FHIRTranslation.wordSimilarity(form, fhirAttribute);
        
        return highestSimilarity;
    
    ##########
    
    # Combination Mechanism A
    @staticmethod
    def averageSimilarity(ehrClass, fhirClass):
        
        # Add all similarities together, divide to get between 0 and 1.
        return (FHIRTranslation.textSimilarity(ehrClass, fhirClass) + FHIRTranslation.semanticSimilarity(ehrClass, fhirClass) + FHIRTranslation.wordSimilarity(ehrClass, fhirClass) + FHIRTranslation.grammaticalSimilarity(ehrClass, fhirClass) + FHIRTranslation.wordGrammaticalSimilarty(ehrClass, fhirClass)) / 5.0;
        
    # Combination Mechanism B
    @staticmethod
    def maxSimilarity(ehrClass, fhirClass):
        
        return max(FHIRTranslation.textSimilarity(ehrClass, fhirClass), max(FHIRTranslation.semanticSimilarity(ehrClass, fhirClass), max(FHIRTranslation.wordSimilarity(ehrClass, fhirClass), max(FHIRTranslation.grammaticalSimilarity(ehrClass, fhirClass), FHIRTranslation.wordGrammaticalSimilarty(ehrClass, fhirClass)))));
        
    @staticmethod
    def translatePatient():
        
        #print FHIRTranslation.textSimilarity("identity", "patient");
        
        FHIRTranslation.translatePatient2();
         
    @staticmethod
    def translatePatient2():
        
        # Get JSON representation of FHIR resource (Patient).
        # Testing: json.load(open('../../../../resources/patient-fhir.json')
        # patientJSON = Utilities.JSONfromFHIRClass(Patient, False);

        
        # Find classes, and then match within those classes.
        for ehrClass in Utilities.getXMLElements(xml.etree.ElementTree.parse('../../../../resources/tpp.xml').find("Response"), set(), False, True):
            
            print ehrClass
            for _, fhirClass, _ in pkgutil.iter_modules(['models']):
                
                overallSimilarity = FHIRTranslation.averageSimilarity(ehrClass, fhirClass);
                
                if overallSimilarity >= 0.5:
                    print ehrClass + " " + fhirClass + " " + str(overallSimilarity);
           
        # Get patient record from EHR
        # SystmOne().getPatientRecord("4917111072");
        
        # Find mappings between EHR and FHIR (needs some sort of preference in light of multiple suggestions for the same EHR item).
        # print FHIRTranslation.map(FHIRTranslation.semanticSimilarity, 0.8, patientJSON);
        # print FHIRTranslation.map(FHIRTranslation.textSimilarity, 0.8, patientJSON);
        # print FHIRTranslation.map(FHIRTranslation.wordSimilarity, 0.5, patientJSON);
        
        # Match components of patient record from EHR to components from JSON representation
        
        # Replace values
        # Utilities.getReplaceJSONKeys(patientJSON, None, list(), 'id', 'abc');
        
        # return.
        #return patientJSON
      
    @staticmethod
    def map(similarityMethod, threshold, patientJSON):
        
        mappings = [];
        
        # Find candidate in FHIR representation for each EHR XML attribute.
        for ehrAttribute in Utilities.getXMLElements(xml.etree.ElementTree.parse('../../../../resources/ehr-response.xml').find("Response"), set(), True):
            
            highestSimilarity = -sys.maxint - 1;
            mapping = [0] * 2;
            
            for fhirAttribute in Utilities.getReplaceJSONKeys(patientJSON, ""):
                
                if ( similarityMethod(ehrAttribute, fhirAttribute) > highestSimilarity ):
                    
                    mapping[0] = ehrAttribute;
                    mapping[1] = fhirAttribute;
                    highestSimilarity = similarityMethod(ehrAttribute, fhirAttribute);
                   
            if highestSimilarity > -sys.maxint - 1 and highestSimilarity > threshold:    
                mappings.append(mapping);
        
        return mappings;
                