import json, collections, xml.etree.ElementTree, sys
from pprint import pprint

from EHR.SystmOne import SystmOne
from utils.utilities import Utilities
from translation.translationConstants import TranslationConstants
from translation.similarityMetrics import SimilarityMetrics
from translation.translationUtilities import TranslationUtilities
from translation.matches import Matches;

import models_full;

class FHIRTranslation(object):
    
    @staticmethod
    def dataTypeCompatible(ehrData, expression):
        return True;
       
    @staticmethod
    def childSimilarity(ehrClass, fhirClass, ehrClassesToChildren=None, fhirClassesToChildren=None, xml=None, linkedClasses=False):
        
        if ( ehrClassesToChildren ):
            ehrClassChildren = ehrClassesToChildren[ehrClass];
        else:
            ehrClassChildren = TranslationUtilities.getEHRClassChildren(xml, ehrClass);
        
        if ( fhirClassesToChildren ):
            fhirClassChildren = fhirClassesToChildren[fhirClass];  
        else:
            fhirClassChildren = TranslationUtilities.getFHIRClassChildren(fhirClass, linkedClasses);
        
        if (not isinstance(fhirClass, basestring)): 
            fhirClassExclusion = fhirClass.__name__;
        else:
            fhirClassExclusion = fhirClass;
        
        if ( fhirClassChildren == None or fhirClassExclusion in TranslationConstants.EXCLUDED_FHIR_CLASSES ): return 0;
        
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
                if Matches.matches(ehrClassChild, fhirClassChildForMatch, TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD) and FHIRTranslation.dataTypeCompatible("", ""):
                    
                    # To identify raw match strength, we want to look at the combined results of all the metrics without any thresholds.  
                    matchStrength = Matches.match(ehrClassChild, fhirClassChildForMatch, TranslationConstants.TEXT_SIMILARITY_WEIGHTING,  TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING,  TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);
                    
                    #matchStrength = FHIRTranslation.match(ehrClassChild, fhirClassChild[0], TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, False);
                    
                    #print ehrClassChild + " " + fhirClassChild + " " + str(matchStrength);
                    
                    # If the EHR child and FHIR child are linked by the name of the EHR parent, this should affect the match strength. E.g. Medication (EHR parent) in MedicationType (EHR Child) and medicationReference (FHIR child) 
                    if ehrClass.lower() in ehrClassChild.lower() and ehrClass.lower() in fhirClassChild[0].lower():
                         matchStrength = matchStrength * TranslationConstants.CONTEXT_WEIGHTING;
                         
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
    def getPatient(id):
        # return SystmOne().getPatientRecord(id);
        return xml.etree.ElementTree.parse('../../../resources/' + TranslationConstants.EHR_PATH + '.xml');

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
        
        if (len(ehrClasses)): FHIRTranslation.translatePatientInit(ehrClasses, patientXML);
    
    @staticmethod
    def translatePatientInit(ehrClasses, patientXML):
        
        # Get fhirClasses
        fhirClasses = TranslationUtilities.getFHIRClasses();
        
        # Get incoming and outgoing connections to each FHIR class.
        fhirConnections = TranslationUtilities.getFHIRConnections(fhirClasses);
        
        # Prepare lists of classes and children.
        ehrClassesToChildren = {};
        # Get outgoing connections of each ehrClass.
        ehrClassesToParents = {}
        
        for ehrClass in ehrClasses:
            
            children = TranslationUtilities.getEHRClassChildren(patientXML, ehrClass, True, False);
            if len(children):
                ehrClassesToChildren[ehrClass] = children;
                
            parents = TranslationUtilities.getEHRClassChildren(patientXML, ehrClass, False, True);
            if len(parents):
                ehrClassesToParents[ehrClass] = parents;
        
        fhirClassesToChildren = {};
        
        for fhirClass in fhirClasses:
            
            children = TranslationUtilities.getFHIRClassChildren(fhirClass, False);
            
            if ( children != None ):
                fhirClassesToChildren[fhirClass] = children;
        
        # Remove EHR classes and FHIR classes that do not have children (typically 'type' classes in FHIR).
        ehrClasses = set(ehrClassesToChildren.keys());
        fhirClasses = fhirClassesToChildren.keys();
        
        FHIRTranslation.matchStageOne(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections);
        
    # Match stage 1: Exact FHIR terms that are contained in the EHR term        
    @staticmethod
    def matchStageOne(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections):
        
        # Match components of patient record from EHR to components from JSON representation
        ehrFHIRMatches = {};
        
        ehrClassesToRemove = set();
        
        for ehrClass in ehrClasses: 
            
            matches = 0;
            
            for fhirClass in fhirClasses:
                
                if SimilarityMetrics.compositeStringSimilarity(ehrClass, str(fhirClass.__name__), SimilarityMetrics.textSimilarity, True) == 1.0:
                    matches += 1;
                    fhirMatch = fhirClass;
            
            # If there is only one 100% match between an EHR Class and FHIR Class, we take this as the best candidate, and remove the EHR class from the pool.
            if matches == 1:
                ehrFHIRMatches[ehrClass] = [(fhirMatch, FHIRTranslation.childSimilarity(ehrClass, fhirMatch, ehrClassesToChildren, fhirClassesToChildren))];
                ehrClassesToRemove.add(ehrClass);
        
        ehrClasses = ehrClasses - ehrClassesToRemove;
        
        FHIRTranslation.matchStageTwo(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches);
    
    # Match Stage 2: Child matches   
    @staticmethod
    def matchStageTwo(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches):
        
        for ehrClass in ehrClasses:
            
            ehrFHIRMatches[ehrClass] = [];
            
            childMatches = [];
            
            for fhirClass in fhirClasses:
                
                childSimilarity = FHIRTranslation.childSimilarity(ehrClass, fhirClass, None, fhirClassesToChildren, FHIRTranslation.getPatient("4917111072"));
                                
                childMatches.append((fhirClass, childSimilarity));
                
            childMatches = sorted(childMatches, key=lambda sortable: (sortable[1]), reverse=True);
            
            for childMatch in childMatches:
                
                if ( childMatch[1] > TranslationConstants.CHILD_MATCH_THRESHOLD ):
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
                    
        FHIRTranslation.matchStageThree(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches);
    
    # Match Stage 3: Fuzzy parent matches
    @staticmethod
    def matchStageThree(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches):
            
        # Now decide between multiples matches based upon names of parent classes.
        for ehrClass in ehrFHIRMatches:
            
            # Convert EHR to FHIR class matches to include similarity of parent class names.
            fhirClassChildParentSimilarity = [];
            
            # For each matching FHIR class to this EHR class
            for fhirClassChildSimilarity in ehrFHIRMatches[ehrClass]:
                
                similarity = Matches.match(ehrClass, fhirClassChildSimilarity[0].__name__);
                asList = list(fhirClassChildSimilarity)
                # Add the parent similarity to the child similarity to get an overall similarity value.
                asList[1] = asList[1] + similarity;
                fhirClassChildSimilarity = tuple(asList)
                fhirClassChildParentSimilarity.append(fhirClassChildSimilarity);
            
            ehrFHIRMatches[ehrClass] = fhirClassChildParentSimilarity;              
        
        FHIRTranslation.matchStageFour(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches);
    
    # Match Stage 4: Replicating connections
    @staticmethod
    def matchStageFour(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches):
        
        ehrFHIRCommonConnections = {};
         
        for ehrClass in ehrClassesToParents.keys():
            
            for fhirClass in fhirClasses:
                
                if fhirClass in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;
                
                # If any of the outgoing connections from the EHR class (child, parent elements) now have FHIR matches, see if that set of convertible connections corresponds to the connections (incoming and outgoing) of this FHIR class. Add this result to the child similarity.
                commonConnections = 0;
                
                for outgoingChild in ehrClassesToParents[ehrClass]:
                    
                    if outgoingChild in ehrFHIRMatches.keys():
                        
                        if fhirClass not in fhirConnections.keys() or ehrClass not in ehrFHIRMatches: continue;
                        
                        for connection in [fhirConnection[0] for fhirConnection in fhirConnections[fhirClass]]:
                            
                            if ehrFHIRMatches[outgoingChild][0][0] == connection:
                                
                                commonConnections += 1;
                                print str(outgoingChild) + " is a child of " + str(ehrClass) + ". " + str(outgoingChild) + " has been matched to " + str(ehrFHIRMatches[outgoingChild][0][0]) + " in FHIR, connecting the two. " + str(fhirClass) + " is also connected to " + str(connection) + ", so " + str(ehrClass) + " and " + str(fhirClass.__name__) + " are related.";
                                
                                # See if other classes that are children of this EHR element, and have resolved FHIR connections, would be linked to from this mutual connection, thus strengthening the connection between the relationship. 
                                #for outgoingChildSibling in ehrClassesToParents[ehrClass]:
                                    
                                    #if outgoingChildSibling in ehrFHIRMatches.keys():
                                        
                                        #for additionalConnection in [fhirConnection[0] for fhirConnection in fhirConnections[connection]]:
                                            
                                            #if 
                                
                                if (ehrClass, fhirClass) in ehrFHIRCommonConnections.keys():
                                    ehrFHIRCommonConnections[(ehrClass, fhirClass)] = ehrFHIRCommonConnections[(ehrClass, fhirClass)] + 1;
                                
                                else:
                                    ehrFHIRCommonConnections[(ehrClass, fhirClass)] = 1;
                                    
        FHIRTranslation.printMatches(ehrFHIRMatches, ehrClassesToChildren, fhirClassesToChildren);                           
        
    @staticmethod
    def printMatches(ehrFHIRMatches, ehrClassesToChildren, fhirClassesToChildren):
              
        # Handle two EHR classes matching to the same FHIR class. OK if they don't have overlapping fields.                        
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
                        matchStrength = Matches.match(ehrChild, fhirChild[0], TranslationConstants.TEXT_SIMILARITY_WEIGHTING,  TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING,  TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True)
                        
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
