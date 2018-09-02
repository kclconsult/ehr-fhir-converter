import json, inspect, collections, xml.etree.ElementTree, sys
from pprint import pprint
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer
import pkgutil
import pyclbr;

#from models.patient import Patient
#import models;
from EHR.SystmOne import SystmOne
from Utils.Utilities import Utilities

import models_full;

import importlib;
from numpy import average

class FHIRTranslation(object):
    
    MODELS_PATH = "models_subset";
    
    EHR_PATH = "tpp/tpp-full";
    
    # Thresholds don't have to be the same at every stage.
    OVERALL_SIMILARITY_THRESHOLD = 0.95;
    
    TEXT_SIMILARITY_THRESHOLD = 0.95;
    
    SEMANTIC_SIMILARITY_THRESHOLD = 0.95;
    
    GRAMMATICAL_SIMILARITY_THRESHOLD = 0.95;
  
    # Might want to be more generous with child matches.
    OVERALL_CHILD_SIMILARITY_THRESHOLD = 0.95;
    
    # The portion of child fields in an EHR tag that must be housed by a FHIR class in order to consider that class a match (weighted by match strength (and candidate class specificity)).
    CHILD_MATCH_THRESHOLD = 0.1
    
    # If some metrics are too generous (e.g. semantic matching 'address' and 'reference'), then we can reduce their 'contribution' to the measure of similarity using a weighting.
    TEXT_SIMILARITY_WEIGHTING = 1;
    
    SEMANTIC_SIMILARITY_WEIGHTING = 0.95;
    
    GRAMMATICAL_SIMILARITY_WEIGHTING = 1;
    
    CONTEXT_WEIGHTING = 2;
    
    EXCLUDED_FHIR_CLASSES = { "Extension", "FHIRReference" };
    
    # Similarity Metric A
    @staticmethod
    def textSimilarity(ehrAttribute, fhirAttribute, stem=False):
        
        # Gradually more complex text similarity
        #if ehrAttribute.lower() == fhirAttribute.lower():
            #return 1.0;
        
        #if ehrAttribute.lower() in fhirAttribute.lower():
        #    return len(ehrAttribute) / float(len(fhirAttribute));
        
        #if fhirAttribute.lower() in ehrAttribute.lower():
        #    return len(fhirAttribute) / float(len(ehrAttribute));
        
        #if stem:
        #    stemmer = PorterStemmer()
        #    ehrAttribute = stemmer.stem(ehrAttribute);
        #    fhirAttribute = stemmer.stem(fhirAttribute);
        
        return fuzz.ratio(ehrAttribute.lower(), fhirAttribute.lower()) / 100.0;
    
    @staticmethod
    def textMatch(ehr, fhir, highestCompositeResult=True, textSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD):
    
        if (FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.textSimilarity, highestCompositeResult) * FHIRTranslation.TEXT_SIMILARITY_WEIGHTING >= textSimilarityThreshold):
            return True;
        
        else:
            return False;
        
    # Similarity Metric B
    @staticmethod
    def semanticSimilarity(ehrAttribute, fhirAttribute):
        
        # If these attributes would be associated via a text match instead, then don't also reevaluate their similarity via the text similarity below.
        if FHIRTranslation.textMatch(ehrAttribute, fhirAttribute, False): return 0;
        
        highestSimilarity = 0;
        
        # wordnet requires word separation by underscore, whereas EHR XML responses (for TPP at least) use camelCase (this won't be an issue if used with composite string similarity, where only one word is used at a time).
        for set in wordnet.synsets(Utilities.capitalToSeparation(ehrAttribute)):
            
            for synonym in set.lemma_names():
                
                similarity = FHIRTranslation.compositeStringSimilarity(Utilities.separationToCapital(synonym), fhirAttribute, FHIRTranslation.textSimilarity, False);
                
                # Get similarity between synonym for ehrAttribute and fhirAttribute (not synonyms that are the ehr attribute itself). If this is over a given threshold, mark as a semantic match.
                if not FHIRTranslation.textSimilarity(synonym, ehrAttribute) == 1.0 and similarity > highestSimilarity and FHIRTranslation.textMatch(Utilities.separationToCapital(synonym), fhirAttribute):
                    
                    highestSimilarity = similarity;
                   
        return highestSimilarity;    
     
    # Similarity Metric C
    @staticmethod
    def grammaticalSimilarity(ehrAttribute, fhirAttribute):
        
        if FHIRTranslation.textMatch(ehrAttribute, fhirAttribute): return 0;
        
        highestSimilarity = 0;
        
        for lemma in Utilities.lemmas(ehrAttribute):
            
            if FHIRTranslation.textSimilarity(lemma, fhirAttribute, True) > highestSimilarity and FHIRTranslation.textMatch(lemma, fhirAttribute):
                highestSimilarity = FHIRTranslation.textSimilarity(lemma, fhirAttribute, True);
        
        return highestSimilarity;
    
    # Similarity Metric D - Sentence progression? e.g. "Done at" and "Location"
    ######
    
    # With highest result False, there needs to be a stricter connection between the class or fields. Probably best for child fields to have stricter match rules.
    @staticmethod
    def compositeStringSimilarity(ehrClassField, fhirClassField, comparisonMethod, highestResult=True):
        
        # If ehrClass string is composite, compare each word with the FHIR target using all of the metrics, and 
        # then use chosen combination method to produce a value.
        # For each word, add these values, and then divide by number of words to get an average match across all words (or max?).
        highestSimilarity = 0;
        totalSimilarity = 0;
        
        ehrWords = Utilities.listFromCapitals(ehrClassField);
        fhirWords = Utilities.listFromCapitals(fhirClassField);
        
        for ehrWord in ehrWords:
            
            highestSimilarityForEHRWord = 0;
            
            for fhirWord in fhirWords:
                
                similarity = comparisonMethod(ehrWord, fhirWord);
                
                if( similarity > highestSimilarity ): highestSimilarity = similarity;
                    
                if ( similarity > highestSimilarityForEHRWord ): highestSimilarityForEHRWord = similarity;
            
            totalSimilarity += highestSimilarityForEHRWord;
            
        if ( highestResult ):
            return highestSimilarity;
        
        else:
            return totalSimilarity / len(ehrWords); #max(float(len(ehrWords)), float(len(fhirWords)));
        
    @staticmethod
    def match(ehrClassField, fhirClassField, textSimilarityWeighting=TEXT_SIMILARITY_WEIGHTING, semanticSimilarityWeighting=SEMANTIC_SIMILARITY_WEIGHTING, grammaticalSimilarityWeighting=GRAMMATICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, grammaticalSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, overallSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True, firstPastThreshold=True, highestStrength=False, combined=False, average=False):
        
        textSimilarity = FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.textSimilarity, highestCompositeResult) * textSimilarityWeighting;
        
        # This should change if highest result is not being used, perhaps to number of words that match?.
        
        if ( firstPastThreshold and textSimilarity >= textSimilarityThreshold  ):
            return FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.textSimilarity, highestCompositeResult);
        
        # 
        
        semanticSimilarity = FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.semanticSimilarity, highestCompositeResult) * semanticSimilarityWeighting;
        
        if ( firstPastThreshold and semanticSimilarity >= semanticSimilarityThreshold):
            
            return FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.semanticSimilarity, highestCompositeResult);
        
        #
        
        grammaticalSimilarity = FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.grammaticalSimilarity, highestCompositeResult) * grammaticalSimilarityWeighting;
        
        if (firstPastThreshold and grammaticalSimilarity >= grammaticalSimilarityThreshold):
            return FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.grammaticalSimilarity, highestCompositeResult);
        
        strength = max(textSimilarity, max(semanticSimilarity, grammaticalSimilarity));
        
        if ( highestStrength and strength >= overallSimilarityThreshold):
            return strength;
        
        strength = textSimilarity + semanticSimilarity + grammaticalSimilarity;
        
        if ( combined and strength >= overallSimilarityThreshold ):
            return strength;
        
        strength = (textSimilarity + semanticSimilarity + grammaticalSimilarity) / 3.0;
        
        if ( average and strength >= overallSimilarityThreshold ):
            return strength; 
        
        return 0;
        
    # See if there is a match at all, based on thresholds.
    @staticmethod
    def matches(ehr, fhir, textSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, grammaticalSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, similarityThreshold=OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True, firstPastThreshold=True, highestStrength=False, combined=False, average=False):
        
            if ( FHIRTranslation.match(ehr, fhir, FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold, semanticSimilarityThreshold, grammaticalSimilarityThreshold, similarityThreshold, highestCompositeResult, firstPastThreshold, highestStrength, combined, average) > 0 ):
                return True;
            
            else:
                return False;
    
    @staticmethod
    def getEHRClasses(patientXML, children=True, parents=False):
        
        return Utilities.getXMLElements(patientXML.find("Response"), {}, False);
        
    @staticmethod
    def getEHRClassChildren(xml, ehrClass, children=True, parents=False):
        
        # As we may have multiple examples of an EHR class in an example piece of marked up data from an EHR vendor, we want to choose that class that has the most children (i.e. the most examples of the schema being used).
        highestChildren = xml.find(".//" + ehrClass)
        for ehrClassExample in xml.findall(".//" + ehrClass):
            if ( len(ehrClassExample.getchildren()) > len(highestChildren.getchildren()) ):
                highestChildren = ehrClassExample;
        
        children = Utilities.getXMLElements(highestChildren, {}, children, parents, True, True);
        
        if 0 in children.keys():
            return children[0];
        else:
            return {};
    
    @staticmethod
    def getFHIRClassChildren(fhirClass, linkedClasses):
        
        fhirElements = Utilities.getFHIRElements(fhirClass, {}, True, False, linkedClasses);

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
    def dataTypeCompatible(ehrData, expression):
        return True;
       
    @staticmethod
    def childSimilarity(ehrClass, fhirClass, ehrClassesToChildren=None, fhirClassesToChildren=None, xml=None, linkedClasses=False):
        
        if ( ehrClassesToChildren ):
            ehrClassChildren = ehrClassesToChildren[ehrClass];
        else:
            ehrClassChildren = FHIRTranslation.getEHRClassChildren(xml, ehrClass);
        
        if ( fhirClassesToChildren ):
            fhirClassChildren = fhirClassesToChildren[fhirClass];  
        else:
            fhirClassChildren = FHIRTranslation.getFHIRClassChildren(fhirClass, linkedClasses);
        
        if (not isinstance(fhirClass, basestring)): 
            fhirClassExclusion = fhirClass.__name__;
        else:
            fhirClassExclusion = fhirClass;
        
        if ( fhirClassChildren == None or fhirClassExclusion in FHIRTranslation.EXCLUDED_FHIR_CLASSES ): return 0;
        
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
                if FHIRTranslation.matches(ehrClassChild, fhirClassChildForMatch, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD) and FHIRTranslation.dataTypeCompatible("", ""):
                    
                    # To identify raw match strength, we want to look at the combined results of all the metrics without any thresholds.  
                    matchStrength = FHIRTranslation.match(ehrClassChild, fhirClassChildForMatch, FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);
                    
                    #matchStrength = FHIRTranslation.match(ehrClassChild, fhirClassChild[0], FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, False);
                    
                    #print ehrClassChild + " " + fhirClassChild + " " + str(matchStrength);
                    
                    # If the EHR child and FHIR child are linked by the name of the EHR parent, this should affect the match strength. E.g. Medication (EHR parent) in MedicationType (EHR Child) and medicationReference (FHIR child) 
                    if ehrClass.lower() in ehrClassChild.lower() and ehrClass.lower() in fhirClassChild[0].lower():
                         matchStrength = matchStrength * FHIRTranslation.CONTEXT_WEIGHTING;
                         
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
           
            # print str(totalChildMatches) + " " + str(totalChildMatches / float(len(ehrClassChildren))) + " " + str(averageMatchStrength) + " " + str(len(fhirClassChildren)) + " " + str(min(len(ehrClassChildren) / float(len(fhirClassChildren)), 1));
            # How many matches have been found for the EHR elements in the candidate FHIR class (weighted by match strength, and by the specificity of the class).       
            return ((totalChildMatches / float(len(ehrClassChildren))) * averageMatchStrength) # * min(len(ehrClassChildren) / float(len(fhirClassChildren)), 1);   
        
        else:
            return 0;
    
    @staticmethod
    def getFHIRClasses():
        
        fhirClasses = [];
        
        for _, fhirModule, _ in pkgutil.iter_modules([FHIRTranslation.MODELS_PATH]):
            
            # Don't use test modules as a potential match.
            if "_tests" in fhirModule: continue;
            
            for fhirClass in pyclbr.readmodule(FHIRTranslation.MODELS_PATH + "." + fhirModule).keys():
                
                # Import this module as we'll need it later to examine content of FHIR Class
                importedModule = importlib.import_module(FHIRTranslation.MODELS_PATH + "." + fhirModule);
                # Turn the fhirClass string into a fhirClass reference.
                fhirClasses.append(getattr(importedModule, fhirClass));
                
        return fhirClasses;
    
    @staticmethod
    def getFHIRConnections(fhirClasses):
        
        connections = {};
        
        for fhirClass in fhirClasses:
            
            if fhirClass in FHIRTranslation.EXCLUDED_FHIR_CLASSES: continue;
            
            for connectingClass in [t for t in (Utilities.getFHIRElements(fhirClass, {}, False, True, False, [], False, True, True, fhirClasses) or [])]:
                
                if connectingClass.__name__ in FHIRTranslation.EXCLUDED_FHIR_CLASSES: continue;
                
                # Log bi-directional connection.
                connections.setdefault(fhirClass,set()).add((connectingClass, "Out"));
                connections.setdefault(connectingClass,set()).add((fhirClass, "In"));
        
        return connections;
        
    @staticmethod
    def getPatient(id):
        # return SystmOne().getPatientRecord(id);
        return xml.etree.ElementTree.parse('../../../resources/' + FHIRTranslation.EHR_PATH + '.xml');

    @staticmethod
    def translatePatient(action=None, ehrClass=None, ehrClassChild=None, fhirClassChild=None, fhirClass=None):
    
         # Get patient record from EHR
        patientXML = FHIRTranslation.getPatient("4917111072");
        
        ehrClasses = {};
        
        if ( action == 0 and ehrClass ):
            ehrClasses = { ehrClass };
        
        elif ( action == 1 and ehrClassChild and fhirClassChild ):
            print "Checking match strength."
            print FHIRTranslation.match(ehrClassChild, fhirClassChild,  FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);
        
        elif ( action == 2 and ehrClassChild and fhirClassChild ):
            print "Checking for match value (if matches)."
            print FHIRTranslation.match(ehrClassChild, fhirClassChild, FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, True, False, True);
            
        elif ( action == 3 and ehrClassChild and fhirClassChild ):
            print "Checking if matches."
            print FHIRTranslation.matches(ehrClassChild, fhirClassChild, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, True);
        
        elif ( action == 4 and ehrClassChild and fhirClassChild ):
            print "Checking semantic similarity."
            print FHIRTranslation.semanticSimilarity(ehrClassChild, fhirClassChild);
        
        elif ( action == 5 and ehrClassChild and fhirClassChild ):
            print "Checking grammatical similarity."
            print FHIRTranslation.grammaticalSimilarity(ehrClassChild, fhirClassChild);
            
        elif ( action == 6 and ehrClass and fhirClass ):
            print "Checking child similarity."
            print FHIRTranslation.childSimilarity(ehrClass, fhirClass, None, None, FHIRTranslation.getPatient("4917111072"));
            
        else:
            ehrClasses = FHIRTranslation.getEHRClasses(patientXML);
        
        if (len(ehrClasses)): FHIRTranslation.translatePatientInit(ehrClasses, patientXML);
                  
    @staticmethod
    def translatePatientInit(ehrClasses, patientXML):
    
        # Get fhirClasses
        fhirClasses = FHIRTranslation.getFHIRClasses();
        
        # Get incoming and outgoing connections to each FHIR class.
        fhirConnections = FHIRTranslation.getFHIRConnections(fhirClasses);
        
        # Prepare lists of classes and children.
        ehrClassesToChildren = {};
        # Get outgoing connections of each ehrClass.
        ehrClassesToParents = {}
        
        for ehrClass in list(set().union(*ehrClasses.values())):
            
            children = FHIRTranslation.getEHRClassChildren(patientXML, ehrClass, True, False);
            if len(children):
                ehrClassesToChildren[ehrClass] = children;
                
            parents = FHIRTranslation.getEHRClassChildren(patientXML, ehrClass, False, True);
            if len (parents):
                ehrClassesToParents[ehrClass] = parents;
        
        fhirClassesToChildren = {};
        
        for fhirClass in fhirClasses:
            
            children = FHIRTranslation.getFHIRClassChildren(fhirClass, False);
            
            if ( children != None ):
                fhirClassesToChildren[fhirClass] = children;
        
        # Remove EHR classes and FHIR classes that do not have children (typically 'type' classes in FHIR).
        ehrClasses = ehrClassesToChildren.keys();
        fhirClasses = fhirClassesToChildren.keys();
        
        # Match components of patient record from EHR to components from JSON representation
        
        # Match stage 1: Exact FHIR terms that are contained in the EHR term
        ehrFHIRMatches = {};
        
        ehrClassesToRemove = set();
        
        for ehrClass in list(set().union(*ehrClasses.values())): 
            
            matches = 0;
            
            for fhirClass in fhirClasses:
                
                if FHIRTranslation.compositeStringSimilarity(ehrClass, str(fhirClass.__name__), FHIRTranslation.textSimilarity, True) == 1.0:
                    matches += 1;
                    fhirMatch = fhirClass;
            
            # If there is only one 100% match between an EHR Class and FHIR Class, we take this as the best candidate, and remove the EHR class from the pool.
            if matches == 1:
                ehrFHIRMatches[ehrClass] = [(fhirMatch, FHIRTranslation.childSimilarity(ehrClass, fhirMatch, ehrClassesToChildren, fhirClassesToChildren))];
                ehrClassesToRemove.add(ehrClass);
        
        # Remove those EHR classes that have now been matched from the list of EHR classes to match. ~MDC Probably could be shorter.
        for depth in ehrClasses:
            for ehrClassToRemove in ehrClassesToRemove:
                if ( ehrClassToRemove in ehrClasses[depth] ):
                    ehrClasses[depth].remove(ehrClassToRemove);
    
        # Match Stage 2: Child matches 
        for ehrClass in list(set().union(*ehrClasses.values())):
            
            ehrFHIRMatches[ehrClass] = [];
            
            childMatches = [];
            
            for fhirClass in fhirClasses:
                
                childSimilarity = FHIRTranslation.childSimilarity(ehrClass, fhirClass, None, fhirClassesToChildren, FHIRTranslation.getPatient("4917111072"));
                                
                childMatches.append((fhirClass, childSimilarity));
                
            childMatches = sorted(childMatches, key=lambda sortable: (sortable[1]), reverse=True);
            
            for childMatch in childMatches:
                
                if ( childMatch[1] > FHIRTranslation.CHILD_MATCH_THRESHOLD ):
                    ehrFHIRMatches[ehrClass].append(childMatch);
            
            #print str(ehrClass) + " " + str(childMatches);        
            # If there are no candidates for an ehrClass based on child matches (i.e. none of the matches are above the threshold), then choose the highest.
            if len(ehrFHIRMatches[ehrClass]) == 0:
                
                firstChildMatch = childMatches[0];
                highestMatch = firstChildMatch[1];
                ehrFHIRMatches[ehrClass].append(firstChildMatch);
                
                # Skip the match that has just been added.
                iterChildMatches = iter(childMatches);
                next(iterChildMatches);
                
                for childMatch in iterChildMatches:
                    if ( childMatch[1] == highestMatch ):
                        ehrFHIRMatches[ehrClass].append(childMatch);
                    else:
                        break;
           
        # Match Stage 3: Fuzzy parent matches
        
        # Now decide between multiples matches based upon names of parent classes.
        for ehrClass in ehrFHIRMatches:
            
            # Convert EHR to FHIR class matches to include similarity of parent class names.
            fhirClassChildParentSimilarity = [];
            
            # For each matching FHIR class to this EHR class
            for fhirClassChildSimilarity in ehrFHIRMatches[ehrClass]:
                
                similarity = FHIRTranslation.match(ehrClass, fhirClassChildSimilarity[0].__name__);
                asList = list(fhirClassChildSimilarity)
                # Add the parent similarity to the child similarity to get an overall similarity value.
                asList[1] = asList[1] + similarity;
                fhirClassChildSimilarity = tuple(asList)
                fhirClassChildParentSimilarity.append(fhirClassChildSimilarity);
            
            ehrFHIRMatches[ehrClass] = fhirClassChildParentSimilarity;              
        
        # Match Stage 3.5: 
        for ehrClass in list(set().union(*ehrClasses.values())):
            
            for fhirClass in fhirClasses:
                
                # If any of the outgoing connections from the EHR class (child elements) now have FHIR matches, see if that set of convertible connections corresponds to the connections (incoming and outgoing) of this FHIR class. Add this result to the child similarity.
                commonConnections = 0;
                
                for outgoingChild in ehrClassesToParents[ehrClass]:
                    
                    if outgoingChild in ehrFHIRMatches.keys():
                        
                        if fhirClass not in fhirConnections.keys(): continue;
                        
                        for connection in [fhirConnection[0] for fhirConnection in fhirConnections[fhirClass]]:
                            
                            if ehrFHIRMatches[outgoingChild][0][0] == connection:
                                
                                commonConnections += 1;
                                #print str(outgoingChild) + " is a child of " + str(ehrClass) + ". " + str(outgoingChild) + " has been matched to " + str(ehrFHIRMatches[outgoingChild][0][0]) + " in FHIR, connecting the two. " + str(fhirClass) + " is also connected to " + str(connection) + ", so " + str(ehrClass) + " and " + str(fhirClass) + " are related.";
                                
                                for match in ehrFHIRMatches[ehrClass]:
                                    
                                    if match[0] == fhirClass:
                                        
                                        if len(match) == 3:
                                            asList = list(match)
                                            asList[2] = asList[2] + 1;
                                            ehrFHIRMatches[ehrClass][ehrFHIRMatches[ehrClass].index(match)] = tuple(asList)
                                        
                                        else:
                                            ehrFHIRMatches[ehrClass][ehrFHIRMatches[ehrClass].index(match)] = match + (1,);
                                         
        for ehrClass in ehrFHIRMatches:
            
            print "===========================";
            print ehrClass;
            matches = sorted(ehrFHIRMatches[ehrClass], key=lambda sortable: (sortable[1]), reverse=True);
            
            if len(matches):
                print matches;
            
                # Match Stage 4: Match EHR children to FHIR children from chosen class.
                children = fhirClassesToChildren[matches[0][0]]; # [:]
                
                ehrChildToHighestFHIRchild = {};
                
                # Find matches for each of the parent matches.
                for ehrChild in ehrClassesToChildren[ehrClass]:
                            
                    # Find the FHIR children of the top match. Extract the name of the FHIR class from each tuple.
                    for fhirChild in children:
                   
                        # Each child is a tuple with parent as second value.
                        matchStrength = FHIRTranslation.match(ehrChild, fhirChild[0], FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True)
                        
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
        #print ft.childSimilarity("Medication", "models_full.claimresponse.ClaimResponsePayment", None, None, ft.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Medication", "models_full.medicationrequest.MedicationRequest", None, None, FHIRTranslation.getPatient("4917111072"), True);
        #print FHIRTranslation.childSimilarity("Medication", "models_full.sequence.SequenceStructureVariantInner", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Demographics", "models_full.patient.Patient", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Demographics", "models_full.activitydefinition.ActivityDefinition", None, None, FHIRTranslation.getPatient("4917111072"));              
