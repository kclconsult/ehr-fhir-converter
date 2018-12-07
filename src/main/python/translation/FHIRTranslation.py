import json, collections, sys, operator
from pprint import pprint
from xml.etree import ElementTree;

from EHR.SystmOne import SystmOne
from utils.utilities import Utilities
from translation.translationConstants import TranslationConstants
from translation.similarityMetrics import SimilarityMetrics
from translation.translationUtilities import TranslationUtilities
from translation.matches import Matches;

import models_subset;

class FHIRTranslation(object):

    @staticmethod
    def dataTypeCompatible(ehrData, expression):
        return True;

    @staticmethod
    def getFHIRClassesToChildren(fhirClasses=TranslationUtilities.getFHIRClasses(), linkedClasses=True, fhirClassesRecurse=True, selectiveRecurse=TranslationConstants.SELECTIVE_RECURSE, includesBackboneElements=True, mergeMainChildrenWithBackboneChildren=True):

        fhirClassesToChildren = {};

        if (includesBackboneElements and mergeMainChildrenWithBackboneChildren):

            for fhirClassAndBackboneElements in fhirClasses:

                fhirClass = fhirClassAndBackboneElements[0];

                for fhirClassOrBackboneElement in fhirClassAndBackboneElements:

                    children = TranslationUtilities.getFHIRClassChildren(fhirClassOrBackboneElement, linkedClasses, fhirClassesRecurse, selectiveRecurse);

                    if ( children != None ): fhirClassesToChildren.setdefault(fhirClass, []).extend(children)

        else:

            if ( not mergeMainChildrenWithBackboneChildren ): fhirClasses = Utilities.mergeListOfLists(fhirClasses);

            for fhirClass in fhirClasses:

                children = TranslationUtilities.getFHIRClassChildren(fhirClass, linkedClasses, fhirClassesRecurse, selectiveRecurse);

                if ( children != None ): fhirClassesToChildren[fhirClass] = children;

        return fhirClassesToChildren;

    @staticmethod
    def getPatient(id):
        #return TranslationUtilities.ehrClassToExamples(ElementTree.parse('../../../resources/' + TranslationConstants.EHR_PATH + '.xml').find("Response"));
        return ElementTree.parse('../../../resources/' + TranslationConstants.EHR_PATH + '.xml').find("Response");

    import models_subset.patient;

    @staticmethod
    def translatePatient():

         # Get patient record from EHR
        patientXML = FHIRTranslation.getPatient("4917111072");

        ehrClasses = TranslationUtilities.getEHRClasses(patientXML);

        if not len(ehrClasses): return;

        # Get fhirClasses
        fhirClasses = TranslationUtilities.getFHIRClasses();

        # Get incoming and outgoing connections to each FHIR class (differs from children).
        fhirConnections = TranslationUtilities.getFHIRConnections(fhirClasses);

        # Prepare lists of classes and children.
        ehrClassesToChildren = {};

        for ehrClass in ehrClasses:

            children = TranslationUtilities.getEHRClassChildren(patientXML, ehrClass, True, False, True);

            if len(children): ehrClassesToChildren = Utilities.mergeDicts([ehrClassesToChildren, children]);

        # Map each FHIR class not only to its own children, but also the children of its backbone elements.
        fhirClassesToChildren = FHIRTranslation.getFHIRClassesToChildren(TranslationUtilities.getFHIRClasses(True), False);

        # Remove EHR classes and FHIR classes that do not have children (typically 'type' classes in FHIR).
        ehrClasses = set(ehrClassesToChildren.keys());
        fhirClasses = fhirClassesToChildren.keys();

        candidateEntryPoints = [];
        classesExamined = 0;

        for fhirClass in fhirClasses:

            placedEHRChildrenInThisClassOrConnected = 0;
            placed = [];
            usedFHIRClassesForPlacement = set();
            hops = -1;

            for ehrClass in ehrClasses:

                for ehrChild in ehrClassesToChildren[ehrClass]:

                    placement = FHIRTranslation.recursivelyPlaceEHRchild(False, fhirClass, fhirClassesToChildren, fhirConnections, ehrClass, ehrChild, 0, []);

                    if ( placement ):
                        placedEHRChildrenInThisClassOrConnected += 1;
                        hops += placement[2];
                        usedFHIRClassesForPlacement.add(placement[1]);
                        placed.append(((ehrChild, ehrClass), placement));

            if ( placedEHRChildrenInThisClassOrConnected > 0 ): candidateEntryPoints.append((fhirClass, ( placedEHRChildrenInThisClassOrConnected / float(len(set(set().union(*ehrClassesToChildren.values())))) ), str(hops), "Average hops: " + str( hops / float(placedEHRChildrenInThisClassOrConnected) ), "Classes used: " + str(len(set(usedFHIRClassesForPlacement))), placed));

            if placedEHRChildrenInThisClassOrConnected == len(set(set().union(*ehrClassesToChildren.values()))): break;

            classesExamined += 1;

            print str((classesExamined / float(len(fhirClasses))) * 100) + "%";

        for entry in sorted(candidateEntryPoints, key = operator.itemgetter(1, 2)):
            print str(entry) + "\n";

    @staticmethod
    def recursivelyPlaceEHRchild(alsoMatchParent, fhirClass, fhirClassesToChildren, fhirConnections, ehrParent, ehrChild, hops, visited):

        visited.append(fhirClass);

        hops += 1;

        strongestMatch = -sys.maxint -1
        strongestMatchDetails = None;

        for fhirChild in fhirClassesToChildren[fhirClass]:

            if ( not alsoMatchParent or Matches.fuzzyMatch(ehrParent, fhirClass.__name__) > TranslationConstants.FUZZY_SIMILARITY_THRESHOLD ) and Matches.matches(fhirChild, ehrChild, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD) and FHIRTranslation.dataTypeCompatible("", ""):

                matchStrength = Matches.match(ehrChild, fhirChild, SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [], TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);

                if ( matchStrength > strongestMatch ):

                    strongestMatch = matchStrength;
                    strongestMatchDetails = (fhirChild, fhirClass, hops);

        if ( strongestMatchDetails ): return strongestMatchDetails;

        if ( fhirClass not in fhirConnections.keys() or hops >= TranslationConstants.MAX_HOPS ): return None;

        for connectedResource in fhirConnections[fhirClass]:

            if connectedResource[0] not in visited:

                return FHIRTranslation.recursivelyPlaceEHRchild(alsoMatchParent, connectedResource[0], fhirClassesToChildren, fhirConnections, ehrParent, ehrChild,  hops, visited);

        return None;
