# Test suite
import unittest
import sqlalchemy
import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, Device, DeviceType, Sensor, SensorType

# Test for in memory SQLite
class TestSQLiteMemory(unittest.TestCase):
    # Database definition (in memory sqlite)
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.session.rollback()
        Base.metadata.drop_all(self.engine)

    def testCRUD(self):
        # Insert device type
        device1 = Device(code='device1', description='DESCRIPTION1')
        self.session.add(device1)
        self.session.commit()

        # Check if inserted
        device = self.session.query(Device).filter_by(code='device1').first()
        self.assertEquals(device.code, device1.code)

        # Check for non insertion
        device = self.session.query(Device).filter_by(code='deviceFake').first()
        self.assertTrue(device is None)

        # Check Update
        device = self.session.query(Device).filter_by(code='device1').first()
        device.description = 'DESCRIPTIONChg'
        self.session.commit()
        deviceTst = self.session.query(Device).filter_by(code='device1').first()
        self.assertEquals(deviceTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        device = self.session.query(Device).filter_by(code='device1').first()
        print('Device = %s' % device)

        # Insert a second record and check insertion
        device2 = Device(code='device2', description='DESCRIPTION2')
        self.session.add(device2)
        self.session.commit()
        device = self.session.query(Device).filter_by(code='device2').first()
        self.assertEquals(device.code, device2.code)

        # Rollback test
        device3 = Device(code='device3', description='DESCRIPTION3')
        self.session.add(device3)
        self.session.rollback()
        device = self.session.query(Device).filter_by(code='device3').first()
        self.assertTrue(device is None)

        # Delete record
        device = self.session.query(Device).filter_by(code='device2').first()
        self.session.delete(device)
        self.session.commit()
        self.assertTrue(self.session.query(Device).filter_by(code='device2').count()==0)

        # Add a relation to a device type
        deviceType = DeviceType(code='devicetype1', description='DESCRIPTIONDT1');
        device = self.session.query(Device).filter_by(code='device1').first()
        device.deviceType = deviceType;
        self.session.commit()
        print('Device = %s' % device)
        self.assertEquals(self.session.query(Device).filter_by(code='device1').first()\
                        .deviceType.code, 'devicetype1')

        # Add list of sensors
        sensor1 = Sensor(code='sensor1', description='DESCRIPTIONS1', \
                         sensorType=SensorType(code='sensortype1', description='DESCRIPTIONST1'))
        sensor2 = Sensor(code='sensor2', description='DESCRIPTIONS2', \
                         sensorType=SensorType(code='sensortype2', description='DESCRIPTIONST2'))
        device.sensors.append(sensor1)
        device.sensors.append(sensor2)
        self.session.commit()
        # List sensors of a device
        device = self.session.query(Device).filter_by(code='device1').first()
        print('Device = %s' % device)
        for sensor in device.sensors:
            print('\tSensor = %s' % sensor)

# Test for SQLite on local file
class TestSQLiteOnFile(unittest.TestCase):
    # Database definition
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.session.rollback()
        Base.metadata.drop_all(self.engine)

    def testCRUD(self):
        # Insert device type
        device1 = Device(code='device1', description='DESCRIPTION1')
        self.session.add(device1)
        self.session.commit()

        # Check if inserted
        device = self.session.query(Device).filter_by(code='device1').first()
        self.assertEquals(device.code, device1.code)

        # Check for non insertion
        device = self.session.query(Device).filter_by(code='deviceFake').first()
        self.assertTrue(device is None)

        # Check Update
        device = self.session.query(Device).filter_by(code='device1').first()
        device.description = 'DESCRIPTIONChg'
        self.session.commit()
        deviceTst = self.session.query(Device).filter_by(code='device1').first()
        self.assertEquals(deviceTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        device = self.session.query(Device).filter_by(code='device1').first()
        print('Device = %s' % device)

        # Insert a second record and check insertion
        device2 = Device(code='device2', description='DESCRIPTION2')
        self.session.add(device2)
        self.session.commit()
        device = self.session.query(Device).filter_by(code='device2').first()
        self.assertEquals(device.code, device2.code)

        # Rollback test
        device3 = Device(code='device3', description='DESCRIPTION3')
        self.session.add(device3)
        self.session.rollback()
        device = self.session.query(Device).filter_by(code='device3').first()
        self.assertTrue(device is None)

        # Delete record
        device = self.session.query(Device).filter_by(code='device2').first()
        self.session.delete(device)
        self.session.commit()
        self.assertTrue(self.session.query(Device).filter_by(code='device2').count()==0)

        # Add a relation to a device type
        deviceType = DeviceType(code='devicetype1', description='DESCRIPTIONDT1');
        device = self.session.query(Device).filter_by(code='device1').first()
        device.deviceType = deviceType;
        self.session.commit()
        print('Device = %s' % device)
        self.assertEquals(self.session.query(Device).filter_by(code='device1').first()\
                        .deviceType.code, 'devicetype1')

        # Add list of sensors
        sensor1 = Sensor(code='sensor1', description='DESCRIPTIONS1', \
                         sensorType=SensorType(code='sensortype1', description='DESCRIPTIONST1'))
        sensor2 = Sensor(code='sensor2', description='DESCRIPTIONS2', \
                         sensorType=SensorType(code='sensortype2', description='DESCRIPTIONST2'))
        device.sensors.append(sensor1)
        device.sensors.append(sensor2)
        self.session.commit()
        # List sensors of a device
        device = self.session.query(Device).filter_by(code='device1').first()
        print('Device = %s' % device)
        for sensor in device.sensors:
            print('\tSensor = %s' % sensor)

# Test for mysql (tested on localhost with maria db)
class TestMySql(unittest.TestCase):
    # Database definition (be sure that the db name already exists in database)
    engine = create_engine('mysql://root:root@localhost/testsqlalchemy')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.session.rollback()
        Base.metadata.drop_all(self.engine)

    def testCRUD(self):
        # Insert device type
        device1 = Device(code='device1', description='DESCRIPTION1')
        self.session.add(device1)
        self.session.commit()

        # Check if inserted
        device = self.session.query(Device).filter_by(code='device1').first()
        self.assertEquals(device.code, device1.code)

        # Check for non insertion
        device = self.session.query(Device).filter_by(code='deviceFake').first()
        self.assertTrue(device is None)

        # Check Update
        device = self.session.query(Device).filter_by(code='device1').first()
        device.description = 'DESCRIPTIONChg'
        self.session.commit()
        deviceTst = self.session.query(Device).filter_by(code='device1').first()
        self.assertEquals(deviceTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        device = self.session.query(Device).filter_by(code='device1').first()
        print('Device = %s' % device)

        # Insert a second record and check insertion
        device2 = Device(code='device2', description='DESCRIPTION2')
        self.session.add(device2)
        self.session.commit()
        device = self.session.query(Device).filter_by(code='device2').first()
        self.assertEquals(device.code, device2.code)

        # Rollback test
        device3 = Device(code='device3', description='DESCRIPTION3')
        self.session.add(device3)
        self.session.rollback()
        device = self.session.query(Device).filter_by(code='device3').first()
        self.assertTrue(device is None)

        # Delete record
        device = self.session.query(Device).filter_by(code='device2').first()
        self.session.delete(device)
        self.session.commit()
        self.assertTrue(self.session.query(Device).filter_by(code='device2').count()==0)

        # Add a relation to a device type
        deviceType = DeviceType(code='devicetype1', description='DESCRIPTIONDT1');
        device = self.session.query(Device).filter_by(code='device1').first()
        device.deviceType = deviceType;
        self.session.commit()
        print('Device = %s' % device)
        self.assertEquals(self.session.query(Device).filter_by(code='device1').first()\
                        .deviceType.code, 'devicetype1')

        # Add list of sensors
        sensor1 = Sensor(code='sensor1', description='DESCRIPTIONS1', \
                         sensorType=SensorType(code='sensortype1', description='DESCRIPTIONST1'))
        sensor2 = Sensor(code='sensor2', description='DESCRIPTIONS2', \
                         sensorType=SensorType(code='sensortype2', description='DESCRIPTIONST2'))
        device.sensors.append(sensor1)
        device.sensors.append(sensor2)
        self.session.commit()
        # List sensors of a device
        device = self.session.query(Device).filter_by(code='device1').first()
        print('Device = %s' % device)
        for sensor in device.sensors:
            print('\tSensor = %s' % sensor)
