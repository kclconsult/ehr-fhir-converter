import sys

from translation.FHIRTranslation import FHIRTranslation
from translation.matches import Matches
from translation.translationConstants import TranslationConstants
from translation.similarityMetrics import SimilarityMetrics
from utils.utilities import Utilities

if __name__ == "__main__":

    ft = FHIRTranslation();

    FHIRTranslation.translatePatient();
