import json, collections, sys, operator
from pprint import pprint
from xml.etree import ElementTree;
from munkres import Munkres;

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
    def getFHIRClassesToChildren(fhirClasses=TranslationUtilities.getFHIRClasses(), linkedClasses=True, selectiveRecurse=TranslationConstants.SELECTIVE_RECURSE, fhirClassesRecurse=True, includesBackboneElements=True, mergeMainChildrenWithBackboneChildren=True):

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

        for fhirClass in fhirClasses:

            print " =======Candidate FHIR class=========== "
            print fhirClass;

            placedEHRChildrenInThisClassAndConnected = 0;
            placed = [];

            for ehrChild in set(set().union(*ehrClassesToChildren.values())):

                ## ORDER CANDIDATE FHIR CLASSES BY SIMILARITY TO EHR PARENT

                placement = FHIRTranslation.recursivelyPlaceEHRchild(fhirClass, fhirClassesToChildren, fhirConnections, ehrChild, 0, []);

                if ( placement ):
                    placedEHRChildrenInThisClassAndConnected += 1;
                    placed.append((ehrChild, placement));

            print "Placed: " + str(placedEHRChildrenInThisClassAndConnected) + " out of " + str(len(set(set().union(*ehrClassesToChildren.values()))));
            print placed;
            print set(set().union(*ehrClassesToChildren.values()));
            print " ================================ "

            if placedEHRChildrenInThisClassAndConnected == len(set(set().union(*ehrClassesToChildren.values()))):

                break;

    @staticmethod
    def recursivelyPlaceEHRchild(fhirClass, fhirClassesToChildren, fhirConnections, ehrChild, hops, visited):

        visited.append(fhirClass);

        for fhirChild in fhirClassesToChildren[fhirClass]:

            if Matches.matches(fhirChild.__name__, ehrChild, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD) and FHIRTranslation.dataTypeCompatible("", ""):

                return str(fhirClass) + " " + str(fhirChild) + " " + str(hops);

        hops += 1;

        for connectedResource in fhirConnections:

            connectedResourceResult = "";

            if connectedResource not in visited:

                connectedResourceResult = FHIRTranslation.recursivelyPlaceEHRchild(connectedResource, fhirClassesToChildren, fhirConnections, ehrChild,  hops, visited);

            if ( connectedResourceResult ): return connectedResourceResult;

        return None;

    # Match stage 1: Exact FHIR terms that are contained in the EHR term
    @staticmethod
    def matchStageOne(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections):

        # Match components of patient record from EHR to components from JSON representation
        ehrFHIRMatches = {};
        # Details below.
        ehrFHIRMatchChildConfiguration = {};

        ehrClassesToRemove = set();

        for ehrClass in ehrClasses:

            matches = 0;

            for fhirClass in fhirClasses:

                if SimilarityMetrics.compositeStringSimilarity(ehrClass, str(fhirClass.__name__), SimilarityMetrics.textSimilarity, [], True) == 1.0:
                    matches += 1;
                    fhirMatch = fhirClass;

            # If there is only one 100% match between an EHR Class and FHIR Class, we take this as the best candidate, and remove the EHR class from the pool.
            if matches == 1:
                childSimilarity = FHIRTranslation.childSimilarity(ehrClass, fhirMatch, ehrClassesToChildren, fhirClassesToChildren)
                ehrFHIRMatches[ehrClass] = { fhirMatch: childSimilarity[0] };
                ehrFHIRMatchChildConfiguration[ehrClass] = { fhirMatch: childSimilarity[1] };
                ehrClassesToRemove.add(ehrClass);

        FHIRTranslation.matchStageTwo(ehrClassesToRemove, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, ehrFHIRMatchChildConfiguration);

    # Match Stage 2: Child matches
    @staticmethod
    def matchStageTwo(ehrClassesToRemove, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, ehrFHIRMatchChildConfiguration):

        for ehrClass in ehrClassesToChildren.keys():

            if ehrClass in ehrClassesToRemove: continue;

            # We're going to record the potential FHIR matches for this EHR class AND the matched FHIR children that lead to this FHIR class being listed as a potential match.
            ehrFHIRMatches[ehrClass] = {};
            ehrFHIRMatchChildConfiguration[ehrClass] = {};

            childMatches = [];

            for fhirClass in fhirClasses:

                childSimilarity = FHIRTranslation.childSimilarity(ehrClass, fhirClass, ehrClassesToChildren, fhirClassesToChildren);

                childMatches.append((fhirClass, childSimilarity));

            childMatches = sorted(childMatches, key=lambda sortable: (sortable[1][0]), reverse=True);

            for childMatch in childMatches:

                if ( childMatch[1][0] > TranslationConstants.CHILD_MATCH_THRESHOLD ):
                    # Extract different parts of what is returned from the childSimilarity function (match strength and child configuration).
                    ehrFHIRMatches[ehrClass][childMatch[0]] = childMatch[1][0];
                    ehrFHIRMatchChildConfiguration[ehrClass][childMatch[0]] = childMatch[1][1];

            # If there are no candidates for an ehrClass based on child matches (i.e. none of the matches are above the threshold), then choose the highest.
            if len(ehrFHIRMatches[ehrClass]) == 0:

                # As the list of child matches is sorted, the first in the list is the highest.
                firstChildMatch = childMatches[0];
                highestMatch = firstChildMatch[1][0];
                ehrFHIRMatches[ehrClass][firstChildMatch[0]] = firstChildMatch[1][0];
                ehrFHIRMatchChildConfiguration[ehrClass][firstChildMatch[0]] = firstChildMatch[1][1];

                # Skip the match that has just been added.
                iterChildMatches = iter(childMatches);
                next(iterChildMatches);

                # Add any equally high matches.
                for childMatch in iterChildMatches:
                    if ( childMatch[1][0] == highestMatch ):
                        ehrFHIRMatches[ehrClass][childMatch[0]] = childMatch[1][0];
                        ehrFHIRMatchChildConfiguration[ehrClass][childMatch[0]] = childMatch[1][1];
                    else:
                        break;

        FHIRTranslation.matchStageThree(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, ehrFHIRMatchChildConfiguration);

    # Match Stage 3: Fuzzy parent matches
    @staticmethod
    def matchStageThree(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, ehrFHIRMatchChildConfiguration):

        # Now decide between multiples matches based upon names of parent classes.
        for ehrClass in ehrFHIRMatches:

            # For each matching FHIR class to this EHR class
            for fhirClass, childSimilarity in ehrFHIRMatches[ehrClass].iteritems():

                ehrClassParent = ehrClass;

                # Remove the number from the end of our class (numbers used to signify EHR classes with non-intersecting children with the same name) for the purposes of this comparison.
                if Utilities.isNumber(ehrClass[len(ehrClass) - 1]): ehrClassParent = ehrClass[:-1];

                parentSimilarity = Matches.fuzzyMatch(ehrClassParent, fhirClass.__name__);

                # Add the parent similarity to the child similarity to get an overall similarity value.
                ehrFHIRMatches[ehrClass][fhirClass] = childSimilarity + parentSimilarity;

        FHIRTranslation.matchStageFour(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, ehrFHIRMatchChildConfiguration);

    # Match Stage 4: Replicating connections
    @staticmethod
    def matchStageFour(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, ehrFHIRMatchChildConfiguration):

        ehrFHIRCommonConnections = {};

        for ehrClass in ehrClassesToParents.keys():

            for fhirClass in fhirClasses:

                if fhirClass in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;

                # Find situations in which an EHR class has a child (which is also a parent) and a FHIR class has a connection, and those two classes (child and connection) have been matched, thus connecting the EHR and FHIR classes. For example Event (EHR parent) links to ClinicalCode (EHR child, with children of its own) and Encounter (FHIR class A) links to Condition (FHIR class B). If ClinicalCode and Condition are matched (which they are), then the classes -- Event and Encounter -- are likely to have some connection (which they do). Assuming all of an EHR (EHRA) class's children have a FHIR representation, this process repeats, and in the best case identifies one FHIR class which connects to each of the FHIR classes that has been chosen as a child-match for EHRAs children (one-to-many).

                for ehrChild in ehrClassesToParents[ehrClass]:

                    if ehrChild in ehrFHIRMatches.keys():

                        if fhirClass not in fhirConnections.keys() or ehrClass not in ehrFHIRMatches.keys(): continue;

                        for connection in [fhirConnection[0] for fhirConnection in fhirConnections[fhirClass]]:

                            ehrFHIRMatchesSorted = sorted(ehrFHIRMatches[ehrChild].items(), key=operator.itemgetter(1));
                            ehrFHIRMatchesSorted.reverse();

                            # Sort for the top match (Position 0, FHIR match at subsequent position 0). Should probably consider other EHR-FHIR matches as common connection criteria, if they are as equally strong, not just the top.
                            if ehrFHIRMatchesSorted[0][0] == connection:

                                additionalConnections = len(TranslationUtilities.recreatableConnections(ehrChild, ehrClassesToParents[ehrClass], ehrFHIRMatches, fhirConnections))

                                if ehrClass not in ehrFHIRCommonConnections.keys(): ehrFHIRCommonConnections[ehrClass] = {};

                                # +1 for the first EHR-FHIR match, plus any resulting subsequent common connections.
                                if fhirClass in ehrFHIRCommonConnections[ehrClass].keys():
                                    ehrFHIRCommonConnections[ehrClass][fhirClass] = ehrFHIRCommonConnections[ehrClass][fhirClass] + ( 1 + additionalConnections );

                                else:
                                    ehrFHIRCommonConnections[ehrClass][fhirClass] = ( 1 + additionalConnections );

        FHIRTranslation.matchStageFive(ehrFHIRMatches, ehrClassesToChildren, fhirClassesToChildren, ehrFHIRCommonConnections, ehrFHIRMatchChildConfiguration);

    # Match Stage 5: Match EHR children to FHIR children from chosen class (and print results).
    @staticmethod
    def matchStageFive(ehrFHIRMatches, ehrClassesToChildren, fhirClassesToChildren, ehrFHIRCommonConnections, ehrFHIRMatchChildConfiguration, addCommonConnections=True):

        for ehrClass in ehrFHIRMatches:

            print "===========================";
            print ehrClass;

            if len(ehrFHIRMatches[ehrClass]):

                if ( addCommonConnections ):

                    for fhirClass, matchScore in ehrFHIRMatches[ehrClass].iteritems():

                        if ehrClass not in ehrFHIRCommonConnections.keys() or fhirClass not in ehrFHIRCommonConnections[ehrClass].keys(): continue;

                        # Add common connections to existing match score.
                        ehrFHIRMatches[ehrClass][fhirClass] = ehrFHIRMatches[ehrClass][fhirClass] + ehrFHIRCommonConnections[ehrClass][fhirClass];

                ehrFHIRMatchesSorted = sorted(ehrFHIRMatches[ehrClass].items(), key=operator.itemgetter(1));
                ehrFHIRMatchesSorted.reverse();

                print ehrFHIRMatchesSorted;

                # Print the priorly computed EHR child to FHIR child matches for this top FHIR match.
                print ehrFHIRMatchChildConfiguration[ehrClass][ehrFHIRMatchesSorted[0][0]];

            print "===========================";

        # Replace values in JSON version of matching classes.
        # Utilities.getReplaceJSONKeys(patientJSON, None, list(), 'id', 'abc');

        # return.
        # return patientJSON

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
