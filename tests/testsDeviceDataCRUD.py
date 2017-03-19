# Test suite
import unittest
import sqlalchemy
import models
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, DeviceData, Device, DeviceType, Sensor, SensorType

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
        dd1 = DeviceData(value=10.0, datetimeRead=datetime.datetime.now())
        self.session.add(dd1)
        self.session.commit()

        # Check if inserted
        dd = self.session.query(DeviceData).filter_by(value=10.0).first()
        self.assertEquals(dd.value, dd1.value)

        # Check for non insertion
        dd = self.session.query(DeviceData).filter_by(value=99.0).first()
        self.assertTrue(dd is None)

        # Check Update
        dd = self.session.query(DeviceData).filter_by(value=10.0).first()
        dd.value = 20.0
        self.session.commit()
        ddTst = self.session.query(DeviceData).filter_by(value=20.0).first()
        self.assertEquals(ddTst.value, 20.0)

        # Check printout (to see this you have to run nosetest --nocapture
        dd = self.session.query(DeviceData).filter_by(value=20.0).first()
        print('DeviceData = %s' % dd)

        # Insert a second record and check insertion
        dd2 = DeviceData(value=100.0)
        self.session.add(dd2)
        self.session.commit()
        dd = self.session.query(DeviceData).filter_by(value=100.0).first()
        self.assertEquals(dd.value, dd2.value)

        # Rollback test
        dd3 = DeviceData(value=1000.0)
        self.session.add(dd3)
        self.session.rollback()
        dd = self.session.query(DeviceData).filter_by(value=1000.0).first()
        self.assertTrue(dd is None)

        # Delete record
        dd = self.session.query(DeviceData).filter_by(value=100.0).first()
        self.session.delete(dd)
        self.session.commit()
        self.assertTrue(self.session.query(DeviceData).filter_by(value=100.0).count()==0)

        # Add to device data data read from a device
        sensorType1 = SensorType(code='sensorType1', description='SENSORTYPEDESCR1')
        sensorType2 = SensorType(code='sensorType2', description='SENSORTYPEDESCR2')
        deviceType1 = DeviceType(code='deviceType1', description='DEVICETYPEDESCR1')
        deviceType2 = DeviceType(code='deviceType2', description='DEVICETYPEDESCR2')
        sensor11 = Sensor(code='sensor11', description='SENSORDESCR11', sensorType=sensorType1)
        sensor12 = Sensor(code='sensor12', description='SENSORDESCR12', sensorType=sensorType2)
        sensor21 = Sensor(code='sensor21', description='SENSORDESCR21', sensorType=sensorType1)
        sensor22 = Sensor(code='sensor22', description='SENSORDESCR22', sensorType=sensorType2)
        device1 = Device(code='device1', description='DEVICEDESCR1',\
                         deviceType=deviceType1)
        device1.sensors.append(sensor11)
        device1.sensors.append(sensor12)
        device2 = Device(code='device2', description='DEVICEDESCR2',\
                         deviceType=deviceType2)
        device2.sensors.append(sensor21)
        device2.sensors.append(sensor22)
        deviceData11=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=11.0,\
                               device=device1)
        deviceData12=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=12.0,\
                               device=device1)
        deviceData21=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=21.0,\
                               device=device2,)
        deviceData22=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=22.0,\
                               device=device2)
        self.session.add(deviceData11)
        self.session.add(deviceData12)
        self.session.add(deviceData21)
        self.session.add(deviceData22)
        self.session.commit()
        # Print data inserted
        devicedatas = self.session.query(DeviceData)
        for dd in devicedatas:
            print('Device Data : %s'%dd)
            print('\tDevice : %s'%dd.device)
            if dd.device is not None and dd.device.sensors is not None:
                for sens in dd.device.sensors:
                    print('\t\tSensor : %s'%sens)

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
        dd1 = DeviceData(value=10.0, datetimeRead=datetime.datetime.now())
        self.session.add(dd1)
        self.session.commit()

        # Check if inserted
        dd = self.session.query(DeviceData).filter_by(value=10.0).first()
        self.assertEquals(dd.value, dd1.value)

        # Check for non insertion
        dd = self.session.query(DeviceData).filter_by(value=99.0).first()
        self.assertTrue(dd is None)

        # Check Update
        dd = self.session.query(DeviceData).filter_by(value=10.0).first()
        dd.value = 20.0
        self.session.commit()
        ddTst = self.session.query(DeviceData).filter_by(value=20.0).first()
        self.assertEquals(ddTst.value, 20.0)

        # Check printout (to see this you have to run nosetest --nocapture
        dd = self.session.query(DeviceData).filter_by(value=20.0).first()
        print('DeviceData = %s' % dd)

        # Insert a second record and check insertion
        dd2 = DeviceData(value=100.0)
        self.session.add(dd2)
        self.session.commit()
        dd = self.session.query(DeviceData).filter_by(value=100.0).first()
        self.assertEquals(dd.value, dd2.value)

        # Rollback test
        dd3 = DeviceData(value=1000.0)
        self.session.add(dd3)
        self.session.rollback()
        dd = self.session.query(DeviceData).filter_by(value=1000.0).first()
        self.assertTrue(dd is None)

        # Delete record
        dd = self.session.query(DeviceData).filter_by(value=100.0).first()
        self.session.delete(dd)
        self.session.commit()
        self.assertTrue(self.session.query(DeviceData).filter_by(value=100.0).count()==0)

        # Add to device data data read from a device
        sensorType1 = SensorType(code='sensorType1', description='SENSORTYPEDESCR1')
        sensorType2 = SensorType(code='sensorType2', description='SENSORTYPEDESCR2')
        deviceType1 = DeviceType(code='deviceType1', description='DEVICETYPEDESCR1')
        deviceType2 = DeviceType(code='deviceType2', description='DEVICETYPEDESCR2')
        sensor11 = Sensor(code='sensor11', description='SENSORDESCR11', sensorType=sensorType1)
        sensor12 = Sensor(code='sensor12', description='SENSORDESCR12', sensorType=sensorType2)
        sensor21 = Sensor(code='sensor21', description='SENSORDESCR21', sensorType=sensorType1)
        sensor22 = Sensor(code='sensor22', description='SENSORDESCR22', sensorType=sensorType2)
        device1 = Device(code='device1', description='DEVICEDESCR1',\
                         deviceType=deviceType1)
        device1.sensors.append(sensor11)
        device1.sensors.append(sensor12)
        device2 = Device(code='device2', description='DEVICEDESCR2',\
                         deviceType=deviceType2)
        device2.sensors.append(sensor21)
        device2.sensors.append(sensor22)
        deviceData11=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=11.0,\
                               device=device1)
        deviceData12=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=12.0,\
                               device=device1)
        deviceData21=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=21.0,\
                               device=device2,)
        deviceData22=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=22.0,\
                               device=device2)
        self.session.add(deviceData11)
        self.session.add(deviceData12)
        self.session.add(deviceData21)
        self.session.add(deviceData22)
        self.session.commit()
        # Print data inserted
        devicedatas = self.session.query(DeviceData)
        for dd in devicedatas:
            print('Device Data : %s'%dd)
            print('\tDevice : %s'%dd.device)
            if dd.device is not None and dd.device.sensors is not None:
                for sens in dd.device.sensors:
                    print('\t\tSensor : %s'%sens)

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
        dd1 = DeviceData(value=10.0, datetimeRead=datetime.datetime.now())
        self.session.add(dd1)
        self.session.commit()

        # Check if inserted
        dd = self.session.query(DeviceData).filter_by(value=10.0).first()
        self.assertEquals(dd.value, dd1.value)

        # Check for non insertion
        dd = self.session.query(DeviceData).filter_by(value=99.0).first()
        self.assertTrue(dd is None)

        # Check Update
        dd = self.session.query(DeviceData).filter_by(value=10.0).first()
        dd.value = 20.0
        self.session.commit()
        ddTst = self.session.query(DeviceData).filter_by(value=20.0).first()
        self.assertEquals(ddTst.value, 20.0)

        # Check printout (to see this you have to run nosetest --nocapture
        dd = self.session.query(DeviceData).filter_by(value=20.0).first()
        print('DeviceData = %s' % dd)

        # Insert a second record and check insertion
        dd2 = DeviceData(value=100.0)
        self.session.add(dd2)
        self.session.commit()
        dd = self.session.query(DeviceData).filter_by(value=100.0).first()
        self.assertEquals(dd.value, dd2.value)

        # Rollback test
        dd3 = DeviceData(value=1000.0)
        self.session.add(dd3)
        self.session.rollback()
        dd = self.session.query(DeviceData).filter_by(value=1000.0).first()
        self.assertTrue(dd is None)

        # Delete record
        dd = self.session.query(DeviceData).filter_by(value=100.0).first()
        self.session.delete(dd)
        self.session.commit()
        self.assertTrue(self.session.query(DeviceData).filter_by(value=100.0).count()==0)

        # Add to device data data read from a device
        sensorType1 = SensorType(code='sensorType1', description='SENSORTYPEDESCR1')
        sensorType2 = SensorType(code='sensorType2', description='SENSORTYPEDESCR2')
        deviceType1 = DeviceType(code='deviceType1', description='DEVICETYPEDESCR1')
        deviceType2 = DeviceType(code='deviceType2', description='DEVICETYPEDESCR2')
        sensor11 = Sensor(code='sensor11', description='SENSORDESCR11', sensorType=sensorType1)
        sensor12 = Sensor(code='sensor12', description='SENSORDESCR12', sensorType=sensorType2)
        sensor21 = Sensor(code='sensor21', description='SENSORDESCR21', sensorType=sensorType1)
        sensor22 = Sensor(code='sensor22', description='SENSORDESCR22', sensorType=sensorType2)
        device1 = Device(code='device1', description='DEVICEDESCR1',\
                         deviceType=deviceType1)
        device1.sensors.append(sensor11)
        device1.sensors.append(sensor12)
        device2 = Device(code='device2', description='DEVICEDESCR2',\
                         deviceType=deviceType2)
        device2.sensors.append(sensor21)
        device2.sensors.append(sensor22)
        deviceData11=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=11.0,\
                               device=device1)
        deviceData12=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=12.0,\
                               device=device1)
        deviceData21=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=21.0,\
                               device=device2,)
        deviceData22=DeviceData(datetimeRead=datetime.datetime.now(),\
                               value=22.0,\
                               device=device2)
        self.session.add(deviceData11)
        self.session.add(deviceData12)
        self.session.add(deviceData21)
        self.session.add(deviceData22)
        self.session.commit()
        # Print data inserted
        devicedatas = self.session.query(DeviceData)
        for dd in devicedatas:
            print('Device Data : %s'%dd)
            print('\tDevice : %s'%dd.device)
            if dd.device is not None and dd.device.sensors is not None:
                for sens in dd.device.sensors:
                    print('\t\tSensor : %s'%sens)
