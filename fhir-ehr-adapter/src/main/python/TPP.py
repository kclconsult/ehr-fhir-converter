import socket, sys, time, xml.dom.minidom
from APIConstants import APIConstants
from APIVariables import APIVariables
from Utils import Utilities

class TPP(object):
    
    def __init__(self):
        
        Utilities.xmlRequest(
            '<Function>GetPatientRecord</Function>' + \
            '<APIKey>' + APIVariables.KEY + '</APIKey>' + \
            '<DeviceID>'+ APIVariables.DEVICE_ID +'</DeviceID>' + \
            '<DeviceVersion>' + APIVariables.DEVICE_VERSION + '</DeviceVersion>' + \
            '<FunctionVersion>' + APIVariables.FUNCTION_VERSION + '</FunctionVersion>' + \
            '<FunctionParameters>' + \
            '<Identity><NhsNumber>4917111072</NhsNumber></Identity>' + \
            APIConstants.LEAVE_RECORD_OPEN + \
            '<Filter> <ClinicalCode>X3003</ClinicalCode> <ClinicalCode>XaBVJ</ClinicalCode> <Numeric>XE2mq</Numeric> </Filter>' + \
            APIConstants.MEDICATION + \
            '</FunctionParameters>'
        );