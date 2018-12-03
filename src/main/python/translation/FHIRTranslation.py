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
    def childSimilarity(ehrClass, fhirClass, ehrClassesToChildren=None, fhirClassesToChildren=None, xml=None, linkedClasses=True, recurse=True, selectiveRecurse=TranslationConstants.SELECTIVE_RECURSE, allStrengths=False):

        if ( ehrClassesToChildren ):
            ehrClassChildren = ehrClassesToChildren[ehrClass];
        else:
            ehrClassChildren = TranslationUtilities.getEHRClassChildren(xml, ehrClass)[ehrClass]; #~MDC TODO: Deal with the fact that this now returns a dictionary.

        if ( fhirClassesToChildren ):
            fhirClassChildren = fhirClassesToChildren[fhirClass];
        else:
            fhirClassChildren = TranslationUtilities.getFHIRClassChildren(fhirClass, linkedClasses, recurse, selectiveRecurse);

        if ( fhirClassChildren == None ): return 0;

        # Because the same FHIR class field may be a candidate for more than one EHR attribute, and we cannot accommodate more than one attribute in a field, we keep track of these multiple matches, so as to only count them once in our total child matches, and to pick the strongest match for our strength indications.
        ehrChildrenToFHIRChildMatchCandidates = {};

        # Map each FHIR child child to a list of children fro mthe EHR that could match to it.
        # for fhirClassChild in fhirClassChildren: fhirMatchCandidates[fhirClassChild] = [];

        # For each child of the EHR parent (can also includes ATTRIBUTES (same tag) of EHR parent and children).
        for ehrClassChild in ehrClassChildren:

            # Look at this FHIR classes children
            for fhirClassChild in fhirClassChildren:

                # Extract the name of the child itself, if it is listed as a tuple with its parent.
                if ( linkedClasses ):
                    fhirClassChildForMatch = fhirClassChild[0];
                else:
                    fhirClassChildForMatch = fhirClassChild;

                # Compare all FHIR class children to each child of this EHR class, and record the strength of connection.
                if allStrengths or Matches.matches(ehrClassChild, fhirClassChildForMatch, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD) and FHIRTranslation.dataTypeCompatible("", ""):

                    # To identify raw match strength, we want to look at the combined results of all the metrics without any thresholds.
                    matchStrength = Matches.match(ehrClassChild, fhirClassChildForMatch, SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [], TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);

                    # If the EHR child and FHIR child are linked by the name of the EHR parent, this should affect the match strength. E.g. Medication (EHR parent) in MedicationType (EHR Child) and medicationReference (FHIR child)
                    if ehrClass.lower() in ehrClassChild.lower() and ehrClass.lower() in fhirClassChild[0].lower():
                         matchStrength = matchStrength * TranslationConstants.CONTEXT_WEIGHTING;

                    # Because the same children might be present from multiple recursed, connected classes.
                    if ( ehrClassChild in ehrChildrenToFHIRChildMatchCandidates.keys() and (fhirClassChild, matchStrength) in ehrChildrenToFHIRChildMatchCandidates[ehrClassChild] ): continue;

                    ehrChildrenToFHIRChildMatchCandidates.setdefault(ehrClassChild, []).append((fhirClassChild, matchStrength));

        # Maximise child matches based on strength, e.g.:
        # EHR1 = { FHIRA: 3, FHIRB: 2, FHIRC: 1 } = 1B (2)
        # EHR2 = { FHIRA: 4, FHIRB: 2, FHIRC: 7 } = 2A (4)
        # EHR3 = { FHIRA: 5, FHIRB: 4, FHIRC: 9 } = 3C (9)

        # Separate out the ehrChildrenToFHIRChildMatchCandidates dictionary for use with Munkres. Dcitionaries don't retain any order, which complicates things.
        ehrChildRowTitles = ehrChildrenToFHIRChildMatchCandidates.keys();

        # This will form the column names, with those EHR children (rows) that are not related to a given FHIR child being given a value of zero. This enables Munkres to operate correctly.
        allFHIRChildrenCandidatesAndParents = []

        for ehrChild in ehrChildRowTitles:

            # 0 is the child element of the tuple; second 0 is the child itself, rather than its recorded parent.
            allFHIRChildrenCandidatesAndParents.extend([childStrengthTuple[0] for childStrengthTuple in ehrChildrenToFHIRChildMatchCandidates[ehrChild]]);

        allFHIRChildrenCandidatesAndParents = set(sorted(allFHIRChildrenCandidatesAndParents));

        ehrChildrenToFHIRChildMatchCandidates_matrix = [];

        # Construct matrix by row: the EHR children
        for ehrChild in ehrChildrenToFHIRChildMatchCandidates: # rows

            ehrChildToCandidateStrengthValuesRow = [];

            # Construct matrix by column: each potential FHIR child to be matched to an EHR child row across the top, with extra FHIR children that have not been previously linked to the EHR child row being added to appease Munkres, and being given a value of 0.
            for fhirChildCandidateAndParent in allFHIRChildrenCandidatesAndParents: # columns

                # If the currently listed fhirChildCandidate, from all candidates across all EHR children, has a value for this actual child, use it, otherwise set to a large number (as it is redundant entry purely for a complete matrix for Munkres).
                if fhirChildCandidateAndParent[0] in [childStrengthTuple[0][0] for childStrengthTuple in ehrChildrenToFHIRChildMatchCandidates[ehrChild]]:

                    # Although list is constructed here, *should* only have one value, which is the retreived matching FHIRentry (get child from child and parent with first 0, then accessed with 0, and then extract the actual strength 1).
                    ehrChildToCandidateStrengthValuesRow.append([childStrengthTuple for childStrengthTuple in ehrChildrenToFHIRChildMatchCandidates[ehrChild] if childStrengthTuple[0][0] == fhirChildCandidateAndParent[0]][0][1] * -1)

                else:

                    # Arbitrarily large number to ensure this FHIR child is not considered as a FHIR candidate for the EHR child (as it wasn't previously matched, it's only included for a complete matrix).
                    ehrChildToCandidateStrengthValuesRow.append(sys.maxint);

            ehrChildrenToFHIRChildMatchCandidates_matrix.append(ehrChildToCandidateStrengthValuesRow);

        # Put the matches back together, this time with the single selected FHIR match.
        ehrChildrenToFHIRChildMatch = {};

        if len(ehrChildrenToFHIRChildMatchCandidates):

            munkres = Munkres();
            strengthAllocation = munkres.compute(ehrChildrenToFHIRChildMatchCandidates_matrix);

            for row, column in strengthAllocation:
                ehrChildrenToFHIRChildMatch[ehrChildRowTitles[row]] = ( list(allFHIRChildrenCandidatesAndParents)[column], ehrChildrenToFHIRChildMatchCandidates_matrix[row][column] * -1 );

        # Post-processing candidates:

        totalChildMatches = 0;
        # Because the number of matches isn't the only thing that's important, it's the accuracy of those matches.
        totalMatchStrength = 0;

        for ehrChildToFHIRChild in ehrChildrenToFHIRChildMatch:

            totalChildMatches += 1;

            # All items in list have same strength, so just use first item.
            totalMatchStrength += ehrChildrenToFHIRChildMatch[ehrChildToFHIRChild][1];

        if ( totalChildMatches > 0 ):

            averageMatchStrength = totalMatchStrength / float(totalChildMatches);

            #print str(totalChildMatches) + " " + str(totalChildMatches / float(len(ehrClassChildren))) + " " + str(averageMatchStrength) + " " + str(len(fhirClassChildren)) + " " + str(min(len(ehrClassChildren) / float(len(fhirClassChildren)), 1)) + " " + str((totalChildMatches / float(len(ehrClassChildren))) * averageMatchStrength);
            # How many matches have been found for the EHR elements in the candidate FHIR class (weighted by match strength, and by the specificity of the class).
            return ((((totalChildMatches / float(len(ehrClassChildren))) * averageMatchStrength)), ehrChildrenToFHIRChildMatch) # * min(len(ehrClassChildren) / float(len(fhirClassChildren)), 1);

        else:

            return (0, ehrChildrenToFHIRChildMatch);

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

        # Selective Recurse selectively expands resources linked to a FHIR class, so that the children of those resources are also included in the FHIR class.
        if (len(ehrClasses)): FHIRTranslation.translatePatientInit(ehrClasses, patientXML);

    @staticmethod
    def translatePatientInit(ehrClasses, patientXML):

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
        fhirClassesToChildren = FHIRTranslation.getFHIRClassesToChildren(TranslationUtilities.getFHIRClasses(True));

        # Remove EHR classes and FHIR classes that do not have children (typically 'type' classes in FHIR).
        ehrClasses = set(ehrClassesToChildren.keys());
        fhirClasses = fhirClassesToChildren.keys();

        FHIRTranslation.matchStageOne(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections);

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
