import sys, time;

from BaseHTTPServer import HTTPServer
import uuid, requests, json

from FHIR.FHIRServer import FHIRServer
from Translation.FHIRTranslation import FHIRTranslation
import SMARTOnFHIRContainer
       
def addArguments(*args):
    FHIRServer(False, *args)
          
def serve():
    
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, addArguments)
    print time.asctime(), "Server Starts - %s:%s" % (server_address, 8080)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (server_address, 8080)

 
if __name__ == "__main__":
    
    SMARTOnFHIRContainer.serve();