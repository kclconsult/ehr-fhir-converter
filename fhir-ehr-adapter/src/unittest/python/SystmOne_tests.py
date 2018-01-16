from mockito import mock, verify
import unittest,sys

sys.path.append('src/main/python/SMARTOnFHIRContainer')

from EHR.SystmOne import SystmOne

class SystmOneTests(unittest.TestCase):
    
    def test_GetPatientRecord(self):
        
        self.assertTrue(len(str(SystmOne.getPatientRecord("1234"))) > 0);
