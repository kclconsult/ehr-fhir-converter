from mockito import mock, verify
import unittest, sys

import SMARTOnFHIRContainer

class FHIRServerTests(unittest.TestCase):
    
    def test_RunServer(self):
        
        #SMARTOnFHIRContainer.serve();
        self.assertTrue(True);