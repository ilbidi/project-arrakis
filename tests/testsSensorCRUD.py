# Test suite
import unittest
import sqlalchemy
import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, Sensor, SensorType

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
        # Insert sensor type
        sensor1 = Sensor(code='sensor1', description='DESCRIPTION1')
        self.session.add(sensor1)
        self.session.commit()

        # Check if inserted
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        self.assertEquals(sensor.code, sensor1.code)

        # Check for non insertion
        sensor = self.session.query(Sensor).filter_by(code='sensorFake').first()
        self.assertTrue(sensor is None)

        # Check Update
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        sensor.description = 'DESCRIPTIONChg'
        self.session.commit()
        sensorTst = self.session.query(Sensor).filter_by(code='sensor1').first()
        self.assertEquals(sensorTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        print('Sensor = %s' % sensor)

        # Insert a second record and check insertion
        sensor2 = Sensor(code='sensor2', description='DESCRIPTION2')
        self.session.add(sensor2)
        self.session.commit()
        sensor = self.session.query(Sensor).filter_by(code='sensor2').first()
        self.assertEquals(sensor.code, sensor2.code)

        # Rollback test
        sensor3 = Sensor(code='sensor3', description='DESCRIPTION3')
        self.session.add(sensor3)
        self.session.rollback()
        sensor = self.session.query(Sensor).filter_by(code='sensor3').first()
        self.assertTrue(sensor is None)

        # Delete record
        sensor = self.session.query(Sensor).filter_by(code='sensor2').first()
        self.session.delete(sensor)
        self.session.commit()
        self.assertTrue(self.session.query(Sensor).filter_by(code='sensor2').count()==0)

        # Add a relation to a sensor type
        sensorType = SensorType(code='sensortype1', description='DESCRIPTIONST1');
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        sensor.sensorType = sensorType;
        self.session.commit()
        print('Sensor = %s' % sensor)
        self.assertEquals(self.session.query(Sensor).filter_by(code='sensor1').first()\
                        .sensorType.code, 'sensortype1')

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
        # Insert sensor type
        sensor1 = Sensor(code='sensor1', description='DESCRIPTION1')
        self.session.add(sensor1)
        self.session.commit()

        # Check if inserted
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        self.assertEquals(sensor.code, sensor1.code)

        # Check for non insertion
        sensor = self.session.query(Sensor).filter_by(code='sensorFake').first()
        self.assertTrue(sensor is None)

        # Check Update
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        sensor.description = 'DESCRIPTIONChg'
        self.session.commit()
        sensorTst = self.session.query(Sensor).filter_by(code='sensor1').first()
        self.assertEquals(sensorTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        print('Sensor = %s' % sensor)

        # Insert a second record and check insertion
        sensor2 = Sensor(code='sensor2', description='DESCRIPTION2')
        self.session.add(sensor2)
        self.session.commit()
        sensor = self.session.query(Sensor).filter_by(code='sensor2').first()
        self.assertEquals(sensor.code, sensor2.code)

        # Rollback test
        sensor3 = Sensor(code='sensor3', description='DESCRIPTION3')
        self.session.add(sensor3)
        self.session.rollback()
        sensor = self.session.query(Sensor).filter_by(code='sensor3').first()
        self.assertTrue(sensor is None)

        # Delete record
        sensor = self.session.query(Sensor).filter_by(code='sensor2').first()
        self.session.delete(sensor)
        self.session.commit()
        self.assertTrue(self.session.query(Sensor).filter_by(code='sensor2').count()==0)

        # Add a relation to a sensor type
        sensorType = SensorType(code='sensortype1', description='DESCRIPTIONST1');
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        sensor.sensorType = sensorType;
        self.session.commit()
        print('Sensor = %s' % sensor)
        self.assertEquals(self.session.query(Sensor).filter_by(code='sensor1').first()\
                        .sensorType.code, 'sensortype1')

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
        # Insert sensor type
        sensor1 = Sensor(code='sensor1', description='DESCRIPTION1')
        self.session.add(sensor1)
        self.session.commit()

        # Check if inserted
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        self.assertEquals(sensor.code, sensor1.code)

        # Check for non insertion
        sensor = self.session.query(Sensor).filter_by(code='sensorFake').first()
        self.assertTrue(sensor is None)

        # Check Update
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        sensor.description = 'DESCRIPTIONChg'
        self.session.commit()
        sensorTst = self.session.query(Sensor).filter_by(code='sensor1').first()
        self.assertEquals(sensorTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        print('Sensor = %s' % sensor)

        # Insert a second record and check insertion
        sensor2 = Sensor(code='sensor2', description='DESCRIPTION2')
        self.session.add(sensor2)
        self.session.commit()
        sensor = self.session.query(Sensor).filter_by(code='sensor2').first()
        self.assertEquals(sensor.code, sensor2.code)

        # Rollback test
        sensor3 = Sensor(code='sensor3', description='DESCRIPTION3')
        self.session.add(sensor3)
        self.session.rollback()
        sensor = self.session.query(Sensor).filter_by(code='sensor3').first()
        self.assertTrue(sensor is None)

        # Delete record
        sensor = self.session.query(Sensor).filter_by(code='sensor2').first()
        self.session.delete(sensor)
        self.session.commit()
        self.assertTrue(self.session.query(Sensor).filter_by(code='sensor2').count()==0)

        # Add a relation to a sensor type
        sensorType = SensorType(code='sensortype1', description='DESCRIPTIONST1');
        sensor = self.session.query(Sensor).filter_by(code='sensor1').first()
        sensor.sensorType = sensorType;
        self.session.commit()
        print('Sensor = %s' % sensor)
        self.assertEquals(self.session.query(Sensor).filter_by(code='sensor1').first()\
                        .sensorType.code, 'sensortype1')
        
