import sys, requests, uvicorn, uuid

from utils.utilities import Utilities
from FHIR.utilities import Utilities
from FHIR.create import create

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route, Router

router = Router([Mount("/create", app=create)])
app = Starlette(debug=True)
app.mount("", router)

@app.route("/simulateTranslatePatient")
def simulateTranslatePatient(request):
    FHIRTranslation.translatePatient();

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3004)
