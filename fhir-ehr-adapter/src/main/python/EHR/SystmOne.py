import socket, sys, time, xml.dom.minidom
from APIConstants import APIConstants
from APIVariables import APIVariables
from Utils import Utilities

class SystmOne(object):
    
    @staticmethod
    def contactAPI(call, id):
         
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
    
    @staticmethod
    def getPatientRecord(id):
        
        print SystmOne.contactAPI("GetPatientRecord", id);
       