import pkgutil, importlib, pyclbr, inspect, sys

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
                else:
                    fhirClasses.append(fhirClass);

            if mergeBackboneElements and len(connectedClasses): fhirClasses.append(connectedClasses);

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

    # Aim to treat EHR classes with the same name as different entities, if they have non-intersecting child classes.
    @staticmethod
    def ehrClassToExamples(patientXML):

        depths = Utilities.getXMLElements(patientXML, {}, False, True, False, True, True);

        for depth in range(len(depths) -1, 0, -1):

            # Expand EHR classes with children that are a subset of one or more other EHR classes with the same name to include the additional children.
            for ehrClass in depths[depth]:

                log = False;
                if "ClinicalCode" in ehrClass.tag: log = True;
                allChildren = [];

                # Only append afterwards to retain structure throughout processing
                childrenToAppend = {};

                for ehrClassExample in patientXML.findall(".//" + ehrClass.tag):

                    if ( len(ehrClassExample.getchildren()) == 0  ): continue;
                    allChildren.append( (ehrClassExample, ehrClassExample.getchildren() ) );

                if ( len(allChildren) == 0  ): continue;

                allChildren.sort(key=lambda t: len(t[1]), reverse=True)

                for children in allChildren:

                    for otherChildren in allChildren:

                        if ( children[1] == otherChildren[1] or str([element.tag for element in otherChildren[1]]) == str([element.tag for element in children[1]]) ): continue;

                        if ( set([element.tag for element in otherChildren[1]]).issubset(set([element.tag for element in children[1]])) ):

                            for child in children[1]:

                                if child.tag not in str([element.tag for element in otherChildren[1]]):

                                    childrenToAppend.setdefault(otherChildren[0], []).append(child);

                for parentElement in childrenToAppend.keys():

                    for newChildElement in childrenToAppend[parentElement]:

                        if ( newChildElement.tag not in [element.tag for element in parentElement.getchildren()]):

                            parentElement.append(newChildElement);

                # EHR classes that still have different children after this processing are given different numeric names so they are treated as different entities.
                childrenToNewTagName = {};

                for ehrClassExample in patientXML.findall(".//" + ehrClass.tag):

                    if ( str(sorted([element.tag for element in ehrClassExample.getchildren()])) not in childrenToNewTagName.keys() ):

                        if (len(childrenToNewTagName) > 0): ehrClassExample.tag = ehrClassExample.tag + str(len(childrenToNewTagName));

                        childrenToNewTagName[str(sorted([element.tag for element in ehrClassExample.getchildren()]))] = ehrClassExample.tag;

                    else:

                        ehrClassExample.tag = childrenToNewTagName[str(sorted([element.tag for element in ehrClassExample.getchildren()]))];

        return patientXML;

    @staticmethod
    def getEHRClasses(patientXML, children=True, parents=False, duplicates=False):

        if ( duplicates ):

           ehrClasses = Utilities.getXMLElements(patientXML, {}, False, parents, duplicates);
           allValues = [];
           for depth in ehrClasses: allValues += ehrClasses[depth];
           return allValues;

        else:

            # Combines all value in dictionary of EHR depths.
            return [element.tag for element in set(set().union(*Utilities.getXMLElements(patientXML, {}, False, parents, duplicates).values()))];

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

    # See if the children of this EHR
    # See if other classes that are children of this EHR element, and have resolved FHIR connections, would be linked to from this mutual connection, thus strengthening the connection between the relationship.
    @staticmethod
    def recreatableConnections(ehrClass, ehrClasses, ehrFHIRMatches, fhirConnections, path=[]):

        if len(ehrClasses) == 0: return path;

        print str(ehrClass) + " " + str(ehrClasses) + " " + str(path);

        # Copy ehrClasses content to new object, as we'll be removing items.
        ehrClasses = set(list(ehrClasses)[:])
        ehrClasses.remove(ehrClass);

        for sibling in ehrClasses:

            print "Sibling: " + str(sibling) + " " + str(ehrClass == sibling) + " " + str(sibling not in ehrFHIRMatches.keys());

            if ( ehrClass == sibling or sibling not in ehrFHIRMatches.keys() ): continue;

            print "Sibling FHIR version: " + str(ehrFHIRMatches[sibling][0][0]);
            print "ehrClass FHIR version: " + str(ehrFHIRMatches[ehrClass][0][0]);
            print "FHIR connections EHR class: " + str(fhirConnections[ehrFHIRMatches[ehrClass][0][0]]);

            # If the FHIR versions of two EHR siblings connect
            if ( ehrFHIRMatches[sibling][0][0] in [fhirConnection[0] for fhirConnection in fhirConnections[ehrFHIRMatches[ehrClass][0][0]]]  ):

                path.append(ehrFHIRMatches[sibling][0]);
                recreatableConnections(sibling, ehrClasses, ehrFHIRMatches, fhirConnections, path);

        return path;
