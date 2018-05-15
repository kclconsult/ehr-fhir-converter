import json, inspect, collections, xml.etree.ElementTree, sys
from pprint import pprint
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer
import pkgutil
import pyclbr;

#from models.patient import Patient
import models;
import models_full;

from EHR.SystmOne import SystmOne
from Utils.Utilities import Utilities

import importlib;
from numpy import average

class FHIRTranslation():
    
    MODELS_PATH = "models_full";
    
    EHR_PATH = "tpp-full";
    
    # Could adjust based on user feedback if, for example, matches are too generous.
    # A user-friendly way of asking about this 'do you feel you've got too many results?'.
    # Different threshold if two words (less strict).
    # Single threshold for all
    TEXT_SIMILARITY_THRESHOLD = 0.95;
    
    SEMANTIC_SIMILARITY_THRESHOLD = 0.8;
    
    GRAMMATICAL_SIMILARITY_THRESHOLD = 0.5;
    
    # Thresholds don't have to be the same at every stage.
    OVERALL_SIMILARITY_THRESHOLD = 0.95;
    
    # Might want to be more generous with child matches.
    OVERALL_CHILD_SIMILARITY_THRESHOLD = 0.8;
    
    # The portion of child fields in an EHR tag that must be housed by a FHIR class in order to consider that class a match (weighted by match strength and candidate class specificity)..
    CHILD_MATCH_THRESHOLD = 0.1
    
    # If some metrics are too generous (e.g. semantic matching 'address' and 'reference'), then we can reduce their 'contribution' to the measure of similarity using a weighting.
    TEXT_SIMILARITY_WEIGHTING = 1;
    
    SEMANTIC_SIMILARITY_WEIGHTING = 0.8;
    
    GRAMMATICAL_SIMILARITY_WEIGHTING = 1;
    
    CONTEXT_WEIGHTING = 2;
    
    # Similarity Metric A
    @staticmethod
    def textSimilarity(ehrAttribute, fhirAttribute, stem=False):
        
        # Gradually more complex text similarity
        if ehrAttribute.lower() == fhirAttribute.lower():
            return 1.0;
        
        if ehrAttribute.lower() in fhirAttribute.lower():
            return len(ehrAttribute) / float(len(fhirAttribute));
        
        if fhirAttribute.lower() in ehrAttribute.lower():
            return len(fhirAttribute) / float(len(ehrAttribute));
        
        if stem:
            stemmer = PorterStemmer()
            ehrAttribute = stemmer.stem(ehrAttribute);
            fhirAttribute = stemmer.stem(fhirAttribute);
        
        return fuzz.ratio(ehrAttribute, fhirAttribute) / 100.0;
    
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
        
        #if FHIRTranslation.textMatch(ehrAttribute, fhirAttribute): return 0;
        
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
    
    # Same as match but without thresholds to give raw match value.
    @staticmethod
    def match(ehrClassField, fhirClassField, textSimilarityWeighting=TEXT_SIMILARITY_WEIGHTING, semanticSimilarityWeighting=SEMANTIC_SIMILARITY_WEIGHTING, grammaticalSimilarityWeighting=GRAMMATICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, grammaticalSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True, firstPastThreshold=True, highestStrength=False, combined=False):
        
        textSimilarity = FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.textSimilarity, highestCompositeResult) * textSimilarityWeighting;
        
        # This should change if highest result is not being used, perhaps to number of words that match?.
        
        if ( firstPastThreshold and textSimilarity >= textSimilarityThreshold  ):
            return FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.textSimilarity, highestCompositeResult);
        
        # 
        
        semanticSimilarity = FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.semanticSimilarity, highestCompositeResult) * semanticSimilarityWeighting;
        
        if ( firstPastThreshold and semanticSimilarity >= semanticSimilarityThreshold):
            
            return FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.semanticSimilarity, highestCompositeResult);
        
        #
        
        grammaticalSimilarity = FHIRTranslation.compositeStringSimilarity(ehrClassField, fhirClassField, FHIRTranslation.grammaticalSimilarity, highestCompositeResult) * grammaticalSimilarityWeighting;
        
        if (firstPastThreshold and grammaticalSimilarity >= grammaticalSimilarityThreshold):
            return FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.grammaticalSimilarity, highestCompositeResult);
        
        if ( firstPastThreshold ): return 0;
        
        #
        
        if ( highestStrength ):
            return max(textSimilarity, max(semanticSimilarity, grammaticalSimilarity));
        if ( combined ):
            return textSimilarity + semanticSimilarity + grammaticalSimilarity;
        else:
            return (textSimilarity + semanticSimilarity + grammaticalSimilarity) / 3.0;
        
    # See if there is a match at all, based on thresholds.
    @staticmethod
    def matches(ehr, fhir, textSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, grammaticalSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True, firstPastThreshold=True, highestStrength=False, combined=False,average=False):
        
        if ( firstPastThreshold ):
            
            if ( FHIRTranslation.match(ehrClassChild, fhirClassChild[0], FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold, semanticSimilarityThreshold, grammaticalSimilarityThreshold, highestCompositeResult, firstPastThreshold, highestStrength, combined) > 0 ):
                return True;
            
            else:
                return False;
            
        if ( higeshtStrength or combine or average ):
            
            if ( FHIRTranslation.match(ehrClassChild, fhirClassChild[0], FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, textSimilarityThreshold, semanticSimilarityThreshold, grammaticalSimilarityThreshold, highestCompositeResult, firstPastThreshold, highestStrength, combined) > FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD ):
                return True;
            
            else:
                return False;
    
    @staticmethod
    def getEHRClassChildren(xml, ehrClass):
        return Utilities.getXMLElements(xml.find(".//" + ehrClass), set(), True, True, False, True);
    
    @staticmethod
    def getFHIRClassChildren(fhirClass, linkedClasses):
        
        fhirElements = Utilities.getFHIRElements(fhirClass, {}, True, True, linkedClasses);
        
        if linkedClasses and fhirElements != None:
            
            fhirChildAndParent = [];
            
            for fhirClassToChildren in fhirElements:
                
                for fhirClassChild in fhirElements[fhirClassToChildren]:
                    
                    # If linked classes are examined, it's not just the name of the fhirChild for the supplied class added, but also the name of the fhir children in each linked class, and entries are stored as tuples, so the origin of the child can be traced.
                    fhirChildAndParent.append((fhirClassChild, fhirClassToChildren));
            
            return fhirChildAndParent;
               
        else:
            return fhirElements;
    
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
        
        totalChildMatches = 0;
        # Because the number of matches isn't the only thing that's important, it's the accuracy of those matches.
        totalMatchStrength = 0;
        
        if ( fhirClassChildren == None ): return 0;
        
        # Because the same FHIR class field may be a candidate for more than one EHR attribute, and we cannot accommodate more than one attribute in a field, we keep track of these multiple matches, so as to only count them once in our total child matches, and to pick the strongest match for our strength indications. 
        fhirMatchCandidates = {};
        
        for fhirClassChild in fhirClassChildren: fhirMatchCandidates[fhirClassChild] = [];
        
        # For each child of the EHR parent (also includes ATTRIBUTES (same tag) of EHR parent and children).
        for ehrClassChild in ehrClassChildren:
            
            highestMatchStrength = 0;
            highestFHIRClassChildMatch = "";
            
            # Look at that FHIR classes children
            for fhirClassChild in fhirClassChildren:
                
                # Compare all FHIR class children to each child of this EHR class, and find the most that match in order to resolve multiple potential class matches.
                if FHIRTranslation.matches(ehrClassChild, fhirClassChild[0], FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, True) and FHIRTranslation.dataTypeCompatible("", ""):
                    
                    #matchStrength = FHIRTranslation.match(ehrClassChild, fhirClassChild[0], FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, False);
                    matchStrength = FHIRTranslation.match(ehrClassChild, fhirClassChild[0], FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, False, False, True);
                    
                    # print ehrClassChild + " " + fhirClassChild + " " + str(matchStrength);
                    
                    if matchStrength > highestMatchStrength:
                        highestMatchStrength = matchStrength;
                        highestFHIRClassChildMatch = fhirClassChild;
                    
            if highestFHIRClassChildMatch in fhirMatchCandidates.keys():
                
                if len(fhirMatchCandidates[highestFHIRClassChildMatch]) > 0:
                    
                    if highestMatchStrength >= fhirMatchCandidates[highestFHIRClassChildMatch][0][1]:
                        
                        if highestMatchStrength > fhirMatchCandidates[highestFHIRClassChildMatch][0][1]:
                            del fhirMatchCandidates[highestFHIRClassChildMatch][:];
                           
                        fhirMatchCandidates[highestFHIRClassChildMatch].append((ehrClassChild, highestMatchStrength));
                
                else:
                    fhirMatchCandidates[highestFHIRClassChildMatch].append((ehrClassChild, highestMatchStrength));
                   
        for fhirMatchCandidate in fhirMatchCandidates:
            
            if len(fhirMatchCandidates[fhirMatchCandidate]) > 0:
                
                totalChildMatches += len(fhirMatchCandidates[fhirMatchCandidate]);
                
                # if the ehr child and fhir child are linked by the name of the ehr entry, this should affect the match strength. 
                if ehrClass.lower() in fhirMatchCandidate[0].lower() and ehrClass.lower() in fhirMatchCandidates[fhirMatchCandidate][0][0].lower():
                    fhirMatchCandidates[fhirMatchCandidate][0] = (fhirMatchCandidates[fhirMatchCandidate][0][0], fhirMatchCandidates[fhirMatchCandidate][0][1] * FHIRTranslation.CONTEXT_WEIGHTING);
                    
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
    def getPatient(id):
        # return SystmOne().getPatientRecord(id);
        return xml.etree.ElementTree.parse('../../../../resources/' + FHIRTranslation.EHR_PATH + '.xml');
                   
    @staticmethod
    def translatePatient(action=None, ehrClass=None, ehrClassChild=None, fhirClassChild=None):
        
        #print FHIRTranslation.matchStrength("MedicationType", "medicationCodeableConcept", FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, False, True);
        #print FHIRTranslation.childSimilarity("Medication", "models_full.claimresponse.ClaimResponsePayment", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Medication", "models_full.medicationrequest.MedicationRequest", None, None, FHIRTranslation.getPatient("4917111072"), True);
        #print FHIRTranslation.childSimilarity("Medication", "models_full.sequence.SequenceStructureVariantInner", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Demographics", "models_full.patient.Patient", None, None, FHIRTranslation.getPatient("4917111072"));
        #print FHIRTranslation.childSimilarity("Demographics", "models_full.activitydefinition.ActivityDefinition", None, None, FHIRTranslation.getPatient("4917111072"));
    
         # Get patient record from EHR
        patientXML = FHIRTranslation.getPatient("4917111072");
        
        ehrClasses = {};
        
        if ( action == 0 and ehrClass ):
            ehrClasses = { ehrClass };
        
        elif ( action == 1 and ehrClassChild and fhirClassChild ):
            print "Checking match strength."
            print FHIRTranslation.match(ehrClassChild, fhirClassChild,  FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, False, False, True);
        
        elif ( action == 2 and ehrClassChild and fhirClassChild ):
            print "Checking for match value (if matches)."
            print FHIRTranslation.match(ehrClassChild, fhirClassChild, FHIRTranslation.TEXT_SIMILARITY_WEIGHTING,  FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING,  FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, True, False, True);
            
        elif ( action == 3 and ehrClassChild and fhirClassChild ):
            print "Checking if matches."
            print FHIRTranslation.matches(ehrClassChild, fhirClassChild, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, True);
        
        elif ( action == 4 and ehrClassChild and ehrClassChild ):
            print "Checking semantic similarity."
            print FHIRTranslation.semanticSimilarity(ehrClassChild, fhirClassChild);
        
        elif ( action == 5 and ehrClassChild and ehrClassChild ):
            print "Checking grammatical similarity."
            print FHIRTranslation.grammaticalSimilarity(ehrClassChild, fhirClassChild);
            
        else:
            ehrClasses = Utilities.getXMLElements(patientXML.find("Response"), set(), False);
            
        if (len(ehrClasses)): FHIRTranslation.translatePatientInit(ehrClasses, patientXML);
    
    
    @staticmethod
    def translatePatientInit(ehrClasses, patientXML):
        
        # Get fhirClasses
        fhirClasses = FHIRTranslation.getFHIRClasses();
    
        # Prepare lists of classes and children.
        ehrClassesToChildren = {};
        
        for ehrClass in ehrClasses:
            
            ehrClassesToChildren[ehrClass] = FHIRTranslation.getEHRClassChildren(patientXML, ehrClass);
        
        fhirClassesToChildren = {};
        
        for fhirClass in fhirClasses:
            
            children = FHIRTranslation.getFHIRClassChildren(fhirClass, True);
            
            if ( children != None ):
                fhirClassesToChildren[fhirClass] = children;
        
        # Remove FHIR classes that do not have children (typically 'type' classes).
        fhirClasses = fhirClassesToChildren.keys();
        
        # Match components of patient record from EHR to components from JSON representation
        
        # Match stage 1: Exact FHIR terms that are contained in the EHR term
        ehrFHIRMatches = {};
        
        ehrClassesToRemove = set();
        
        for ehrClass in ehrClasses: # ! Should be EHR classes with children.
        
            matches = 0;
            
            for fhirClass in fhirClasses:
                
                if FHIRTranslation.compositeStringSimilarity(ehrClass, str(fhirClass.__name__), FHIRTranslation.textSimilarity, True) == 1.0:
                    matches += 1;
                    fhirMatch = fhirClass;
            
            # If there is only one 100% match between an EHR Class and FHIR Class, we take this as the best candidate, and remove the EHR class from the pool.
            if matches == 1:
                ehrFHIRMatches[ehrClass] = [(fhirMatch, FHIRTranslation.childSimilarity(ehrClass, fhirMatch, ehrClassesToChildren, fhirClassesToChildren))];
                ehrClassesToRemove.add(ehrClass);
        
        ehrClasses = ehrClasses - ehrClassesToRemove;
        
        # Match Stage 2: Child matches
        
        # Match EHR to FHIR classes based on similarity between EHR attributes and nested tags and FHIR class attributes.
        for ehrClass in ehrClasses:
            
            ehrFHIRMatches[ehrClass] = [];
            
            childMatches = [];
            
            for fhirClass in fhirClasses:
                
                childSimilarity = FHIRTranslation.childSimilarity(ehrClass, fhirClass, ehrClassesToChildren, fhirClassesToChildren);
                
                childMatches.append((fhirClass, childSimilarity));

            childMatches = sorted(childMatches, key=lambda sortable: (sortable[1]), reverse=True);
            
            for childMatch in childMatches:
                
                if ( childMatch[1] > FHIRTranslation.CHILD_MATCH_THRESHOLD ):
                    ehrFHIRMatches[ehrClass].append(childMatch);
                    
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
                lst = list(fhirClassChildSimilarity)
                # Add the parent similarity to the child similarity to get an overall similarity value.
                lst[1] = lst[1] + similarity;
                fhirClassChildSimilarity = tuple(lst)
                fhirClassChildParentSimilarity.append(fhirClassChildSimilarity);
            
            ehrFHIRMatches[ehrClass] = fhirClassChildParentSimilarity;              
        
        for ehrClass in ehrFHIRMatches:
            
            print ehrClass;
            matches = sorted(ehrFHIRMatches[ehrClass], key=lambda sortable: (sortable[1]), reverse=True);
            
            if len(matches):
                print matches;
        
        # Replace values in JSON version of matching classes.
        # Utilities.getReplaceJSONKeys(patientJSON, None, list(), 'id', 'abc');
        
        # return.
        # return patientJSON
    
    ##########
    
    # Combination Mechanism A
    @staticmethod
    def averageSimilarity(ehrClass, fhirClass):
        
        # Add all similarities together, divide to get between 0 and 1.
        return (FHIRTranslation.textSimilarity(ehrClass, fhirClass, True) + 
                FHIRTranslation.semanticSimilarity(ehrClass, fhirClass) + 
                FHIRTranslation.grammaticalSimilarity(ehrClass, fhirClass)) / 3.0;
        
    # Combination Mechanism B
    @staticmethod
    def maxSimilarity(ehrClass, fhirClass):
        
        return max(FHIRTranslation.textSimilarity(ehrClass, fhirClass, True), 
               max(FHIRTranslation.semanticSimilarity(ehrClass, fhirClass), FHIRTranslation.grammaticalSimilarity(ehrClass, fhirClass)));
    
    ##########
                