import pkgutil, importlib, pyclbr, inspect, sys, operator

from utils.utilities import Utilities;
from translation.translationConstants import TranslationConstants;

import unittest, models_subset

import models_full.activitydefinition;
import models_full.address;
#import models.codesystem;
import models_full.devicemetric;
import models_full.claimresponse;
import models_full.medication;
import models_full.medicationdispense;
import models_full.medicationadministration;
import models_full.medicationrequest;
import models_full.patient;
import models_full.sequence;

import models_subset.practitioner;
import models_subset.patient;
import models_subset.coding;
import models_subset.encounter;
import models_subset.codeableconcept;

class TranslationUtilities(object):

    #TODO: Actually merge class with its backbone.
    @staticmethod
    def getFHIRClasses(mergeBackboneElements=False):

        fhirClasses = [];

        for _, fhirModule, _ in pkgutil.iter_modules([TranslationConstants.MODELS_PATH]):

            # Don't use test modules as a potential match.
            if "_tests" in fhirModule: continue;

            connectedClasses = [];

            for fhirClass in pyclbr.readmodule(TranslationConstants.MODELS_PATH + "." + fhirModule).keys():

                if fhirClass in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;

                # Import this module as we'll need it later to examine content of FHIR Class
                importedModule = importlib.import_module(TranslationConstants.MODELS_PATH + "." + fhirModule);

                # Turn the fhirClass string into a fhirClass reference.
                fhirClass = getattr(importedModule, fhirClass);

                # We don't want supporting classes, just main
                # if (mergeBackboneElements):
                if not mergeBackboneElements and "BackboneElement" in [base.__name__ for base in fhirClass.__bases__]: continue

                if mergeBackboneElements:
                    connectedClasses.append(fhirClass);
                    # Sorts the classes in order to always have the base class (non-backbone) first, e.g. Encounter first over something like EncounterLocation.
                    connectedClasses = sorted(connectedClasses, cmp=Utilities.classLengthSort);
                else:
                    fhirClasses.append(fhirClass);

            if mergeBackboneElements and len(connectedClasses):
                fhirClasses.append(connectedClasses);

        return fhirClasses;

    @staticmethod
    def getFHIRConnections(fhirClasses):

        connections = {};

        for fhirClass in fhirClasses:

            if fhirClass in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;

            for connectingClass in [t for t in (TranslationUtilities.getFHIRElements(fhirClass, {}, False, True, False, [], [], False, True, True, fhirClasses) or [])]:

                if connectingClass.__name__ in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;

                # Log bi-directional connection.
                connections.setdefault(fhirClass,set()).add((connectingClass, "Out"));
                connections.setdefault(connectingClass,set()).add((fhirClass, "In"));

        return connections;

    @staticmethod
    def processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName):

        if attributeTypeOverAttributeName:
            classesToChildren[root].add(attributeContainer[2]);
        else:
            classesToChildren[root].add(attributeName);

    # NB. FHIR is not hierarchical.
    @staticmethod
    def getFHIRElements(root, classesToChildren, children=True, parents=True, recurse=True, selectiveRecurse=[], visited=[], addParentName=False, attributeTypeOverAttributeName=False, resolveFHIRReferences=False, otherFHIRClasses=None):

        # Convert string to class, if not class.
        if ( not inspect.isclass(root) ): root = eval(root);

        # Ignore test classes.
        if ( unittest.TestCase in inspect.getmro(root) or Exception in inspect.getmro(root) ): return;

        # Don't examine classes that don't use the 'elementsProperties' approach to list attributes.
        if ( not callable(getattr(root, "elementProperties", None)) ): return;

        if ( root not in classesToChildren.keys() ): classesToChildren[root] = set();

        # Attributes of this class and parents.
        attributes = root.elementProperties(root());

        # List of parents (first element in tuple is this class).
        parents = inspect.getmro(root)[1:]

        for parent in parents:

            if ( not callable(getattr(parent, "elementProperties", None)) ): continue;

            attributes = [item for item in attributes if item not in parent.elementProperties(parent())]

        # If the type of an attribute is simply 'FHIRReference' we aim to resolve the scope of this reference by adding duplicate attributes for each potential reference type.
        if resolveFHIRReferences:

            #print "---> " + str(root);

            newAttributes = [];

            for attributeContainer in attributes:

                if ( "FHIRReference" in attributeContainer[2].__name__ ):

                    #print attributeContainer[0];

                    sourceLines = inspect.getsource(root).split("\n");

                    for sourceLine in sourceLines:

                        if ( "self." + attributeContainer[0] in sourceLine ):

                            #print sourceLine;

                            # If the list of possible references happens not to be two lines later, try three lines later.
                            if "FHIRReference" not in sourceLines[sourceLines.index(sourceLine) + 2]:
                                index = sourceLines.index(sourceLine) + 3;
                            else:
                                index = sourceLines.index(sourceLine) + 2;

                            for possibleFHIRReference in inspect.getsource(root).split("\n")[index].split("`")[3].split(","):

                                if possibleFHIRReference.strip() in [item.__name__ for item in otherFHIRClasses]:

                                    attributeContainerAsList = list(attributeContainer);
                                    attributeContainerAsList.insert(2, otherFHIRClasses[[item.__name__ for item in otherFHIRClasses].index(possibleFHIRReference.strip())]);
                                    attributeContainer = tuple(attributeContainerAsList);
                                    newAttributes.append(attributeContainer);

                else:
                    newAttributes.append(attributeContainer);

            attributes = newAttributes;

        # For all attributes of this class (minus attributes of parent, which are typically generic).
        for attributeContainer in attributes:

            attribute = getattr(attributeContainer[2], "elementProperties", None)
            attributeName = attributeContainer[0];

            #print str(attributeContainer);

            if addParentName: attributeName = attributeName + str(root.__name__); # ! Change this to add it as an extra child.

            if children:
                if not callable(attribute):
                    TranslationUtilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName);

            if parents:
                if callable(attribute):
                    TranslationUtilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName);

            else:
                TranslationUtilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName);

            # Don't expand from within FHIRReferences, as it has a recursive reference to identifier (also doesn't appear to be captured correctly by the parser, e.g. organisation from Patient).
            # Extensions classes appear in every class so don't show anything unique.
            # Don't follow links to types that are of the root class itself.
            # and attributeContainer[0] not in set([j for i in classesToChildren.values() for j in i])
            if ( ( recurse and len(selectiveRecurse) == 0 ) or ( recurse and str(root.__name__) in selectiveRecurse ) or ( recurse and str(attributeContainer[2].__name__) in selectiveRecurse ) ) and callable(attribute) and "FHIRReference" not in str(root.__name__) and "Extension" not in str(attributeContainer[2]) and attributeContainer[2] != root and attributeContainer[0] not in visited:

                visited.append(attributeContainer[0]);
                TranslationUtilities.getFHIRElements(attributeContainer[2], classesToChildren, children, parents, recurse, selectiveRecurse, visited);

        if recurse:
            return classesToChildren;

        else:
            return classesToChildren[root];

    @staticmethod
    def getFHIRClassChildren(fhirClass, linkedClasses, selectiveRecurse=[]):

        fhirElements = TranslationUtilities.getFHIRElements(fhirClass, {}, True, False, linkedClasses, selectiveRecurse, []);

        if linkedClasses and fhirElements != None:

            fhirChildAndParent = [];

            for fhirClassToChildren in fhirElements:

                for fhirClassChild in fhirElements[fhirClassToChildren]:

                    # If linked classes are examined, it's not just the name of the fhirChild for the supplied class added, but also the name of the fhir children in each linked class, and entries are stored as tuples so the origin of the child can be traced.
                    fhirChildAndParent.append((fhirClassChild, fhirClassToChildren));

            return fhirChildAndParent;

        else:
            return fhirElements;

    # Aim to treat EHR classes with the same name as different entities if they have non-intersecting child classes.
    @staticmethod
    def ehrClassToExamples(patientXML):

        # First get unique examples of EHR classes, to be expanded upon later to find all examples
        noDuplicateEHRClassesAtDepths = Utilities.getXMLElements(patientXML, {}, False, True, False, True, True);

        for depth in range(len(noDuplicateEHRClassesAtDepths) -1, 0, -1):

            # Expand EHR classes with children that are a subset of one or more other EHR classes with the same name to include the additional children held by that other class. This method will additionally ensure EHR classes are subsumed by larger EHR classes created during the expansion process.
            for ehrClass in noDuplicateEHRClassesAtDepths[depth]:

                allParentsAndChildren = [];

                # Only append afterwards to retain structure throughout processing. Will not contain all parents.
                childrenToAppend = {};

                # Store so we get the same memory IDs later for debugging.
                ehrClassExamples = patientXML.findall(".//" + ehrClass.tag);

                # Find all examples from original unique list.
                for ehrClassExample in ehrClassExamples:

                    if ( len(ehrClassExample.getchildren()) == 0  ): continue;
                    allParentsAndChildren.append( (ehrClassExample, ehrClassExample.getchildren() ) );

                if ( len(allParentsAndChildren) == 0  ): continue;

                # Sort so that the the parents with the least children are considered first.
                allParentsAndChildren.sort(key=lambda t: len(t[1]), reverse=True)

                for parentAndChildren in allParentsAndChildren:

                    for parentAndOtherChildren in allParentsAndChildren:

                        children = parentAndChildren[1];
                        otherParent = parentAndOtherChildren[0]
                        otherChildren = parentAndOtherChildren[1];

                        # If trying to compare to self as part of nested loop, skip.
                        if ( children == otherChildren or str([element.tag for element in otherChildren]) == str([element.tag for element in children]) ): continue;

                        # EHRname - set of children; sameEHRname - other set of children. If the childen of sameEHRname are a subset of the children of EHRname, then (plan to) add the children of EHRname that are not in sameEHRname to sameEHRname.
                        if ( set([element.tag for element in otherChildren]).issubset(set([element.tag for element in children])) ):

                            for child in children:

                                if child.tag not in str([element.tag for element in otherChildren]):

                                    # Prepare to add later to avoid changing structure during processing.
                                    childrenToAppend.setdefault(otherParent, []).append(child);

                # EHR classes with the same name that still have different children after this processing are given different numeric suffixes so they are treated as different entities. To do this, this dictionary is introduced to link unique, sorted sets of children to parent names.
                childrenToNewTagName = {};

                for ehrClassExample in ehrClassExamples:

                    if ( len(ehrClassExample.getchildren()) == 0  ): continue;

                    # If we don't have a record of this instance of an EHR class name (e.g. one instance of a ClinicalCode element, when lots of ClinicalCode elements exist in the document.), then it is either the first example of this EHR class name (+ children) combination that we have extracted, or it is a new EHR class name + children combination, in which case it should be recorded with a new incremented numerical suffix. As such, childrenToNewTagName holds a record of all unique EHRname:children combinations.
                    if ( str(sorted([element.tag for element in ehrClassExample.getchildren()])) not in childrenToNewTagName.keys() ):

                        # Incrementally name.
                        if (len(childrenToNewTagName) > 0): ehrClassExample.tag = ehrClassExample.tag + str(len(childrenToNewTagName));

                        # Record the mapping between this set of EHR children and the new tag name. We order the set (to ensure different permutations are ignored when indexing), and if the EHR happens to have multiple children with the same tag, don't use this as part of the index.
                        childrenToNewTagName[str(sorted([element.tag for element in ehrClassExample.getchildren()]))] = ehrClassExample.tag;

                    else:

                        # If we do have a record of this EHR class name + children combination, then it has already been given a numerical suffix (or none, if it was the first instance in the document), so this EHR element example should be given the same numerical suffix, as along with its children it represents the same entity.
                        ehrClassExample.tag = childrenToNewTagName[str(sorted([element.tag for element in ehrClassExample.getchildren()]))];

        return patientXML;

    @staticmethod
    def getEHRClasses(patientXML, children=True, parents=True, duplicates=False):

        if ( duplicates ):

           ehrClasses = Utilities.getXMLElements(patientXML, {}, children, parents, duplicates);
           allValues = [];
           for depth in ehrClasses: allValues += ehrClasses[depth];
           return allValues;

        else:

            # Combines all values in dictionary of EHR depths.
            return [element.tag for element in set(set().union(*Utilities.getXMLElements(patientXML, {}, children, parents, duplicates).values()))];

    @staticmethod
    def filterChildrenParents(ehrClassChildren, filter):

        ehrChildrenToRemove = [];

        for ehrClassChild in ehrClassChildren:

            childElements = [element[1] for element in ehrClassChildren[ehrClassChild] if element[0] == filter];

            if ( childElements ): ehrClassChildren[ehrClassChild] = childElements;
            else: ehrChildrenToRemove.append(ehrClassChild);

        all(map(ehrClassChildren.pop, ehrChildrenToRemove));

        return ehrClassChildren;

    @staticmethod
    def getEHRClassChildren(patientXML, ehrClass, children=True, parents=False, allEHRChildren=False, groupEHRChildren=False):

        ehrClassChildren = {};

        # As we may have multiple examples of an EHR class in an example piece of marked up data from an EHR vendor, we want to find all possible examples of children that can be listed under that class.
        allEHRClassChildren = []

        for ehrClassExample in patientXML.findall(".//" + ehrClass):

            ehrClassExampleDepthsToChildren = Utilities.getXMLElements(ehrClassExample, {}, children, parents, False, True, True);

            if 0 in ehrClassExampleDepthsToChildren.keys():

                if ( not allEHRChildren or groupEHRChildren ):

                    ehrClassChildren.setdefault(ehrClass, []).extend([element.tag for element in ehrClassExampleDepthsToChildren[0]]);

                else:

                    allEHRClassChildren.append({ ehrClassExample: [element.tag for element in ehrClassExampleDepthsToChildren[0]] });

            if ( not allEHRChildren ): break;

        if ( groupEHRChildren ): ehrClassChildren = Utilities.mergeDicts([allEHRClassChildren]);

        return ehrClassChildren;

    # Once an EHR class (EHRA) and a FHIR class (FHIRA) are related -- because a child of EHRA (ChildA) and a connection of FHIRA (ConnectionA) have been child-matched together -- see if any of the siblings of ChildA have FHIR child matches themselves. For example, another child (ChildB) might have a FHIR child match (ConnectionB). If this is the case, is FHIR ConnectionA linked to FHIR ConnectionB? If so, this strengthens the case for the connection between the original, top EHR class and FHIR class connections -- EHRA and FHIRA -- because it shows that if this match is chosen, FHIRA class can replicate the connection between two of EHRA's children through a two-hop path of resource connections. Therefore, in the best case, the FHIR versions of all of EHRA's children are all connected together, through resource references, in a path from FHIRA. This puts less emphasis on finding a single FHIR class that connects to all of an EHR class's FHIR represented children (path, rather than one-to-many).
    @staticmethod
    def recreatableConnections(ehrClass, ehrClasses, ehrFHIRMatches, fhirConnections, path=[]):

        if len(ehrClasses) == 0: return path;

        # Copy ehrClasses content to new object, as we'll be removing items.
        ehrClasses = set(list(ehrClasses)[:])
        ehrClasses.remove(ehrClass);

        for sibling in ehrClasses:

            if ( ehrClass == sibling or sibling not in ehrFHIRMatches.keys() ): continue;

            ehrFHIRMatchesSortedSibling = sorted(ehrFHIRMatches[sibling].items(), key=operator.itemgetter(1));
            ehrFHIRMatchesSortedSibling.reverse();

            ehrFHIRMatchesSortedEHR = sorted(ehrFHIRMatches[ehrClass].items(), key=operator.itemgetter(1));
            ehrFHIRMatchesSortedEHR.reverse();

            # If the FHIR versions of two EHR siblings connect, then we can replicate the link between two EHR children with connected FHIR classes.
            if ( ehrFHIRMatchesSortedSibling[0][0] in [fhirConnection[0] for fhirConnection in fhirConnections[ehrFHIRMatchesSortedEHR[0][0]]] ):

                path.append(ehrFHIRMatches[sibling][0]);
                # Recurse in an attempt to find the best case.
                recreatableConnections(sibling, ehrClasses, ehrFHIRMatches, fhirConnections, path);

        return path;
