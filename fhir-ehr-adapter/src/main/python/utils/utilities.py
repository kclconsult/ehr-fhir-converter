import socket, sys, time, xml.dom.minidom, uuid, json, inspect, collections

from xml.sax.saxutils import escape
from nltk.corpus import wordnet

from EHR.APIConstants import APIConstants
from EHR.APIVariables import APIVariables

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

class Utilities(object):
    
    MODELS_PATH = "models_subset";
    
    @staticmethod
    def mergeDicts(dicts):
        
        superDict = collections.defaultdict(set)
        for d in dicts:
            for k, v in d.iteritems():  # d.items() in Python 3+
                superDict[k].update(v)
        
        return superDict;

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
            
    @staticmethod
    def getXMLElements(root, depthToElement={}, children=True, parents=True, recurse=True, attributes=False, depth=0):
        
        for elem in root.getchildren():
            
            if children: # if is child
                if len(elem.getchildren()) == 0:
                    depthToElement.setdefault(depth, set()).add(elem.tag);
                    if (attributes): 
                        for attribute in elem.attrib.keys():
                            depthToElement.setdefault(depth, set()).add(attribute);
                    
            if parents: # if is parent
                if len(elem.getchildren()) > 0 or len(elem.attrib.keys()):
                    depthToElement.setdefault(depth, set()).add(elem.tag);
                    #set.add(elem.tag);
                    #if (attributes): set = set.union(elem.attrib.keys()); ~MDC Attributes always children?
                    
            if not children and not parents:
                depthToElement.setdefault(depth, set()).add(elem.tag);
            
            if ( recurse ): 
                # Record depth allowing us to order ehrClasses by tree position, so we look at most nested first.
                Utilities.getXMLElements(elem, depthToElement, children, parents, recurse, attributes, depth+1);
        
        return depthToElement
    
    @staticmethod 
    def capitalToSeparation(word):
        
        index = 0;
        
        for letter in list(word):
            
            if index > 0 and letter.isupper():
                word = word[0:index] + "_" + word[index:len(word)]
                index += 1
                
            index += 1
            
        return word
    
    @staticmethod 
    def listFromCapitals(word):
        
        withSeparators = Utilities.capitalToSeparation(word);
        
        if "_" not in withSeparators:
            return [word];
        else:
            return Utilities.capitalToSeparation(word).split("_");
    
    @staticmethod
    def separationToCapital(word):
        
        full_word = "";
        
        for section in word.split("_"):
            
            full_word += section.capitalize();
        
        return full_word;
        
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
    def ehrRequest(data):
        
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