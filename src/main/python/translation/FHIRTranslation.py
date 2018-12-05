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
        # return SystmOne().getPatientRecord(id);
        return TranslationUtilities.ehrClassToExamples(ElementTree.parse('../../../resources/' + TranslationConstants.EHR_PATH + '.xml').find("Response"));

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

            children = TranslationUtilities.getEHRClassChildren(patientXML, ehrClass, True, False);
            if len(children):
                ehrClassesToChildren = Utilities.mergeDicts([ehrClassesToChildren, children]);

        # Map each FHIR class not only to its own children, but also the children of its backbone elements.
        fhirClassesToChildren = FHIRTranslation.getFHIRClassesToChildren(TranslationUtilities.getFHIRClasses(True), False);

        # Remove EHR classes and FHIR classes that do not have children (typically 'type' classes in FHIR).
        ehrClasses = set(ehrClassesToChildren.keys());
        fhirClasses = fhirClassesToChildren.keys();

        candidateEntryPoints = [];
        classesExamined = 0;

        for fhirClass in fhirClasses:

            classesExamined += 1;
            print str((classesExamined / float(len(fhirClasses))) * 100) + "%";

            placedEHRChildrenInThisClassOrConnected = 0;
            placed = [];
            hops = -1;

            for ehrClass in ehrClasses:

                for ehrChild in ehrClassesToChildren[ehrClass]:

                    placement = FHIRTranslation.recursivelyPlaceEHRchild(fhirClass, fhirClassesToChildren, fhirConnections, ehrChild, 0, []);

                    if ( placement ):
                        placedEHRChildrenInThisClassOrConnected += 1;
                        hops += placement[2];
                        placed.append((ehrChild, placement));

            candidateEntryPoints.append((fhirClass, (placedEHRChildrenInThisClassOrConnected / float(len(set(set().union(*ehrClassesToChildren.values()))))), hops, placed));

            if placedEHRChildrenInThisClassOrConnected == len(set(set().union(*ehrClassesToChildren.values()))): break;

        print sorted(candidateEntryPoints, key = operator.itemgetter(1, 2));

    @staticmethod
    def recursivelyPlaceEHRchild(fhirClass, fhirClassesToChildren, fhirConnections, ehrChild, hops, visited):

        visited.append(fhirClass);

        hops += 1;

        for fhirChild in fhirClassesToChildren[fhirClass]:

            if Matches.matches(fhirChild, ehrChild, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD) and FHIRTranslation.dataTypeCompatible("", ""):

                return (fhirChild, fhirClass, hops);

        for connectedResource in fhirConnections:

            connectedResourceResult = "";

            if connectedResource not in visited:

                connectedResourceResult = FHIRTranslation.recursivelyPlaceEHRchild(connectedResource, fhirClassesToChildren, fhirConnections, ehrChild,  hops, visited);

            if ( connectedResourceResult ): return connectedResourceResult;

        return None;
