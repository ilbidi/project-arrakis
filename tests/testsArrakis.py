# Test suite arrakis
import unittest
import sqlalchemy
import arrakis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, SensorType, Sensor, DeviceType, Device, DeviceData
from arrakis import arrakis

# Test with sqllite in memory
class TestArrakisSQLiteMemory(unittest.TestCase):
    # Database definition (in memory sqlite)
    engine = create_engine('sqlite:///:memory:')

    def setUp(self):
        arrakis.Session.configure(bind=self.engine)
        arrakis.session = arrakis.Session()
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        arrakis.session.rollback()
        arrakis.session.close()
        Base.metadata.drop_all(self.engine)

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

        # Check errors in list
        data = arrakis.dictInput(input=None)
        self.assertFalse(data)
        data = arrakis.dictInput(input='')
        self.assertFalse(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00')
        self.assertFalse(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234')
        self.assertTrue(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234|FAIL')
        self.assertFalse(data)

    def testInsDataRead(self):
        #"""Test inserimento dati"""
        arrakis.insDataRead(arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234'))
        arrakis.insDataRead(arrakis.dictInput(input='EEFFGGHH|00|99DDEEFF|00|1234'))
        arrakis.insDataRead(arrakis.dictInput(input='EEFFGGHH|00|99GGHHJJ|00|1234'))
        # List all tables
        for instance in arrakis.session.query(SensorType).order_by(SensorType.id):
            print(instance)
        for instance in arrakis.session.query(DeviceType).order_by(DeviceType.id):
            print(instance)
        for instance in arrakis.session.query(Sensor).order_by(Sensor.id):
            print(instance)
        for instance in arrakis.session.query(Device).order_by(Device.id):
            print(instance)
        for instance in arrakis.session.query(DeviceData).order_by(DeviceData.id):
            print(instance)
        self.assertTrue(True)

# Test with sqllite on file
class TestArrakisSQLiteOnFile(unittest.TestCase):
    # Database definition (on file sqlite)
    engine = create_engine('sqlite:///test.db')

    def setUp(self):
        arrakis.Session.configure(bind=self.engine)
        arrakis.session = arrakis.Session()
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        arrakis.session.rollback()
        arrakis.session.close()
        Base.metadata.drop_all(self.engine)

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

        # Check errors in list
        data = arrakis.dictInput(input=None)
        self.assertFalse(data)
        data = arrakis.dictInput(input='')
        self.assertFalse(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00')
        self.assertFalse(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234')
        self.assertTrue(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234|FAIL')
        self.assertFalse(data)

    def testInsDataRead(self):
        #"""Test inserimento dati"""
        arrakis.insDataRead(arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234'))
        arrakis.insDataRead(arrakis.dictInput(input='EEFFGGHH|00|99DDEEFF|00|1234'))
        arrakis.insDataRead(arrakis.dictInput(input='EEFFGGHH|00|99GGHHJJ|00|1234'))
        # List all tables
        for instance in arrakis.session.query(SensorType).order_by(SensorType.id):
            print(instance)
        for instance in arrakis.session.query(DeviceType).order_by(DeviceType.id):
            print(instance)
        for instance in arrakis.session.query(Sensor).order_by(Sensor.id):
            print(instance)
        for instance in arrakis.session.query(Device).order_by(Device.id):
            print(instance)
        for instance in arrakis.session.query(DeviceData).order_by(DeviceData.id):
            print(instance)
        self.assertTrue(True)

# Test for mysql (tested on localhost with maria db)
class TestArrakisSQLiteMySql(unittest.TestCase):
    # Database definition (on file sqlite)
    engine = create_engine('mysql://root:root@localhost/testsqlalchemy')

    def setUp(self):
        arrakis.Session.configure(bind=self.engine)
        arrakis.session = arrakis.Session()
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        arrakis.session.rollback()
        arrakis.session.close()
        Base.metadata.drop_all(self.engine)

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

        # Check errors in list
        data = arrakis.dictInput(input=None)
        self.assertFalse(data)
        data = arrakis.dictInput(input='')
        self.assertFalse(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00')
        self.assertFalse(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234')
        self.assertTrue(data)
        data = arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234|FAIL')
        self.assertFalse(data)

    def testInsDataRead(self):
        #"""Test inserimento dati"""
        arrakis.insDataRead(arrakis.dictInput(input='AABBCCDD|00|99AABBCC|00|1234'))
        arrakis.insDataRead(arrakis.dictInput(input='EEFFGGHH|00|99DDEEFF|00|1234'))
        arrakis.insDataRead(arrakis.dictInput(input='EEFFGGHH|00|99GGHHJJ|00|1234'))
        # List all tables
        for instance in arrakis.session.query(SensorType).order_by(SensorType.id):
            print(instance)
        for instance in arrakis.session.query(DeviceType).order_by(DeviceType.id):
            print(instance)
        for instance in arrakis.session.query(Sensor).order_by(Sensor.id):
            print(instance)
        for instance in arrakis.session.query(Device).order_by(Device.id):
            print(instance)
        for instance in arrakis.session.query(DeviceData).order_by(DeviceData.id):
            print(instance)
        self.assertTrue(True)
