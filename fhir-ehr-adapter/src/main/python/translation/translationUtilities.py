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
    
    @staticmethod
    def getFHIRClasses(mergeBackboneElements=True):
        
        fhirClasses = [];
        
        for _, fhirModule, _ in pkgutil.iter_modules([TranslationConstants.MODELS_PATH]):
            
            # Don't use test modules as a potential match.
            if "_tests" in fhirModule: continue;
            
            for fhirClass in pyclbr.readmodule(TranslationConstants.MODELS_PATH + "." + fhirModule).keys():
                
                if fhirClass in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;
                
                # Import this module as we'll need it later to examine content of FHIR Class
                importedModule = importlib.import_module(TranslationConstants.MODELS_PATH + "." + fhirModule);
                
                # Turn the fhirClass string into a fhirClass reference.
                fhirClass = getattr(importedModule, fhirClass);
                
                # We don't want supporting classes, just main 
                # if (mergeBackboneElements):
                if "BackboneElement" in [base.__name__ for base in fhirClass.__bases__]: continue
                
                fhirClasses.append(fhirClass);
                
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
    
    @staticmethod
    def ehrClassToExamples(patientXML):
        
        ehrParents = set([elem.tag for elem in patientXML.iter() if len(elem.getchildren()) > 0]);
        
        # Treats EHR classes with a different set of children as a different EHR class, even if names are the same. Gives a unique name to the EHR class. 
        for ehrClass in ehrParents:
            
            id = 0;
            
            for ehrClassExample in patientXML.findall(".//" + ehrClass):
                
                if ( len(ehrClassExample.getchildren()) == 0  ): continue;
                
                if ( id != 0 ): ehrClassExample.tag = ehrClassExample.tag + str(id);
                
                id += 1;
             
        depths = Utilities.getXMLElements(patientXML, {}, False, True, False, True, True);
        
        parentMap = { child:parent for parent in patientXML.iter() for child in parent }
        
        for depth in range(len(depths) -1, 0, -1):
            
            # EHR classes with children that are a subset of other classes are ignored.
            ehrClassesToRemove = [];
        
            for ehrClassExample in depths[depth]:
                
                # To avoid mutual removal from the list (and avoid superfluous loops).
                if ( ehrClassExample.tag in [element.tag for element in ehrClassesToRemove] ): continue;
                
                # Remove parents if they no longer have any children (due to a previous deletion iteration).
                if len(ehrClassExample.getchildren()) == 0: 
                    
                    ehrClassesToRemove.append(ehrClassExample);
                    continue;
                    
                for otherEHRClassExample in depths[depth]:
                    
                    # To avoid superfluous loops.
                    if ( otherEHRClassExample.tag in [element.tag for element in ehrClassesToRemove] ): continue;
                    
                    if ( ehrClassExample.tag == otherEHRClassExample.tag ): continue;
                    
                    if len( otherEHRClassExample.getchildren() ) == 0: 
                    
                        ehrClassesToRemove.append(otherEHRClassExample);
                        continue;
                    
                    if ( Utilities.removeLastCharIfNumber(ehrClassExample.tag) == Utilities.removeLastCharIfNumber(otherEHRClassExample.tag) ):
                        
                        if ( len(ehrClassExample.getchildren()) == len(otherEHRClassExample.getchildren()) ): 
                            
                            # If same number of children, choose element with most siblings.
                            if ( len(parentMap[ehrClassExample].getchildren()) > len(parentMap[otherEHRClassExample].getchildren()) ):
                                
                                ehrClassesToRemove.append(otherEHRClassExample);
                            
                            elif ( len(parentMap[ehrClassExample].getchildren()) < len(parentMap[otherEHRClassExample].getchildren()) ):
                                
                                ehrClassesToRemove.append(ehrClassExample);
                                # Because the outer loop class is now being removed.
                                break;
                            
                        elif ( set([elem.tag for elem in otherEHRClassExample.getchildren()]).issubset(set([elem.tag for elem in ehrClassExample.getchildren()])) ):

                            ehrClassesToRemove.append(otherEHRClassExample);
        
            # Remove IDs that are subsets post loop.
            for ehrClass in set(ehrClassesToRemove): parentMap[ehrClass].remove(ehrClass);
        
            # If, after removal, we are only left with one version of this EHR class, remove any IDs from end of key.
            for ehrClassExample in patientXML.iter():
                
                if (  Utilities.isNumber( ehrClassExample.tag[len(ehrClassExample.tag) - 1] ) and len([element.tag for element in patientXML.iter() if element.tag.startswith( ehrClassExample.tag[:-1] ) and Utilities.isNumber( element.tag[len(element.tag) - 1] ) ] ) == 1 ):
                    
                    ehrClassExample.tag = ehrClassExample.tag[:-1];
        
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
                
                    # TODO: Fix: ehrClassChildren.setDefault(ehrClass, []).extend(ehrClassExampleDepthsToChildren[0]);
                    ehrClassChildren[ehrClass] = [element.tag for element in ehrClassExampleDepthsToChildren[0]];
                    
                else:
                    
                    allEHRClassChildren.append({ ehrClassExample: [element.tag for element in ehrClassExampleDepthsToChildren[0]] });
                
            if ( not allEHRChildren ): break;
            
        if ( groupEHRChildren ): ehrClassChildren = Utilities.mergeDicts([allEHRClassChildren]);
                
        return ehrClassChildren;
    
    # See if other classes that are children of this EHR element, and have resolved FHIR connections, would be linked to from this mutual connection, thus strengthening the connection between the relationship.
    @staticmethod
    def recreatableConnections(ehrClass, ehrClasses, ehrFHIRMatches, fhirConnections, path=[]):
        
        if len(ehrClasses) == 0: return path;
        
        print str(ehrClass) + " " + str(ehrClasses) + " " + str(path);
        
        # Copy ehrClasses content to new object, as we'll be removing items.
        ehrClasses = set(list(ehrClasses)[:])
        ehrClasses.remove(ehrClass);
        
        for sibling in ehrClasses:
            
            print "Sibling: " + str(sibling);
            
            if ( ehrClass == sibling or sibling not in ehrFHIRMatches.keys() ): continue;
            
            print "Sibling FHIR version: " + str(ehrFHIRMatches[sibling][0][0]);
            print "ehrClass FHIR version: " + str(ehrFHIRMatches[ehrClass][0][0]);
            print "FHIR connections EHR class: " + str(fhirConnections[ehrFHIRMatches[ehrClass][0][0]]);
            
            # If the FHIR versions of two EHR siblings connect
            if ( ehrFHIRMatches[sibling][0][0] in [fhirConnection[0] for fhirConnection in fhirConnections[ehrFHIRMatches[ehrClass][0][0]]]  ):
                
                path.append(ehrFHIRMatches[sibling][0]);           
                recreatableConnections(sibling, ehrClasses, ehrFHIRMatches, fhirConnections, path);
            
        return path;    
        
         