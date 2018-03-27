import socket, sys, time, xml.dom.minidom, uuid, json, inspect

from xml.sax.saxutils import escape
from nltk.corpus import wordnet

from EHR.APIConstants import APIConstants
from EHR.APIVariables import APIVariables

import unittest

import models.codesystem;

class Utilities(object):
    
    # Find different grammatical forms of words in camelcase string.
    @staticmethod
    def differentWordForms(wordsInString):
        
        replacements = set();
        
        for word in Utilities.listFromCapitals(wordsInString):
            
            for lemma in Utilities.lemmas(word):
                
                replacement = wordsInString.replace(word, lemma.title());
                replacements.add(replacement);
        
        return replacements;
                
    @staticmethod
    def lemmas(word):
        
        lemmas = set();
        
        for lemma in wordnet.lemmas(word):
            
            for related_lemma in lemma.derivationally_related_forms():
                
                lemmas.add(related_lemma.name());
        
        return lemmas;
    
    # NB. FHIR is not hierarchical.
    @staticmethod
    def getFHIRElements(root, set, children=True, parents=True, recurse=True):
        
        # Convert string to class, if not class
        if ( not inspect.isclass(root) ): root = eval(root);
        
        # Ignore test classes.
        if ( unittest.TestCase in inspect.getmro(root) ): return;
        
        print root;
         # Create new object to represent this class.
        FHIRObject = root();
        
        # Don't examine classes that don't use the 'elementsProperties' approach to list attributes.
        if ( not callable(getattr(root, "elementProperties", None)) ): return;
         
        for attributeContainer in root.elementProperties(root()):
            
            attribute = getattr(attributeContainer[2], "elementProperties", None)
            
            if children:
                if not callable(attribute):
                    set.add(attributeContainer[0]);
                    
            if parents:
                if callable(attribute):
                    set.add(attributeContainer[0]);
                    
            else:
                set.add(attributeContainer[0]);
            
            # Don't expand from within FHIRReferences, as it has a recursive reference to identifier (also doesn't appear to be captured correctly by the parser, e.g. organisation from Patient).
            # Extensions classes appear in every class so don't show anything unique.
            if recurse and callable(attribute) and "FHIRReference" not in str(FHIRClass) and "Extension" not in str(attribute[2]):
                
                Utilities.getFHIRElements(elem, set, children, parents, recurse);
                   
        return set;
    
    @staticmethod
    def getXMLElements(root, set, children=True, parents=True, recurse=True, attributes=False):
        
        for elem in root.getchildren():
            
            if children:
                if len(elem.getchildren()) == 0:
                    set.add(elem.tag);
                    if (attributes): set = set.union(elem.attrib.keys());
                    
            if parents:
                if len(elem.getchildren()) > 0:
                    set.add(elem.tag);
                    if (attributes): set = set.union(elem.attrib.keys());
                    
            else:
                set.add(elem.tag);
            
            if ( recurse ): Utilities.getXMLElements(elem, set, children, parents, recurse);
            
        return set
    
    @staticmethod 
    def capitalToSeparation(word):
        
        index = 0;
        
        for letter in list(word):
            
            if index > 0 and letter.isupper():
                word = word[0:index] + "_" + word[index:len(word)]
                index = index + 1
                
            index = index + 1
            
        return word
    
    @staticmethod 
    def listFromCapitals(word):
        
        withSeparators = Utilities.capitalToSeparation(word);
        
        if "_" not in withSeparators:
            return [word];
        else:
            return Utilities.capitalToSeparation(word).split("_");
    
    # NB. FHIR is not a hierarchy.
    @staticmethod 
    def JSONfromFHIRClass(FHIRClass, nullValues):

        # Create new object to represent this class.
        FHIRObject = FHIRClass();
        
        for attribute in FHIRClass.elementProperties(FHIRClass()):
            invert_op = getattr(attribute[2], "elementProperties", None)
            
            # Don't expand from within FHIRReferences, as it has a recursive reference to identifier (also doesn't appear to be captured correctly by the parser, e.g. organisation from Patient).
            # Extensions classes appear in every class so don't show anything unique.
            if callable(invert_op) and "FHIRReference" not in str(FHIRClass) and "Extension" not in str(attribute[2]):             
                subJSON = Utilities.JSONfromFHIRClass(attribute[2], nullValues)
                setattr(FHIRObject, str(attribute[0]), subJSON)
                
            else:
                if (nullValues): 
                    setattr(FHIRObject, str(attribute[0]), None)
                    
                else:
                    setattr(FHIRObject, str(attribute[0]), str(attribute[2]))
                    
        return FHIRObject.__dict__;
    
    # Can include parent keys (e.g. "name": { "family": ... }, becomes family_name) as this helps with similarity checks.
    @staticmethod    
    def getReplaceJSONKeys(data, parents=None, keys=list(), search=None, replace=None):
        
        if isinstance(data, dict):
            
            for k, v in data.items():
                    
                if parents != None and len(parents) > 0:
                    k = k + "_" + parents
               
                keys.append(k);
                
                if (k == search):
                    data[search] = replace
                
                if not isinstance(v, basestring) and not v is None:
                    if parents != None:
                        parents = k;
                        
                    keys = Utilities.getReplaceJSONKeys(v, parents, keys, search, replace)
                    
                    if parents != None:
                        parents = ""
                       
                
        return keys
    
    @staticmethod    
    def printJSONValues(data):
        
        if isinstance(data, dict):
            
            for k, v in data.items():
                
                if isinstance(v, basestring):
                    print k
                    
                else:
                    Utilities.printJSONValues(v)
                    
        elif isinstance(data, list):
            
            for v in data:
                
                if not isinstance(v, str):
                    Utilities.printJSONValues(v)
                    
        else:
            print data;
            
    @staticmethod
    def xmlRequest(data):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_address = (APIVariables.ADDRESS, APIVariables.PORT)
        
        sock.connect(server_address);
        
        response=""
        
        try:
            
            request = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<ClientIntegrationRequest>' + \
            '<RequestUID>' + str(uuid.uuid4()) + '</RequestUID>' + \
            data + \
            '</ClientIntegrationRequest>'
            
            print request;
            sock.sendall(request.encode('utf-8'))
        
            sock.settimeout(20);
            
            time.sleep(2)
            
            BUFF_SIZE = 4096
            
            response = ""
            
            while True:
            
                part = sock.recv(BUFF_SIZE)
                
                response += part
                
                if len(part) < BUFF_SIZE:
                    break
            
            try:
                
                formatted = xml.dom.minidom.parseString(response)
            
                pretty_xml_as_string = formatted.toprettyxml()
            
                return pretty_xml_as_string
            
            except xml.parsers.expat.ExpatError:
                
                return "Cannot parse response. Is the EHR running?"
        
        finally:
            
            sock.close()