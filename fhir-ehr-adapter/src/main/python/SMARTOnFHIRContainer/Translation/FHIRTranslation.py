import json, inspect, collections
from pprint import pprint

from Utils.Utilities import Utilities
from models.patient import Patient

class FHIRTranslation():
    
    @staticmethod
    def translatePatient():
        
        print json.dumps(Utilities.JSONfromFHIRClass(Patient, True).__dict__)
        
        #p = Patient()
        #n = HumanName()
        #n.given = "Martin"
        #p.name = n.__dict__;
        
        #attributes = Patient.elementProperties(p)
        
        #for x in attributes:
            #invert_op = getattr(x[2], "elementProperties", None)
            #if callable(invert_op):
                #print x[2]
            
        #print json.dumps(p.__dict__)