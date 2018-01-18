import socket, sys, time, xml.dom.minidom, uuid, json

from xml.sax.saxutils import escape
from EHR.APIConstants import APIConstants
from EHR.APIVariables import APIVariables

class Utilities(object):
    
    @staticmethod 
    def JSONfromFHIRClass(FHIRClass, nullValues):

        # Create new object to represent this new class.
        FHIRObject = FHIRClass();
        
        for attribute in FHIRClass.elementProperties(FHIRClass()):
            invert_op = getattr(attribute[2], "elementProperties", None)
            
            # Don't expand from within FHIRReferences, as it has a recursive reference to identifier (also doesn't appear to be captured correctly by the parser, e.g. organisation from Patient.
            # Extensions classes appear in every class so don't show anything unique.
            if callable(invert_op) and "FHIRReference" not in str(FHIRClass) and "Extension" not in str(attribute[2]):             
                subJSON = Utilities.JSONfromFHIRClass(attribute[2], nullValues)
                setattr(FHIRObject, attribute[0], subJSON.__dict__)
            else:
                if (nullValues): 
                    setattr(FHIRObject, attribute[0], None)
                else:
                    setattr(FHIRObject, attribute[0], str(attribute[2]))
                    
        return FHIRObject;
                
    @staticmethod    
    def printJSON(data):
        
        if isinstance(data, dict):
            
            for k, v in data.items():
                
                if isinstance(v, basestring):
                    print k
                    
                else:
                    Utilities.printJSON(v)
                    
        elif isinstance(data, list):
            
            for v in data:
                
                if not isinstance(v, str):
                    Utilities.printJSON(v)
                    
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