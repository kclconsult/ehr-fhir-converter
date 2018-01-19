import json, inspect, collections, xml.etree.ElementTree
from pprint import pprint
from difflib import SequenceMatcher

from Utils.Utilities import Utilities
from models.patient import Patient
from EHR.SystmOne import SystmOne

class FHIRTranslation():
    
    @staticmethod
    def printRecur(root, set):
        
        set.add(root.tag.title())
        
        for elem in root.getchildren():
            FHIRTranslation.printRecur(elem, set)
            
        return set
       
    # Ontology that would understand 'first name' and 'given name' are similar.
    # Use parent JSON field as suffix eg. name: { given: X } becomes given name.   
    # Perhaps don't replace matches outright e.g. address (XML) matching to address (JSON) might suggest that the content of address (JSON) should be replaced with the content of address (XML), but in reality address has sub-JSON fields which are better for this e.g. postcode. Check if any children have been filled, and if they have don't replace parent?
      
    @staticmethod
    def translatePatient():
        
        # Get JSON representation of FHIR resource (Patient).
        patientJSON = Utilities.JSONfromFHIRClass(Patient, False);
        
        # Get patient record from EHR
        # SystmOne().getPatientRecord("4917111072");
        
        for ehrAttribute in FHIRTranslation.printRecur(xml.etree.ElementTree.parse('../../../../resources/ehr-response.xml').getroot(), set()):
            
            #Find candidate in FHIR representation for this attribute.
            for fhirAttribute in Utilities.getReplaceJSONKeys(patientJSON):
                
                if SequenceMatcher(None, ehrAttribute, fhirAttribute).ratio() > 0.8: 
                    print  ehrAttribute + " " + fhirAttribute
            
    
        # Match components of patient record from EHR to components from JSON representation
        
        # Replace values
        Utilities.getReplaceJSONKeys(patientJSON, set(), 'id', 'abc');
        
        # return.
        return patientJSON
       