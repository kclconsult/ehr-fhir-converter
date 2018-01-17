import json, inspect, collections
from pprint import pprint

from Utils.Utilities import Utilities
from models.patient import Patient
from models.humanname import HumanName
from models.extension import Extension
from models.address import Address
from models.coding import Coding

class FHIRTranslation():
    
    @staticmethod
    def translatePatient():
        
        Utilities.printElementProperties(Patient)
        
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