import json
from pprint import pprint

from Utils.Utilities import Utilities

class FHIRTranslation():
    
    @staticmethod
    def translatePatient():
         
        data = json.load(open('../../../../resources/patient-fhir.json'))
    
        Utilities.printJSON(data)