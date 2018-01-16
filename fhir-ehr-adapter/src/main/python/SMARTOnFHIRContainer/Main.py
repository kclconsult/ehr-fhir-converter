from BaseHTTPServer import HTTPServer
import uuid, requests

from EHR.SystmOne import SystmOne
from FHIR.FHIRServer import FHIRServer
from FHIR.FHIRConstants import FHIRConstants

if __name__ == "__main__":
    
    #sysone = SystmOne()
    #sysone.getPatientRecord("4917111072");
    
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, FHIRServer)
    httpd.serve_forever()