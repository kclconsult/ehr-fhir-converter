import json, collections, sys, operator, re
from pprint import pprint
from xml.etree import ElementTree;

from EHR.SystmOne import SystmOne
from utils.utilities import Utilities
from translation.translationConstants import TranslationConstants
from translation.similarityMetrics import SimilarityMetrics
from translation.translationUtilities import TranslationUtilities
from translation.matches import Matches;

import models_subset.patient;

class FHIRTranslation(object):

    @staticmethod
    def getPatient(id):

        return ElementTree.parse('../../../resources/' + TranslationConstants.EHR_PATH + ( "-extract" if TranslationConstants.DEMO else "-full" ) + '.xml').find(TranslationConstants.EHR_ENTRY_POINT);

    @staticmethod
    def dataTypeCompatible(ehrChild, fhirChild, fhirClass):

        if re.match(TranslationConstants.TYPES_TO_REGEX[TranslationUtilities.getFHIRClassChildType(fhirChild, fhirClass)], ehrChild):

            return True;

        else:

            return False;

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
        fhirClassesToChildren = FHIRTranslation.getFHIRClassesToChildren(TranslationUtilities.getFHIRClasses(True));

        # Remove EHR classes and FHIR classes that do not have children (typically 'type' classes in FHIR).
        ehrClasses = set(ehrClassesToChildren.keys());
        fhirClasses = fhirClassesToChildren.keys();

        candidateEntryPoints = [];
        classesExamined = 0;

        totalChildren = len(set(set().union(*ehrClassesToChildren.values())));

        if (TranslationConstants.DEMO): fhirClasses = [models_subset.patient.Patient];

        for fhirClass in fhirClasses:

            if (TranslationConstants.DEMO): print "FHIR class: " + str(fhirClass);

            placed = [];
            usedFHIRClassesForPlacement = set();
            hops = -1;
            totalStrength = 0;

            for ehrClass in ehrClasses:

                for ehrChild in ehrClassesToChildren[ehrClass]:

                    if (TranslationConstants.DEMO): print "  EHR child: " + str(ehrChild);

                    # Getting all potential placements allows us to select more than just the top match, should we want to, such as to handle the instance in which two EHR leaves map to the same FHIR leaf.
                    potentialPlacements = FHIRTranslation.recursivelyPlaceEHRchild(fhirClass, fhirClassesToChildren, fhirConnections, ehrClass, ehrChild, 0, [], []);

                    if ( potentialPlacements and len(potentialPlacements) ):

                        # Sort EHRchild:FHIRchild matches by strength and hops
                        sortedPlacements = sorted(potentialPlacements, key=operator.itemgetter(2, 3));
                        sortedPlacements.reverse();

                        # Get hops of strongest match
                        hops += sortedPlacements[0][3];

                        # Get the FHIR class used for the strongest match
                        usedFHIRClassesForPlacement.add(sortedPlacements[0][1]);

                        # Map EHR information to all the details of the strongest match.
                        placed.append(((ehrChild, ehrClass), sortedPlacements[0]));

            if ( len(placed) > 0 ): candidateEntryPoints.append((fhirClass, ( len(placed) / float(totalChildren) ), hops, "Average hops: " + str( hops / float(len(placed)) ), "Classes used: " + str(len(set(usedFHIRClassesForPlacement))),  placed));

            if len(placed) == totalChildren: break;

            classesExamined += 1;

            print str((classesExamined / float(len(fhirClasses))) * 100) + "%";

        for entry in sorted(candidateEntryPoints, key = operator.itemgetter(1, 2)):
            print str(entry) + "\n";

    @staticmethod
    def recursivelyPlaceEHRchild(fhirClass, fhirClassesToChildren, fhirConnections, ehrParent, ehrChild, hops, visited, potentialPlacements, alsoParentStrength=False, alsoMatchParent=False):

        visited.append(fhirClass);

        hops += 1;

        for fhirChild in fhirClassesToChildren[fhirClass]:

            if ( not alsoMatchParent or Matches.fuzzyMatch(ehrParent, fhirClass.__name__) > TranslationConstants.FUZZY_SIMILARITY_THRESHOLD ) \
            and Matches.matches( \
                ehrChild, fhirChild[0], \
                TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, \
                TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, \
                TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD \
            ) \
            and FHIRTranslation.dataTypeCompatible(ehrChild, fhirChild[0], fhirChild[1]):

                matchStrength = Matches.matchStrength(
                    ehrChild, fhirChild[0]
                )

                if ( alsoParentStrength ):

                    matchStrength += Matches.fuzzyMatchStrength(
                        ehrParent, fhirClass.__name__
                    );

                if ( (fhirChild[0], fhirClass, matchStrength, hops) not in potentialPlacements):

                    potentialPlacements.append((fhirChild[0], fhirClass, matchStrength, hops));

        if ( fhirClass not in fhirConnections.keys() or ( hasattr(TranslationConstants, 'MAX_HOPS') and hops >= TranslationConstants.MAX_HOPS  ) ): return None;

        for connectedResource in fhirConnections[fhirClass]:

            if connectedResource[0] not in visited:

                FHIRTranslation.recursivelyPlaceEHRchild(connectedResource[0], fhirClassesToChildren, fhirConnections, ehrParent, ehrChild,  hops, visited, potentialPlacements, alsoParentStrength, alsoMatchParent);

        return potentialPlacements;
