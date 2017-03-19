# Test suite arrakis
import unittest
import arrakis
from arrakis import arrakis

# Test
class TestArrakis(unittest.TestCase):
    # def setUp(self):

    # def tearDown(self):

    def testParse(self):
        tokens = arrakis.parseInput(input='A|B')
        print(tokens)
        self.assertEquals(tokens[0], 'A')
        self.assertEquals(tokens[1], 'B')
        print(arrakis.dictInput(input='A|B|C|D|E'))
        data = arrakis.dictInput(input='A|B|C|D|E')
        self.assertEquals(data['device'], 'A')
        self.assertEquals(data['deviceType'], 'B')
        self.assertEquals(data['sensor'], 'C')
        self.assertEquals(data['sensorType'], 'D')
        self.assertEquals(data['value'], 'E')

        # Check a read
        read1 = 'AABBCCDD|00|99AABBCC|00|1234'
        data = arrakis.dictInput(input=read1)
        self.assertEquals(data['device'], 'AABBCCDD')
        self.assertEquals(data['deviceType'], '00')
        self.assertEquals(data['sensor'], '99AABBCC')
        self.assertEquals(data['sensorType'], '00')
        self.assertEquals(data['value'], '1234')
