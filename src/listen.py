import sys, requests, uvicorn, uuid

from utils.utilities import Utilities
from FHIR.utilities import Utilities
from FHIR.create import create
from translation.FHIRTranslation import FHIRTranslation
from translation.translationConstants import TranslationConstants

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route, Router

from xml.etree import ElementTree;

router = Router([Mount("/create", app=create)])
app = Starlette(debug=True)
app.mount("", router)

def getPatient(id):
    return ElementTree.parse('../example-ehr-data/' + TranslationConstants.EHR_PATH + ( "-extract" if TranslationConstants.DEMO else "-full" ) + '.xml').find(TranslationConstants.EHR_ENTRY_POINT);

@app.route("/simulateTranslatePatient")
def simulateTranslatePatient(request):
    FHIRTranslation.translatePatient(getPatient("4917111072"));

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3004)
