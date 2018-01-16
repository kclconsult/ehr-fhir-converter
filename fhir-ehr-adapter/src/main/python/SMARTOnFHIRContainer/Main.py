from BaseHTTPServer import HTTPServer
import uuid, requests, json

from EHR.SystmOne import SystmOne
from FHIR.FHIRServer import FHIRServer
from FHIR.FHIRConstants import FHIRConstants
from Translation.FHIRTranslation import FHIRTranslation

if __name__ == "__main__":
    
    #SystmOne().getPatientRecord("4917111072");
    
    #server_address = ('', 8080)
    #httpd = HTTPServer(server_address, FHIRServer)
    #httpd.serve_forever()
    
    FHIRTranslation.translatePatient()