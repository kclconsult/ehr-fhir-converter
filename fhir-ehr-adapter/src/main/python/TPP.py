import socket, sys, time, xml.dom.minidom
from APIConstants import APIConstants
from APIVariables import APIVariables
from Utils import Utilities

class TPP(object):
    
    def contactAPI(self, call, id):
         
         return Utilities.xmlRequest(
             
            '<Function>' + call + '</Function>' + \
            '<APIKey>' + APIVariables.KEY + '</APIKey>' + \
            '<DeviceID>'+ APIVariables.DEVICE_ID +'</DeviceID>' + \
            '<DeviceVersion>' + APIVariables.DEVICE_VERSION + '</DeviceVersion>' + \
            '<FunctionVersion>' + APIVariables.FUNCTION_VERSION + '</FunctionVersion>' + \
            '<FunctionParameters>' + \
            '<Identity><NhsNumber>' + id + '</NhsNumber></Identity>' + \
            '</FunctionParameters>'
            
        );
    
    def getPatientRecord(self, id):
        
        print self.contactAPI("GetPatientRecord", id);
       