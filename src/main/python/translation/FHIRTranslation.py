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
    def childSimilarity(ehrClass, fhirClass, ehrClassesToChildren=None, fhirClassesToChildren=None, xml=None, linkedClasses=False, selectiveRecurse=TranslationConstants.SELECTIVE_RECURSE):

        if ( ehrClassesToChildren ):
            ehrClassChildren = ehrClassesToChildren[ehrClass];
        else:
            ehrClassChildren = TranslationUtilities.getEHRClassChildren(xml, ehrClass)[ehrClass]; #~MDC TODO: Deal with the fact that this now returns a dictionary.

        if ( fhirClassesToChildren ):
            fhirClassChildren = fhirClassesToChildren[fhirClass];
        else:
            fhirClassChildren = TranslationUtilities.getFHIRClassChildren(fhirClass, linkedClasses, selectiveRecurse);

        if ( fhirClassChildren == None ): return 0;

        # Because the same FHIR class field may be a candidate for more than one EHR attribute, and we cannot accommodate more than one attribute in a field, we keep track of these multiple matches, so as to only count them once in our total child matches, and to pick the strongest match for our strength indications.
        fhirMatchCandidates = {};

        for fhirClassChild in fhirClassChildren: fhirMatchCandidates[fhirClassChild] = [];

        # For each child of the EHR parent (can also includes ATTRIBUTES (same tag) of EHR parent and children).
        for ehrClassChild in ehrClassChildren:

            highestMatchStrength = 0;
            highestFHIRClassChildMatch = "";

            # Look at that FHIR classes children
            for fhirClassChild in fhirClassChildren:

                if ( linkedClasses ):
                    fhirClassChildForMatch = fhirClassChild[0];
                else:
                    fhirClassChildForMatch = fhirClassChild;

                # Compare all FHIR class children to each child of this EHR class, and find the most that match in order to resolve multiple potential class matches.
                if Matches.matches(ehrClassChild, fhirClassChildForMatch, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD) and FHIRTranslation.dataTypeCompatible("", ""):

                    # To identify raw match strength, we want to look at the combined results of all the metrics without any thresholds.
                    matchStrength = Matches.match(ehrClassChild, fhirClassChildForMatch, SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [], TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);

                    #matchStrength = FHIRTranslation.match(ehrClassChild, fhirClassChild[0], TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, False);

                    #print str(ehrClassChild) + " " + str(fhirClassChild) + " " + str(matchStrength);

                    # If the EHR child and FHIR child are linked by the name of the EHR parent, this should affect the match strength. E.g. Medication (EHR parent) in MedicationType (EHR Child) and medicationReference (FHIR child)
                    if ehrClass.lower() in ehrClassChild.lower() and ehrClass.lower() in fhirClassChild[0].lower():
                         matchStrength = matchStrength * TranslationConstants.CONTEXT_WEIGHTING;

                    if matchStrength > highestMatchStrength:
                        highestMatchStrength = matchStrength;
                        highestFHIRClassChildMatch = fhirClassChild;

            if highestFHIRClassChildMatch in fhirMatchCandidates.keys():

                # If there are other children in the EHR that are most related to this highest matching FHIR attribute.
                if len(fhirMatchCandidates[highestFHIRClassChildMatch]) > 0:

                    # If the strength of correspondence between this EHR attribute and that FHIR attribute is stronger than all the others (everything in this list has the same strength, so we access position 0, and then position 1 for the strength (position 0 the ehr child name)).
                    if highestMatchStrength >= fhirMatchCandidates[highestFHIRClassChildMatch][0][1]:

                        # If it's greater, clear the list.
                        if highestMatchStrength > fhirMatchCandidates[highestFHIRClassChildMatch][0][1]:
                            del fhirMatchCandidates[highestFHIRClassChildMatch][:];

                    # If it's greater a new individual entry to the recently cleared list. If it's the same, add another entry to this list.
                    fhirMatchCandidates[highestFHIRClassChildMatch].append((ehrClassChild, highestMatchStrength));

                # Otherwise record this new match.
                else:
                    fhirMatchCandidates[highestFHIRClassChildMatch].append((ehrClassChild, highestMatchStrength));

        # Post-processing candidates:

        totalChildMatches = 0;
        # Because the number of matches isn't the only thing that's important, it's the accuracy of those matches.
        totalMatchStrength = 0;

        for fhirMatchCandidate in fhirMatchCandidates:

            if len(fhirMatchCandidates[fhirMatchCandidate]) > 0:

                # If there are multiple EHR children matches to a FHIR attribute with the same strength, then only one of them can be accommodated, so only increment by 1.
                totalChildMatches += 1;

                # All items in list have same strength, so just use first item.
                totalMatchStrength += fhirMatchCandidates[fhirMatchCandidate][0][1];

        #print fhirMatchCandidates;

        if ( totalChildMatches > 0 ):

            averageMatchStrength = totalMatchStrength / float(totalChildMatches);

            #print str(totalChildMatches) + " " + str(totalChildMatches / float(len(ehrClassChildren))) + " " + str(averageMatchStrength) + " " + str(len(fhirClassChildren)) + " " + str(min(len(ehrClassChildren) / float(len(fhirClassChildren)), 1)) + " " + str((totalChildMatches / float(len(ehrClassChildren))) * averageMatchStrength);
            # How many matches have been found for the EHR elements in the candidate FHIR class (weighted by match strength, and by the specificity of the class).
            return ((totalChildMatches / float(len(ehrClassChildren))) * averageMatchStrength) # * min(len(ehrClassChildren) / float(len(fhirClassChildren)), 1);

        else:
            return 0;

    @staticmethod
    def getPatient(id):
        # return SystmOne().getPatientRecord(id);
        return TranslationUtilities.ehrClassToExamples(ElementTree.parse('../../../resources/' + TranslationConstants.EHR_PATH + '.xml').find("Response"));

    @staticmethod
    def translatePatient(action=None, ehrClass=None, ehrClassChild=None, fhirClassChild=None, fhirClass=None):

         # Get patient record from EHR
        patientXML = FHIRTranslation.getPatient("4917111072");

        ehrClasses = {};

        if ( action == 0 and ehrClass ):
            ehrClasses = { ehrClass };

        elif ( action == 1 and ehrClassChild and fhirClassChild ):
            print "Checking match strength."
            print FHIRTranslation.match(ehrClassChild, fhirClassChild,  TranslationConstants.TEXT_SIMILARITY_WEIGHTING,  TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);

        elif ( action == 2 and ehrClassChild and fhirClassChild ):
            print "Checking for match value (if matches)."
            print FHIRTranslation.match(ehrClassChild, fhirClassChild, TranslationConstants.TEXT_SIMILARITY_WEIGHTING,  TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.MORPHOLOGICAL_SIMILARITY_WEIGHTING, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, True, False, True);

        elif ( action == 3 and ehrClassChild and fhirClassChild ):
            print "Checking if matches."
            print FHIRTranslation.matches(ehrClassChild, fhirClassChild, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, True);

        elif ( action == 4 and ehrClassChild and fhirClassChild ):
            print "Checking semantic similarity."
            print SimilarityMetrics.semanticSimilarity(ehrClassChild, fhirClassChild);

        elif ( action == 5 and ehrClassChild and fhirClassChild ):
            print "Checking morphological similarity."
            print SimilarityMetrics.morphologicalSimilarity(ehrClassChild, fhirClassChild);

        elif ( action == 6 and ehrClass and fhirClass ):
            print "Checking child similarity."
            print FHIRTranslation.childSimilarity(ehrClass, fhirClass, None, None, FHIRTranslation.getPatient("4917111072"));

        else:

            ehrClasses = TranslationUtilities.getEHRClasses(patientXML);

        if (len(ehrClasses)): FHIRTranslation.translatePatientInit(ehrClasses, patientXML, True, TranslationConstants.SELECTIVE_RECURSE);

    @staticmethod
    def getFHIRClassesToChildren(fhirClasses=TranslationUtilities.getFHIRClasses(), fhirClassesRecurse=True, selectiveRecurse=TranslationConstants.SELECTIVE_RECURSE, includesBackboneElements=False, mergeMainChildrenWithBackboneChildren=False):

        fhirClassesToChildren = {};

        if (includesBackboneElements and mergeMainChildrenWithBackboneChildren):

            for fhirClassAndBackboneElements in fhirClasses:

                fhirClass = fhirClassAndBackboneElements[0];

                for fhirClassOrBackboneElement in fhirClassAndBackboneElements:

                    children = TranslationUtilities.getFHIRClassChildren(fhirClassOrBackboneElement, fhirClassesRecurse, selectiveRecurse);

                    if ( children != None ): fhirClassesToChildren.setdefault(fhirClass, []).extend(children)

        else:

            if ( not mergeMainChildrenWithBackboneChildren ): fhirClasses = Utilities.mergeListOfLists(fhirClasses);

            for fhirClass in fhirClasses:

                children = TranslationUtilities.getFHIRClassChildren(fhirClass, fhirClassesRecurse, selectiveRecurse);

                if ( children != None ): fhirClassesToChildren[fhirClass] = children;

        return fhirClassesToChildren;

    @staticmethod
    def translatePatientInit(ehrClasses, patientXML, fhirClassesRecurse, selectiveRecurse):

        # Get fhirClasses
        fhirClasses = TranslationUtilities.getFHIRClasses();

        # Get incoming and outgoing connections to each FHIR class (differs from children).
        fhirConnections = TranslationUtilities.getFHIRConnections(fhirClasses);

        # Prepare lists of classes and children.
        ehrClassesToChildren = {};

        # Get outgoing connections of each ehrClass.
        ehrClassesToParents = {}

        for ehrClass in ehrClasses:

            children = TranslationUtilities.getEHRClassChildren(patientXML, ehrClass, True, False);
            if len(children):
                ehrClassesToChildren = Utilities.mergeDicts([ehrClassesToChildren, children]);

            parents = TranslationUtilities.getEHRClassChildren(patientXML, ehrClass, False, True);
            if len(parents):
                ehrClassesToParents = Utilities.mergeDicts([ehrClassesToParents, parents]);

        # Map each FHIR class not only to its own children, but also the children of its backbone elements.
        fhirClassesToChildren = FHIRTranslation.getFHIRClassesToChildren(TranslationUtilities.getFHIRClasses(True), True, selectiveRecurse, True, True);

        # Remove EHR classes and FHIR classes that do not have children (typically 'type' classes in FHIR).
        ehrClasses = set(ehrClassesToChildren.keys());
        fhirClasses = fhirClassesToChildren.keys();

        FHIRTranslation.matchStageOne(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, fhirClassesRecurse);

    # Match stage 1: Exact FHIR terms that are contained in the EHR term
    @staticmethod
    def matchStageOne(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, fhirClassesRecurse):

        # Match components of patient record from EHR to components from JSON representation
        ehrFHIRMatches = {};

        ehrClassesToRemove = set();

        for ehrClass in ehrClasses:

            matches = 0;

            for fhirClass in fhirClasses:

                if SimilarityMetrics.compositeStringSimilarity(ehrClass, str(fhirClass.__name__), SimilarityMetrics.textSimilarity, [], True) == 1.0:
                    matches += 1;
                    fhirMatch = fhirClass;

            # If there is only one 100% match between an EHR Class and FHIR Class, we take this as the best candidate, and remove the EHR class from the pool.
            if matches == 1:
                ehrFHIRMatches[ehrClass] = { fhirMatch: FHIRTranslation.childSimilarity(ehrClass, fhirMatch, ehrClassesToChildren, fhirClassesToChildren, None, fhirClassesRecurse) };
                ehrClassesToRemove.add(ehrClass);

        FHIRTranslation.matchStageTwo(ehrClassesToRemove, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, fhirClassesRecurse);

    # Match Stage 2: Child matches
    @staticmethod
    def matchStageTwo(ehrClassesToRemove, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, fhirClassesRecurse):

        for ehrClass in ehrClassesToChildren.keys():

            if ehrClass in ehrClassesToRemove: continue;

            ehrFHIRMatches[ehrClass] = {};

            childMatches = [];

            for fhirClass in fhirClasses:

                childSimilarity = FHIRTranslation.childSimilarity(ehrClass, fhirClass, ehrClassesToChildren, fhirClassesToChildren, None, True, fhirClassesRecurse);

                childMatches.append((fhirClass, childSimilarity));

            childMatches = sorted(childMatches, key=lambda sortable: (sortable[1]), reverse=True);

            for childMatch in childMatches:

                if ( childMatch[1] > TranslationConstants.CHILD_MATCH_THRESHOLD ):
                    ehrFHIRMatches[ehrClass][childMatch[0]] = childMatch[1];

            # print str(ehrClass) + " " + str(childMatches);

            # If there are no candidates for an ehrClass based on child matches (i.e. none of the matches are above the threshold), then choose the highest.
            if len(ehrFHIRMatches[ehrClass]) == 0:

                # As the list of child matches is sorted, the first in the list is the highest.
                firstChildMatch = childMatches[0];
                highestMatch = firstChildMatch[1];
                ehrFHIRMatches[ehrClass][firstChildMatch[0]] = firstChildMatch[1];

                # Skip the match that has just been added.
                iterChildMatches = iter(childMatches);
                next(iterChildMatches);

                # Add any equally high matches.
                for childMatch in iterChildMatches:
                    if ( childMatch[1] == highestMatch ):
                        ehrFHIRMatches[ehrClass][childMatch[0]] = childMatch[1];
                    else:
                        break;

        FHIRTranslation.matchStageThree(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches);

    # Match Stage 3: Fuzzy parent matches
    @staticmethod
    def matchStageThree(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches):

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

        FHIRTranslation.matchStageFour(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches);

    # Match Stage 4: Replicating connections
    @staticmethod
    def matchStageFour(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches):

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

        FHIRTranslation.matchStageFive(ehrFHIRMatches, ehrClassesToChildren, fhirClassesToChildren, ehrFHIRCommonConnections);

    # Match Stage 5: Match EHR children to FHIR children from chosen class (and print results).
    @staticmethod
    def matchStageFive(ehrFHIRMatches, ehrClassesToChildren, fhirClassesToChildren, ehrFHIRCommonConnections):

        # Handle two EHR classes matching to the same FHIR class. OK if they don't have overlapping fields.
        for ehrClass in ehrFHIRMatches:

            print "===========================";
            print ehrClass;

            if len(ehrFHIRMatches[ehrClass]):

                for fhirClass, matchScore in ehrFHIRMatches[ehrClass].iteritems():

                    if ehrClass not in ehrFHIRCommonConnections.keys() or fhirClass not in ehrFHIRCommonConnections[ehrClass].keys(): continue;

                    ehrFHIRMatches[ehrClass][fhirClass] = ehrFHIRMatches[ehrClass][fhirClass] + ehrFHIRCommonConnections[ehrClass][fhirClass];

                ehrFHIRMatchesSorted = sorted(ehrFHIRMatches[ehrClass].items(), key=operator.itemgetter(1));
                ehrFHIRMatchesSorted.reverse();

                print ehrFHIRMatchesSorted;

                # Get a list of the FHIR children of the top FHIR match.
                children = fhirClassesToChildren[ehrFHIRMatchesSorted[0][0]]; # [:]

                ehrChildToHighestFHIRchild = {};

                # Now find matches for each child (non-parent; leaf) of this EHR class.
                for ehrChild in ehrClassesToChildren[ehrClass]:

                    # For this EHR child derive a match strength for each FHIR child of the matched FHIR class, a select the highest.
                    for fhirChild in children:

                        # Each FHIR child is a tuple with parent as second value. Parameters here enable a different matching configuration for child matches.
                        matchStrength = Matches.match(ehrChild, fhirChild[0], SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [], TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True)

                        # If we don't yet have a suggested FHIR child match for this EHR child, or we have a stronger match, record this.
                        if ( ehrChild not in ehrChildToHighestFHIRchild or matchStrength > ehrChildToHighestFHIRchild[ehrChild][0] ):
                            ehrChildToHighestFHIRchild[ehrChild] = (matchStrength, fhirChild);

                print ehrChildToHighestFHIRchild;

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
