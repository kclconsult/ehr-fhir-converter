import pkgutil, importlib, pyclbr, inspect

from utils.utilities import Utilities;
from translation.translationConstants import TranslationConstants;

import unittest

class TranslationUtilities(object):
    
    @staticmethod
    def getFHIRClasses():
        
        fhirClasses = [];
        
        for _, fhirModule, _ in pkgutil.iter_modules([TranslationConstants.MODELS_PATH]):
            
            # Don't use test modules as a potential match.
            if "_tests" in fhirModule: continue;
            
            for fhirClass in pyclbr.readmodule(TranslationConstants.MODELS_PATH + "." + fhirModule).keys():
                
                # Import this module as we'll need it later to examine content of FHIR Class
                importedModule = importlib.import_module(TranslationConstants.MODELS_PATH + "." + fhirModule);
                # Turn the fhirClass string into a fhirClass reference.
                fhirClasses.append(getattr(importedModule, fhirClass));
                
        return fhirClasses;
    
    @staticmethod
    def getFHIRConnections(fhirClasses):
        
        connections = {};
        
        for fhirClass in fhirClasses:
            
            if fhirClass in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;
            
            for connectingClass in [t for t in (TranslationUtilities.getFHIRElements(fhirClass, {}, False, True, False, [], False, True, True, fhirClasses) or [])]:
                
                if connectingClass.__name__ in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;
                
                # Log bi-directional connection.
                connections.setdefault(fhirClass,set()).add((connectingClass, "Out"));
                connections.setdefault(connectingClass,set()).add((fhirClass, "In"));
        
        return connections;
        
    # NB. FHIR is not hierarchical.
    @staticmethod
    def getFHIRElements(root, classesToChildren, children=True, parents=True, recurse=True, visited=[], addParentName=False, attributeTypeOverAttributeName=False, resolveFHIRReferences=False, otherFHIRClasses=None):
        
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
        
        # If the type of an attribute is simply 'FHIRReference' we aim to resolve the scope of this reference by adding duplicate the attribute for each potential reference type.
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
                    Utilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName);
                    
            if parents:
                if callable(attribute):
                    Utilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName);
                    
            else:
                Utilities.processAttribute(root, attributeTypeOverAttributeName, resolveFHIRReferences, classesToChildren, attributeContainer, attributeName);
                
            # Don't expand from within FHIRReferences, as it has a recursive reference to identifier (also doesn't appear to be captured correctly by the parser, e.g. organisation from Patient).
            # Extensions classes appear in every class so don't show anything unique.
            # Don't follow links to types that are of the root class itself.
            # and attributeContainer[0] not in set([j for i in classesToChildren.values() for j in i])
            if recurse and callable(attribute) and "FHIRReference" not in str(root.__name__) and "Extension" not in str(attributeContainer[2]) and attributeContainer[2] != root and attributeContainer[0] not in visited:
                
                visited.append(attributeContainer[0]);
                Utilities.getFHIRElements(attributeContainer[2], classesToChildren, children, parents, recurse, visited);
                
                    
        if recurse:     
            return classesToChildren;
        
        else:
            return classesToChildren[root];
    
    @staticmethod
    def getFHIRClassChildren(fhirClass, linkedClasses):
        
        fhirElements = TranslationUtilities.getFHIRElements(fhirClass, {}, True, False, linkedClasses);

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
    def getEHRClasses(patientXML, children=True, parents=False):
        
        # Combines all value in dictionary of EHR depths.
        return set(set().union(*Utilities.getXMLElements(patientXML.find("Response"), {}, False).values()));
        
    @staticmethod
    def getEHRClassChildren(xml, ehrClass, children=True, parents=False):
        
        # As we may have multiple examples of an EHR class in an example piece of marked up data from an EHR vendor, we want to find all possible examples of children that can be listed under that class.
        allEHRClassChildren = []
        for ehrClassExample in xml.findall(".//" + ehrClass):
            ehrClassExampleChildren = Utilities.getXMLElements(ehrClassExample, {}, children, parents, True, True)
            if ( children and len(ehrClassExample.attrib.keys()) ):
                ehrClassExampleChildren.setdefault(0, set()).update(ehrClassExample.attrib.keys());
            allEHRClassChildren.append(ehrClassExampleChildren);
        
        ehrClassChildren = Utilities.mergeDicts(allEHRClassChildren);
        
        if 0 in ehrClassChildren.keys():
            return ehrClassChildren[0];
        else:
            return {};