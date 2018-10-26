import time, datetime, re, base64
from BaseHTTPServer import BaseHTTPRequestHandler

from FHIRConstants import FHIRConstants
from Translation.FHIRTranslation import FHIRTranslation

class FHIRServer(BaseHTTPRequestHandler):
    
    def __init__(self, live, *args):
        self.live = live
        BaseHTTPRequestHandler.__init__(self, *args)
        
    def _set_headers(self, id):
        
        self.send_response(200);
        self.send_header('date', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'));
        self.send_header('server', '');
        self.send_header('last-modified', '');
        #self.send_header('transfer-encoding', 'chunked');
        self.send_header('x-powered-by', 'fhir-ehr-adpater');
        self.send_header('content-type', 'application/fhir+json;charset=utf-8');
        self.send_header('etag', '');
        self.send_header('location', FHIRConstants.BASE_URL + "/patient/" + str(id));
        self.end_headers();
    
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_POST(self):
        
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        
        elif self.headers.getheader('Authorization') == 'Basic '+ base64.b64encode("consult:consultproject2017"):
            id = self.path.rsplit('/', 1)[-1];
            self._set_headers(id);
            if self.live:
                pass; # Our middleware returns translated patient
            else:
                self.wfile.write(''.join([re.sub('[\n\t]', '', line) for line in open('MRJhYh5V.py')]));
            pass
        
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass
        
       