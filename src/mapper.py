import sys

from translation.FHIRTranslation import FHIRTranslation
from translation.matches import Matches
from translation.translationConstants import TranslationConstants
from translation.similarityMetrics import SimilarityMetrics
from utils.utilities import Utilities

from starlette.applications import Starlette
import uvicorn

app = Starlette(debug=True)

@app.route("/translate")
def translate():
    FHIRTranslation.translatePatient();

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
