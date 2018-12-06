import sys

from translation.FHIRTranslation import FHIRTranslation
from translation.matches import Matches
from translation.translationConstants import TranslationConstants
from translation.similarityMetrics import SimilarityMetrics
from utils.utilities import Utilities

if __name__ == "__main__":

    ft = FHIRTranslation();

    if len(sys.argv) == 2:
        ft.translatePatient(0, sys.argv[1]);

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

        ft.translatePatient(action, None, sys.argv[2], sys.argv[3]);

    else:
        FHIRTranslation.translatePatient();
