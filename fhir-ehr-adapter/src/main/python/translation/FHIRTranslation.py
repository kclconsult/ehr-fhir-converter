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
    def childSimilarity(ehrClass, fhirClass, ehrClassesToChildren=None, fhirClassesToChildren=None, xml=None, linkedClasses=False, selectiveRecurse=TranslationConstants.SELECTIVE_RECURSE):
        
        if ( ehrClassesToChildren ):
            ehrClassChildren = ehrClassesToChildren[ehrClass];
        else:
            ehrClassChildren = TranslationUtilities.getEHRClassChildren(xml, ehrClass)[ehrClass]; #~MDC TODO: Deal with the fact that this now returns a dictionary.
        
        if ( fhirClassesToChildren ):
            fhirClassChildren = fhirClassesToChildren[fhirClass];  
        else:
            fhirClassChildren = TranslationUtilities.getFHIRClassChildren(fhirClass, linkedClasses, selectiveRecurse);
        
        if ( fhirClassChildren == None ): return 0;
        
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
                    matchStrength = Matches.match(ehrClassChild, fhirClassChildForMatch, SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [], TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True);
                    
                    #matchStrength = FHIRTranslation.match(ehrClassChild, fhirClassChild[0], TranslationConstants.OVERALL_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, TranslationConstants.OVERALL_CHILD_SIMILARITY_THRESHOLD, False);
                    
                    #print str(ehrClassChild) + " " + str(fhirClassChild) + " " + str(matchStrength);
                    
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
           
            #print str(totalChildMatches) + " " + str(totalChildMatches / float(len(ehrClassChildren))) + " " + str(averageMatchStrength) + " " + str(len(fhirClassChildren)) + " " + str(min(len(ehrClassChildren) / float(len(fhirClassChildren)), 1)) + " " + str((totalChildMatches / float(len(ehrClassChildren))) * averageMatchStrength);
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
            
        if (len(ehrClasses)): FHIRTranslation.translatePatientInit(ehrClasses, patientXML, True, TranslationConstants.SELECTIVE_RECURSE);
    
    @staticmethod
    def getFHIRClassesToChildren(fhirClasses=TranslationUtilities.getFHIRClasses(), fhirClassesRecurse=True, selectiveRecurse=TranslationConstants.SELECTIVE_RECURSE):
        
        fhirClassesToChildren = {};
        
        for fhirClass in fhirClasses:
            
            children = TranslationUtilities.getFHIRClassChildren(fhirClass, fhirClassesRecurse, selectiveRecurse);
            
            if ( children != None ):
                fhirClassesToChildren[fhirClass] = children;
        
        return fhirClassesToChildren;
    
    @staticmethod
    def translatePatientInit(ehrClasses, patientXML, fhirClassesRecurse, selectiveRecurse):
        
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
                ehrClassesToChildren = Utilities.mergeDicts([ehrClassesToChildren, children]);
            
            parents = TranslationUtilities.getEHRClassChildren(patientXML, ehrClass, False, True);
            if len(parents):
                ehrClassesToParents = Utilities.mergeDicts([ehrClassesToParents, parents]);
        
        fhirClassesToChildren = FHIRTranslation.getFHIRClassesToChildren(fhirClasses, selectiveRecurse);
        
        # Remove EHR classes and FHIR classes that do not have children (typically 'type' classes in FHIR).
        ehrClasses = set(ehrClassesToChildren.keys());
        fhirClasses = fhirClassesToChildren.keys();
            
        FHIRTranslation.matchStageOne(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, fhirClassesRecurse);
        
    # Match stage 1: Exact FHIR terms that are contained in the EHR term        
    @staticmethod
    def matchStageOne(ehrClasses, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, fhirClassesRecurse):
        
        # Match components of patient record from EHR to components from JSON representation
        ehrFHIRMatches = {};
        
        ehrClassesToRemove = set();
        
        for ehrClass in ehrClasses: 
            
            matches = 0;
            
            for fhirClass in fhirClasses:
                
                if SimilarityMetrics.compositeStringSimilarity(ehrClass, str(fhirClass.__name__), SimilarityMetrics.textSimilarity, [], True) == 1.0:
                    matches += 1;
                    fhirMatch = fhirClass;
            
            # If there is only one 100% match between an EHR Class and FHIR Class, we take this as the best candidate, and remove the EHR class from the pool.
            if matches == 1:
                ehrFHIRMatches[ehrClass] = [(fhirMatch, FHIRTranslation.childSimilarity(ehrClass, fhirMatch, ehrClassesToChildren, fhirClassesToChildren, None, fhirClassesRecurse))];
                ehrClassesToRemove.add(ehrClass);
        
        FHIRTranslation.matchStageTwo(ehrClassesToRemove, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, fhirClassesRecurse);
    
    # Match Stage 2: Child matches   
    @staticmethod
    def matchStageTwo(ehrClassesToRemove, ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches, fhirClassesRecurse):
        
        print str(ehrClassesToChildren) + " " + str(ehrClassesToParents);
        
        sys.exit();
        
        for ehrClass in ehrClassesToChildren.keys():
            
            if ehrClass in ehrClassesToRemove: continue;
            
            ehrFHIRMatches[ehrClass] = [];
            
            childMatches = [];
            
            for fhirClass in fhirClasses:
                
                childSimilarity = FHIRTranslation.childSimilarity(ehrClass, fhirClass, ehrClassesToChildren, fhirClassesToChildren, None, fhirClassesRecurse);
                                
                childMatches.append((fhirClass, childSimilarity));
                
            childMatches = sorted(childMatches, key=lambda sortable: (sortable[1]), reverse=True);
            
            for childMatch in childMatches:
                
                if ( childMatch[1] > TranslationConstants.CHILD_MATCH_THRESHOLD ):
                    ehrFHIRMatches[ehrClass].append(childMatch);
            
            # print str(ehrClass) + " " + str(childMatches);     
               
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
               
        FHIRTranslation.matchStageThree(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches);
    
    # Match Stage 3: Fuzzy parent matches
    @staticmethod
    def matchStageThree(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches):
            
        # Now decide between multiples matches based upon names of parent classes.
        for ehrClass in ehrFHIRMatches:
            
            # Convert EHR to FHIR class matches to include similarity of parent class names.
            fhirClassChildParentSimilarity = [];
            
            # For each matching FHIR class to this EHR class
            for fhirClassChildSimilarity in ehrFHIRMatches[ehrClass]:
                
                ehrClassParent = ehrClass;
                if Utilities.isNumber(ehrClass[len(ehrClass) - 1]): ehrClassParent = ehrClass[:-1];
                 
                similarity = Matches.fuzzyMatch(ehrClassParent, fhirClassChildSimilarity[0].__name__);
                asList = list(fhirClassChildSimilarity)
                # Add the parent similarity to the child similarity to get an overall similarity value.
                asList[1] = asList[1] + similarity;
                fhirClassChildSimilarity = tuple(asList)
                fhirClassChildParentSimilarity.append(fhirClassChildSimilarity);
            
            ehrFHIRMatches[ehrClass] = fhirClassChildParentSimilarity;              
        
        # Sort matches by highest.
        for ehrClass in ehrFHIRMatches:
            ehrFHIRMatches[ehrClass] = sorted(ehrFHIRMatches[ehrClass], key=lambda sortable: (sortable[1]), reverse=True);
        
        FHIRTranslation.matchStageFour(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches);
    
    # Match Stage 4: Replicating connections
    @staticmethod
    def matchStageFour(ehrClassesToChildren, ehrClassesToParents, fhirClasses, fhirClassesToChildren, fhirConnections, ehrFHIRMatches):
        
        ehrFHIRCommonConnections = {};
         
        for ehrClass in ehrClassesToParents.keys():
            
            print "==== " + str(ehrClass);
            
            for fhirClass in fhirClasses:
                
                if fhirClass in TranslationConstants.EXCLUDED_FHIR_CLASSES: continue;
                
                # If any of the outgoing connections from the EHR class (child, parent elements) now have FHIR matches, see if that set of convertible connections corresponds to the connections (incoming and outgoing) of this FHIR class. Add this result to the child similarity.
                commonConnections = 0;
                
                for outgoingChild in ehrClassesToParents[ehrClass]:
                    
                    if outgoingChild in ehrFHIRMatches.keys():
                        
                        if fhirClass not in fhirConnections.keys() or ehrClass not in ehrFHIRMatches: continue;
                        
                        for connection in [fhirConnection[0] for fhirConnection in fhirConnections[fhirClass]]:
                            
                            # Should probably consider other matches, if they are as equally strong.
                            if ehrFHIRMatches[outgoingChild][0][0] == connection:
                                
                                commonConnections += 1;
                                print str(outgoingChild) + " is a child of " + str(ehrClass) + ". " + str(outgoingChild) + " has been matched to " + str(ehrFHIRMatches[outgoingChild][0][0]) + " in FHIR, connecting the two. " + str(fhirClass) + " is also connected to " + str(connection) + ", so " + str(ehrClass) + " and " + str(fhirClass.__name__) + " are related.";
                                
                                print TranslationUtilities.recreatableConnections(outgoingChild, ehrClassesToParents[ehrClass], ehrFHIRMatches, fhirConnections);
                                
                                if (ehrClass, fhirClass) in ehrFHIRCommonConnections.keys():
                                    ehrFHIRCommonConnections[(ehrClass, fhirClass)] = ehrFHIRCommonConnections[(ehrClass, fhirClass)] + 1;
                                
                                else:
                                    ehrFHIRCommonConnections[(ehrClass, fhirClass)] = 1;
                                    
            print "====";
            
        sys.exit();                           
        FHIRTranslation.matchStageFive(ehrFHIRMatches, ehrClassesToChildren, fhirClassesToChildren);                           
    
    # Match Stage 5: Match EHR children to FHIR children from chosen class (and print results).
    @staticmethod
    def matchStageFive(ehrFHIRMatches, ehrClassesToChildren, fhirClassesToChildren):
              
        # Handle two EHR classes matching to the same FHIR class. OK if they don't have overlapping fields.                        
        for ehrClass in ehrFHIRMatches:
            
            print "===========================";
            print ehrClass;
            
            matches = ehrFHIRMatches[ehrClass];
            
            if len(matches):
                print matches;
            
                #
                children = fhirClassesToChildren[matches[0][0]]; # [:]
                
                ehrChildToHighestFHIRchild = {};
                
                # Find matches for each of the parent matches.
                for ehrChild in ehrClassesToChildren[ehrClass]:
                            
                    # Find the FHIR children of the top match. Extract the name of the FHIR class from each tuple.
                    for fhirChild in children:
                   
                        # Each child is a tuple with parent as second value.
                        matchStrength = Matches.match(ehrChild, fhirChild[0], SimilarityMetrics.textSimilarity, [], TranslationConstants.TEXT_SIMILARITY_WEIGHTING, SimilarityMetrics.semanticSimilarity, [], TranslationConstants.SEMANTIC_SIMILARITY_WEIGHTING, SimilarityMetrics.morphologicalSimilarity, [], TranslationConstants.MORPHOLOGICAL_SIMILARITY_WEIGHTING, 0, 0, 0, 0, False, False, True)
                        
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
