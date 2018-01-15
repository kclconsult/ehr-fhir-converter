from BaseHTTPServer import HTTPServer
import uuid;

from EHR.SystmOne import SystmOne
from FHIR.FHIRServer import FHIRServer

if __name__ == "__main__":
    
    #sysone = SystmOne()
    #sysone.getPatientRecord("4917111072");
    
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, FHIRServer)
    print 'Starting httpd...'
    httpd.serve_forever()