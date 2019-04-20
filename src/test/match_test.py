from mockito import mock, verify
from random import shuffle
from nltk.corpus import wordnet
import unittest, sys

from translation.matches import Matches
from utils.utilities import Utilities
from test.match_syntactic_dictionary import usToGB

class MatchTests(unittest.TestCase):

    def test_TestSyntactic(self):

        # e.g self.assertTrue(Matches.match("Organisation", "Organization"));

        matched = 0;
        for key, value in usToGB.items():
            if ( Matches.matches(key, value) ):
                matched += 1;
            else:
                print(str(key) + " " + str(value));
        matchPercentage = matched / float(len(usToGB.items()));
        print("Syntactic match percentage: " + str(matchPercentage));
        self.assertTrue(matchPercentage > 0.90);

    def test_TestMorphological(self):

        # e.g. self.assertTrue(Matches.match("PostCode", "postalCode"));

        total = 0;
        matched = 0;
        for key, value in usToGB.items():
            lemmas = list(Utilities.lemmas(value));
            if ( lemmas ):
                total += 1;
                shuffle(lemmas)
                if ( Matches.matches(value, lemmas[0]) ):
                    matched += 1;
                else:
                    print(str(value) + " " + str(lemmas[0]));
        matchPercentage = matched / float(total);
        self.assertTrue(matchPercentage > 0.90);

    def test_TestSemantic(self):

        # e.g. self.assertTrue(Matches.match("FirstName", "givenHumanName"));

        total = 0;
        matched = 0;
        for key, value in usToGB.items():
            for set in wordnet.synsets(key):
                synonyms = [synonym for synonym in list(set.lemma_names()) if not synonym == key];
                if ( synonyms ):
                    shuffle(synonyms)
                    if ( "_" not in synonyms[0] ):
                        total += 1;
                        if ( Matches.matches(value, synonyms[0]) ):
                            matched += 1;
                        else:
                            print(str(value) + " " + str(synonyms[0]));
                        break;
        matchPercentage = matched / float(total);
        self.assertTrue(matchPercentage > 0.90);
