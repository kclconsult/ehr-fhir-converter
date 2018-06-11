import sys, time;

from BaseHTTPServer import HTTPServer
import uuid, requests, json

from EHR.SystmOne import SystmOne
from FHIR.FHIRServer import FHIRServer
from FHIR.FHIRConstants import FHIRConstants
from Translation.FHIRTranslation import FHIRTranslation

# Our middleware
def translate():
    
    if len(sys.argv) == 2:                                                           
        FHIRTranslation.translatePatient(0, sys.argv[1]);
        
    elif len(sys.argv) == 4:
        if ( sys.argv[1] == "-c" ):
            action = 1;
        elif ( sys.argv[1] == "-m" ):
            action = 2;
        elif ( sys.argv[1] == "-M" ):
            action = 3;
        elif ( sys.argv[1] == "-s" ):
            action = 4;
        elif ( sys.argv[1] == "-g" ):
            action = 5;
        
        FHIRTranslation.translatePatient(action, None, sys.argv[2], sys.argv[3]);
          
    else:
        FHIRTranslation.translatePatient()
        
# The container   
def serve():
    
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, FHIRServer)
    print time.asctime(), "Server Starts - %s:%s" % (server_address, 8080)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (server_address, 8080)
    