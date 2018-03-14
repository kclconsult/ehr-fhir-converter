import json, inspect, collections, xml.etree.ElementTree, sys
from pprint import pprint
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer
import pkgutil
import pyclbr;

from models.patient import Patient
import models;

from EHR.SystmOne import SystmOne
from Utils.Utilities import Utilities

class FHIRTranslation():
    
    # Could adjust based on user feedback if, for example, matches are too generous.
    # A user-friendly way of asking about this 'do you feel you've got too many results?'.
    TEXT_SIMILARITY_THRESHOLD = 0.95;
    
    SEMANTIC_SIMILARITY_THRESHOLD = 0.8;
    
    GRAMMATICAL_SIMILARITY_THRESHOLD = 0.5;
    
    OVERALL_SIMILARITY_THRESHOLD = 0.95;
    
    # If some metrics are too generous (e.g. semantic matching 'address' and 'reference'), then we can reduce their 'contribution' to the measure of similarity using a weighting.
    TEXT_SIMILARITY_WEIGHTING = 1;
    
    SEMANTIC_SIMILARITY_WEIGHTING = 0.8;
    
    GRAMMATICAL_SIMILARITY_WEIGHTING = 0.6;
    
    
    
    # Perhaps don't replace matches outright e.g. address (XML) matching to address (JSON) might suggest that the content of address (JSON) should be replaced with the content of address (XML), but in reality address has sub-JSON fields which are better for this e.g. postcode. Check if any children have been filled, and if they have don't replace parent? -- Only looking at child elements might help with this.
    
    # Similarity Metric A
    @staticmethod
    def textSimilarity(ehrAttribute, fhirAttribute, stem=True):
        
        # Gradually more complex text similarity
        if ehrAttribute == fhirAttribute:
            return 1.0;
        
        if ehrAttribute.lower() in fhirAttribute:
            return len(ehrAttribute) / float(len(fhirAttribute));
        
        if stem:
            stemmer = PorterStemmer()
            ehrAttribute = stemmer.stem(ehrAttribute);
            fhirAttribute = stemmer.stem(fhirAttribute);
            
        return fuzz.ratio(ehrAttribute, fhirAttribute) / 100.0;
    
    # Similarity Metric B
    @staticmethod
    def semanticSimilarity(ehrAttribute, fhirAttribute):
        
        # https://docs.python.org/2/library/sys.html#sys.maxint
        highestSimilarity = 0;
       
        # wordnet requires word separation by underscore, whereas EHR XML responses (for TPP at least) use camelCase.
        for set in wordnet.synsets(Utilities.capitalToSeparation(ehrAttribute)):
           
            for word in set.lemma_names():
                
                # Get similarity between synonym for ehrAttribute and fhirAttribute. If this is over a given threshold, mark as a semantic match.
                if not word == ehrAttribute and FHIRTranslation.textSimilarity(word, fhirAttribute, True) > highestSimilarity and FHIRTranslation.textSimilarity(word, fhirAttribute, True) > FHIRTranslation.TEXT_SIMILARITY_THRESHOLD:
                    
                    highestSimilarity = FHIRTranslation.textSimilarity(word, fhirAttribute, True);
                    
        return highestSimilarity;    
     
    # Similarity Metric C
    @staticmethod
    def grammaticalSimilarity(ehrAttribute, fhirAttribute):
        
        highestSimilarity = 0;
        
        for lemma in Utilities.lemmas(ehrAttribute):
            
            if FHIRTranslation.textSimilarity(lemma, fhirAttribute, True) > highestSimilarity and FHIRTranslation.textSimilarity(lemma, fhirAttribute, True) > FHIRTranslation.TEXT_SIMILARITY_THRESHOLD:
                
                highestSimilarity = FHIRTranslation.textSimilarity(lemma, fhirAttribute, True);
                    
        return highestSimilarity;
    
    # Similarity Metric D - Sentence progression? e.g. "Done at" and "Location"
    ######
    
    @staticmethod
    def compositeStringSimilarity(ehrClass, fhirClass, comparisonMethod):
        
        # If ehrClass string is composite, compare each word with the FHIR target using all of the metrics, and 
        # then use chosen combination method to produce a value.
        # For each word, add these values, and then divide by number of words to get an average match across all words (or max?).
        highestSimilarity = 0;
        
        ehrWords = Utilities.listFromCapitals(ehrClass);
        fhirWords = Utilities.listFromCapitals(fhirClass);
        
        for ehrWord in ehrWords:
            
            for fhirWord in fhirWords:
            
                if( comparisonMethod(ehrWord, fhirWord) > highestSimilarity ):
                    
                    highestSimilarity = comparisonMethod(ehrWord, fhirWord);

        return highestSimilarity;
    
    @staticmethod
    def translatePatient():
    
        FHIRTranslation.translatePatientInit();
    
    # Event -> Encounter 
    # Try using content of EHR class to work out FHIR class
    # Input data from multiple EHRs to work out mapping (e.g. Vision has lots more stuff for event).
    
    # Shortest path between two joined concepts in EHR confirms connection in FHIR? E.g. closest mention of 'medication' to 'location' (both are under same XML head in EHR), is 'clinicalimpression' and 'encounter', so these classes are used to hold this information.
    @staticmethod
    def translatePatientInit():
        
        # Get JSON representation of FHIR resource (Patient).
        # Testing: json.load(open('../../../../resources/patient-fhir.json')
        # patientJSON = Utilities.JSONfromFHIRClass(Patient, False);
        
        # Get patient record from EHR
        # SystmOne().getPatientRecord("4917111072");
        
        # Match components of patient record from EHR to components from JSON representation
        
        # Find classes, and then match within those classes.
        for ehrClass in Utilities.getXMLElements(xml.etree.ElementTree.parse('../../../../resources/tpp.xml').find("Response"), set(), False, True):
            
            for _, fhirModule, _ in pkgutil.iter_modules(['models']):
                
                for fhirClass in pyclbr.readmodule("models." + fhirModule).keys():
                    
                    # Different threshold if two words (less strict).
                    # Single threshold for all
                    if (FHIRTranslation.compositeStringSimilarity(ehrClass, fhirClass, FHIRTranslation.textSimilarity) * FHIRTranslation.TEXT_SIMILARITY_WEIGHTING >= FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD or 
                        FHIRTranslation.compositeStringSimilarity(ehrClass, fhirClass, FHIRTranslation.semanticSimilarity) * FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING >= FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD or 
                        FHIRTranslation.compositeStringSimilarity(ehrClass, fhirClass, FHIRTranslation.grammaticalSimilarity) * FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING >= FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD):
                        
                        print ehrClass + " " + fhirClass + " (" + str(FHIRTranslation.compositeStringSimilarity(ehrClass, fhirClass, FHIRTranslation.textSimilarity)) + " " + str(FHIRTranslation.compositeStringSimilarity(ehrClass, fhirClass, FHIRTranslation.semanticSimilarity)) + " " + str(FHIRTranslation.compositeStringSimilarity(ehrClass, fhirClass, FHIRTranslation.grammaticalSimilarity)) + ")";
                
                # If there are multiple matches, e.g. with medication, NOW find which candidate class can house the attributes from the EHR header best.
              
        # Replace values
        # Utilities.getReplaceJSONKeys(patientJSON, None, list(), 'id', 'abc');
        
        # return.
        # return patientJSON
      
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
    
    ##########
    
    # Combination Mechanism A
    @staticmethod
    def averageSimilarity(ehrClass, fhirClass):
        
        # Add all similarities together, divide to get between 0 and 1.
        return (FHIRTranslation.textSimilarity(ehrClass, fhirClass, True) + 
                FHIRTranslation.semanticSimilarity(ehrClass, fhirClass) + 
                FHIRTranslation.grammaticalSimilarity(ehrClass, fhirClass)) / 3.0;
        
    # Combination Mechanism B
    @staticmethod
    def maxSimilarity(ehrClass, fhirClass):
        
        return max(FHIRTranslation.textSimilarity(ehrClass, fhirClass, True), 
               max(FHIRTranslation.semanticSimilarity(ehrClass, fhirClass), FHIRTranslation.grammaticalSimilarity(ehrClass, fhirClass)));
    
    ##########
                