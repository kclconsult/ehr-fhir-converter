import time, datetime
from BaseHTTPServer import BaseHTTPRequestHandler

from FHIRConstants import FHIRConstants

class FHIRServer(BaseHTTPRequestHandler):
    
    def _set_headers(self, id):
        
        self.send_response(200)
        self.send_header('date', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        self.send_header('server', '')
        self.send_header('last-modified', '')
        self.send_header('transfer-encoding', 'chunked')
        self.send_header('x-powered-by', 'fhir-ehr-adpater')
        self.send_header('content-type', 'application/fhir+json;charset=utf-8')
        self.send_header('connection', 'keep-alive')
        self.send_header('etag', '') # ETag header with the versionId of the resource (if versioning is supported)
        self.send_header('location', FHIRConstants.BASE_URL + "/patient/" + str(id))
        self.end_headers()

    def do_GET(self): 
        id = self.path.rsplit('/', 1)[-1];
        self._set_headers(id)

        SystmOne().getPatientRecord("4917111072");
        self.wfile.write("")
