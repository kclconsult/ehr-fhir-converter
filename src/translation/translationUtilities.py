from builtins import str
from builtins import range
from builtins import object
import pkgutil, importlib, pyclbr, inspect, sys, operator, re

from utils.utilities import Utilities;
from translation.translationConstants import TranslationConstants;

import unittest, models_subset

class TranslationUtilities(object):

    @staticmethod
    def getFHIRClasses(mergeBackboneElements=False, mustBeCallable=True):

        fhirClasses = [];

        for _, fhirModule, _ in pkgutil.iter_modules([TranslationConstants.MODELS_PATH]):

            # Don't use test modules as a potential match.
            if "_tests" in fhirModule: continue;

            if (sys.version_info > (3, 0)):
                classes = sorted(list(pyclbr.readmodule(TranslationConstants.MODELS_PATH + "." + fhirModule).keys()), key=Utilities.cmpToKey(Utilities.classLengthSort))
            else:
                classes = sorted(list(pyclbr.readmodule(TranslationConstants.MODELS_PATH + "." + fhirModule).keys()), cmp=Utilities.classLengthSort)
            # Sorts the classes in order to always have the base class (non-backbone) first, e.g. Encounter first over something like EncounterLocation. Based on the assumption that shortest class names are the base element class.
            for fhirClass in classes:

                if len([excludedMatch for excludedMatch in TranslationConstants.EXCLUDED_FHIR_CLASS_TYPES if excludedMatch in fhirClass]): continue

                # Import this module as we'll need it later to examine content of FHIR Class
                importedModule = importlib.import_module(TranslationConstants.MODELS_PATH + "." + fhirModule);

                # Turn the fhirClass string into a fhirClass reference.
                fhirClass = getattr(importedModule, fhirClass);

                if mustBeCallable and not callable(fhirClass): continue;

                # We don't want supporting classes, just main
                # if (mergeBackboneElements):
                if not mergeBackboneElements and "BackboneElement" in [base.__name__ for base in fhirClass.__bases__]: continue

                if mergeBackboneElements and "BackboneElement" in [base.__name__ for base in fhirClass.__bases__]:
                    fhirClasses[len(fhirClasses) - 1].append(fhirClass);
                elif mergeBackboneElements:
                    fhirClasses.append( [ fhirClass] );
                else:
                    fhirClasses.append(fhirClass);

        return fhirClasses;

    @staticmethod
    def getFHIRConnections(fhirClasses, excludeBackboneClasses=True):

        connections = {};

        for fhirClass in fhirClasses:

            if len([excludedMatch for excludedMatch in TranslationConstants.EXCLUDED_FHIR_CLASS_TYPES if excludedMatch in fhirClass.__name__]): continue

            for connectingClass in [t for t in (TranslationUtilities.getFHIRElements(fhirClass, {}, False, True, False, [], [], False, True, True, fhirClasses) or [])]:

                if len([excludedMatch for excludedMatch in TranslationConstants.EXCLUDED_FHIR_CLASS_TYPES if excludedMatch in connectingClass.__name__]) or ( excludeBackboneClasses and ( "BackboneElement" in [base.__name__ for base in connectingClass.__bases__])): continue;

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

    @staticmethod
    def getFHIRElements(root, classesToChildren, children=True, parents=True, recurse=True, selectiveRecurse=[], visited=[], addParentName=False, attributeTypeOverAttributeName=False, resolveFHIRReferences=False, otherFHIRClasses=None):

        if len([excludedMatch for excludedMatch in TranslationConstants.EXCLUDED_FHIR_CLASS_TYPES if excludedMatch in root.__name__]): return [];

        # Convert string to class, if not class.
        if ( not inspect.isclass(root) ): root = eval(root);

        # Ignore test classes.
        if ( unittest.TestCase in inspect.getmro(root) or Exception in inspect.getmro(root) ): return [];

        # Don't examine classes that don't use the 'elementsProperties' approach to list attributes.
        if ( not callable(getattr(root, "elementProperties", None)) ): return [];

        if ( root not in list(classesToChildren.keys()) ): classesToChildren[root] = set();

        # Attributes of this class and parents.
        attributes = root.elementProperties(root());

        # List of parents (first element in tuple is this class).
        parentList = inspect.getmro(root)[1:]

        for parent in parentList:

            if ( not callable(getattr(parent, "elementProperties", None)) ): continue;

            # Don't reinclude attributes that are already included in a parent.
            attributes = [item for item in attributes if item not in parent.elementProperties(parent())]

        # If the type of an attribute is simply 'FHIRReference' we aim to resolve the scope of this reference by adding duplicate attributes for each potential reference type.
        if resolveFHIRReferences:

            newAttributes = [];

            for attributeContainer in attributes:

                if ( "FHIRReference" in attributeContainer[2].__name__ ):

                    sourceLines = inspect.getsource(root).split("\n");

                    for sourceLine in sourceLines:

                        if ( "self." + attributeContainer[0] in sourceLine ):

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

            if len([excludedMatch for excludedMatch in TranslationConstants.EXCLUDED_FHIR_CLASS_TYPES if excludedMatch in attributeName]): continue


            if children:
                elementsOfChildren = TranslationUtilities.getFHIRElements(attributeContainer[2], {}, True, False, False);

                # If a parent child (linked to another FHIR resource) has a suitable field that can hold data (e.g. value, text), then it doesn't matter if it's a parent, as it can effectively just act as a named container, so it might as well be a child.
                if not callable(attribute) or not set(TranslationConstants.FIELDS_THAT_INDICATE_RESOURCE_CAN_HOLD_ANY_DATA).isdisjoint(set(elementsOfChildren)):

                    TranslationUtilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName);

                    # Add an additional pseudoelement with the parent name appended, whiich aims to represents the context given by the parent (e.g. child: first (not enough on its own) parent: HumanName full: firstHumanName (better representation of what is stored)).
                    if addParentName:

                        TranslationUtilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName + str(root.__name__));

            if parents:
                if callable(attribute):
                    TranslationUtilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName);

            # Don't expand from within FHIRReference, as it has a recursive reference to identifier (also doesn't appear to be captured correctly by the parser, e.g. organisation from Patient).
            # Extensions classes appear in every class so don't show anything unique.
            # Don't follow links to types that are of the root class itself.
            # and attributeContainer[0] not in set([j for i in classesToChildren.values() for j in i])
            if ( ( recurse and len(selectiveRecurse) == 0 ) or ( recurse and str(root.__name__) in selectiveRecurse ) or ( recurse and str(attributeContainer[2].__name__) in selectiveRecurse ) ) and callable(attribute) and "FHIRReference" not in str(root.__name__) and "Extension" not in str(attributeContainer[2]) and attributeContainer[2] != root and attributeContainer[0] not in visited:

                visited.append(attributeContainer[0]);
                TranslationUtilities.getFHIRElements(attributeContainer[2], classesToChildren, children, parents, recurse, selectiveRecurse, visited, addParentName, attributeTypeOverAttributeName, resolveFHIRReferences, otherFHIRClasses);

        if recurse:
            return classesToChildren;

        else:
            return classesToChildren[root];

    @staticmethod
    def getFHIRClassChildren(fhirClass, linkedClasses, recurse=True, selectiveRecurse=[]):

        # Classes plural because may also include linked classes.
        fhirClassesToChildren = TranslationUtilities.getFHIRElements(fhirClass, {}, True, False, recurse, selectiveRecurse, [], True);

        if fhirClassesToChildren != None:

            fhirChildrenOrChildrenAndParent = [];

            for fhirClassToChildren in fhirClassesToChildren:

                for fhirClassChild in fhirClassesToChildren[fhirClassToChildren]:

                    # If linked classes are examined, it's not just the name of the fhirChild for the supplied class added, but also the name of the fhir children in each linked class, and entries are stored as tuples so the origin of the child can be traced.
                    if ( linkedClasses ):
                        fhirChildrenOrChildrenAndParent.append((fhirClassChild, fhirClassToChildren));

                    else:
                        fhirChildrenOrChildrenAndParent.append(fhirClassChild);

            return fhirChildrenOrChildrenAndParent;

    @staticmethod
    def getFHIRClassChildType(fhirChild, fhirClass, addParentName=True):

        # If we're adding pseudo child elements, we won't be able to derive a type for them (because they don't exist), so remove parent suffix.
        if ( addParentName ):

            if ( re.match( "[a-zA-Z0-9]+" + fhirClass.__name__ + "[a-zA-Z0-9]*" , fhirChild ) ):

                fhirChild = fhirChild[:fhirChild.index(fhirClass.__name__)];

        sourceLines = inspect.getsource(fhirClass).split("\n");

        for sourceLine in sourceLines:

            if ( "self." + fhirChild in sourceLine ):

                for type in list(TranslationConstants.TYPES_TO_REGEX.keys()):

                    if ( type in sourceLines[sourceLines.index(sourceLine) + 2].strip() ):

                        return type;

                # If this isn't a type line, it's a resource reference line, and as the only resources permitted to act as children are effective leaf nodes, return string.
                return "str";

        return None;

    # Aim to treat EHR classes with the same name as different entities if they have non-intersecting child classes.
    @staticmethod
    def ehrClassToExamples(patientXML):

        # First get unique examples of EHR classes, to be expanded upon later to find all examples
        noDuplicateEHRClassesAtDepths = Utilities.getXMLElements(patientXML, {}, False, True, False, True, True);

        for depth in range(len(noDuplicateEHRClassesAtDepths) -1, 0, -1):

            # Expand EHR classes with children that are a subset of one or more other EHR classes with the same name to include the additional children held by that other class. This method will not ensure EHR classes are subsumed by larger EHR classes created during the expansion process.
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
                    if ( str(sorted([element.tag for element in ehrClassExample.getchildren()])) not in list(childrenToNewTagName.keys()) ):

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
            return [element.tag for element in set(set().union(*list(Utilities.getXMLElements(patientXML, {}, children, parents, duplicates).values())))];

    @staticmethod
    def getEHRClassChildren(patientXML, ehrClass, children=True, parents=False, allEHRChildren=False, contextualiseChildren=True):

        ehrClassChildren = {};

        for ehrClassExample in patientXML.findall(".//" + ehrClass):

            ehrClassExampleDepthsToChildren = Utilities.getXMLElements(ehrClassExample, {}, children, parents, False, True, True);

            if 0 in list(ehrClassExampleDepthsToChildren.keys()):

                for element in ehrClassExampleDepthsToChildren[0]:

                    # Contextualise those EHR children that do not give enough context on their own, because they are just generic children.
                    if ( contextualiseChildren and element.tag in TranslationConstants.FIELDS_THAT_INDICATE_RESOURCE_CAN_HOLD_ANY_DATA ):

                        # Work out how to present this new compound child (child + parent name), based on which separators are used by this EHR.
                        if ( TranslationConstants.SEPARATOR != "" ):
                            element.tag = ehrClass + TranslationConstants.SEPARATOR + element.tag;

                        else:
                            element.tag = ehrClass[1:] + ehrClass[0].upper() + element.tag;

                    ehrClassChildren.setdefault(ehrClass, []).extend([element.tag]);

            # As we may have multiple examples of an EHR class in an example piece of marked up data from an EHR vendor, we want to find all possible examples of children that can be listed under that class.
            if ( not allEHRChildren ): break;

        return ehrClassChildren;
