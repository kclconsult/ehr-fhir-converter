import socket, sys, time, xml.dom.minidom, uuid

from xml.sax.saxutils import escape
from EHR.APIConstants import APIConstants
from EHR.APIVariables import APIVariables

class Utilities(object):
    
    @staticmethod 
    def printElementProperties(data):
        
        print "======================"
        print "New class: " + data
        print "======================"
        
        for x in data.elementProperties(data()):
            invert_op = getattr(x[2], "elementProperties", None)
            
            if callable(invert_op) and "Extension" not in str(x[2]):
                print x[0] + " " + str(data) + " --> " + str(x[2])
                Utilities.printElementProperties(x[2])
                print "======================"
                print "Back to: " + str(data)
                print "======================"
                
            else:
                print x[0] + " " + str(x[2])
                
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