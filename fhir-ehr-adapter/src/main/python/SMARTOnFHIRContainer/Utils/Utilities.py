import socket, sys, time, xml.dom.minidom, uuid, json

from xml.sax.saxutils import escape

from EHR.APIConstants import APIConstants
from EHR.APIVariables import APIVariables

class Utilities(object):
    
    @staticmethod 
    def captialToSeparation(word):
        
        index = 0;
        
        for letter in list(word):
            
            if index > 0 and letter.isupper():
                word = word[0:index] + "_" + word[index:len(word)]
                index = index + 1
                
            index = index + 1
            
        return word
        
    
    @staticmethod 
    def JSONfromFHIRClass(FHIRClass, nullValues):

        # Create new object to represent this new class.
        FHIRObject = FHIRClass();
        
        for attribute in FHIRClass.elementProperties(FHIRClass()):
            invert_op = getattr(attribute[2], "elementProperties", None)
            
            # Don't expand from within FHIRReferences, as it has a recursive reference to identifier (also doesn't appear to be captured correctly by the parser, e.g. organization from Patient).
            # Extensions classes appear in every class so don't show anything unique.
            if callable(invert_op) and "FHIRReference" not in str(FHIRClass) and "Extension" not in str(attribute[2]):             
                subJSON = Utilities.JSONfromFHIRClass(attribute[2], nullValues)
                setattr(FHIRObject, str(attribute[0]), subJSON)
                
            else:
                if (nullValues): 
                    setattr(FHIRObject, str(attribute[0]), None)
                    
                else:
                    setattr(FHIRObject, str(attribute[0]), str(attribute[2]))
                    
        return FHIRObject.__dict__;
    
    @staticmethod    
    def getReplaceJSONKeys(data, parents=None, keys=list(), search=None, replace=None):
        
        if isinstance(data, dict):
            
            for k, v in data.items():
                    
                if parents != None and len(parents) > 0:
                    k = k + "_" + parents
               
                keys.append(k);
                
                if (k == search):
                    data[search] = replace
                
                if not isinstance(v, basestring) and not v is None:
                    if parents != None:
                        parents = k;
                        
                    keys = Utilities.getReplaceJSONKeys(v, parents, keys, search, replace)
                    
                    if parents != None:
                        parents = ""
                       
                
        return keys
    
    @staticmethod    
    def printJSONValues(data):
        
        if isinstance(data, dict):
            
            for k, v in data.items():
                
                if isinstance(v, basestring):
                    print k
                    
                else:
                    Utilities.printJSONValues(v)
                    
        elif isinstance(data, list):
            
            for v in data:
                
                if not isinstance(v, str):
                    Utilities.printJSONValues(v)
                    
        else:
            print data;
            
    @staticmethod
    def xmlRequest(data):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_address = (APIVariables.ADDRESS, APIVariables.PORT)
        
        sock.connect(server_address);
        
        response=""
        
        try:
            
            request = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<ClientIntegrationRequest>' + \
            '<RequestUID>' + str(uuid.uuid4()) + '</RequestUID>' + \
            data + \
            '</ClientIntegrationRequest>'
            
            print request;
            sock.sendall(request.encode('utf-8'))
        
            sock.settimeout(20);
            
            time.sleep(2)
            
            BUFF_SIZE = 4096
            
            response = ""
            
            while True:
            
                part = sock.recv(BUFF_SIZE)
                
                response += part
                
                if len(part) < BUFF_SIZE:
                    break
            
            try:
                
                formatted = xml.dom.minidom.parseString(response)
            
                pretty_xml_as_string = formatted.toprettyxml()
            
                return pretty_xml_as_string
            
            except xml.parsers.expat.ExpatError:
                
                return "Cannot parse response. Is the EHR running?"
        
        finally:
            
            sock.close()