# Test suite
import unittest
import sqlalchemy
import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, DeviceType

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
        dt1 = DeviceType(code='dt1', description='DESCRIPTION1')
        self.session.add(dt1)
        self.session.commit()

        # Check if inserted
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        self.assertEquals(dt.code, dt1.code)

        # Check for non insertion
        dt = self.session.query(DeviceType).filter_by(code='dtFake').first()
        self.assertTrue(dt is None)

        # Check Update
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        dt.description = 'DESCRIPTIONChg'
        self.session.commit()
        dtTst = self.session.query(DeviceType).filter_by(code='dt1').first()
        self.assertEquals(dtTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        print('DeviceType = %s' % dt)

        # Insert a second record and check insertion
        dt2 = DeviceType(code='dt2', description='DESCRIPTION2')
        self.session.add(dt2)
        self.session.commit()
        dt = self.session.query(DeviceType).filter_by(code='dt2').first()
        self.assertEquals(dt.code, dt2.code)

        # Rollback test
        dt3 = DeviceType(code='dt3', description='DESCRIPTION3')
        self.session.add(dt3)
        self.session.rollback()
        dt = self.session.query(DeviceType).filter_by(code='dt3').first()
        self.assertTrue(dt is None)

        # Delete record
        dt = self.session.query(DeviceType).filter_by(code='dt2').first()
        self.session.delete(dt)
        self.session.commit()
        self.assertTrue(self.session.query(DeviceType).filter_by(code='dt2').count()==0)

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
        dt1 = DeviceType(code='dt1', description='DESCRIPTION1')
        self.session.add(dt1)
        self.session.commit()

        # Check if inserted
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        self.assertEquals(dt.code, dt1.code)

        # Check for non insertion
        dt = self.session.query(DeviceType).filter_by(code='dtFake').first()
        self.assertTrue(dt is None)

        # Check Update
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        dt.description = 'DESCRIPTIONChg'
        self.session.commit()
        dtTst = self.session.query(DeviceType).filter_by(code='dt1').first()
        self.assertEquals(dtTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        print('DeviceType = %s' % dt)

        # Insert a second record and check insertion
        dt2 = DeviceType(code='dt2', description='DESCRIPTION2')
        self.session.add(dt2)
        self.session.commit()
        dt = self.session.query(DeviceType).filter_by(code='dt2').first()
        self.assertEquals(dt.code, dt2.code)

        # Rollback test
        dt3 = DeviceType(code='dt3', description='DESCRIPTION3')
        self.session.add(dt3)
        self.session.rollback()
        dt = self.session.query(DeviceType).filter_by(code='dt3').first()
        self.assertTrue(dt is None)

        # Delete record
        dt = self.session.query(DeviceType).filter_by(code='dt2').first()
        self.session.delete(dt)
        self.session.commit()
        self.assertTrue(self.session.query(DeviceType).filter_by(code='dt2').count()==0)

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
        dt1 = DeviceType(code='dt1', description='DESCRIPTION1')
        self.session.add(dt1)
        self.session.commit()

        # Check if inserted
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        self.assertEquals(dt.code, dt1.code)

        # Check for non insertion
        dt = self.session.query(DeviceType).filter_by(code='dtFake').first()
        self.assertTrue(dt is None)

        # Check Update
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        dt.description = 'DESCRIPTIONChg'
        self.session.commit()
        dtTst = self.session.query(DeviceType).filter_by(code='dt1').first()
        self.assertEquals(dtTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        dt = self.session.query(DeviceType).filter_by(code='dt1').first()
        print('DeviceType = %s' % dt)

        # Insert a second record and check insertion
        dt2 = DeviceType(code='dt2', description='DESCRIPTION2')
        self.session.add(dt2)
        self.session.commit()
        dt = self.session.query(DeviceType).filter_by(code='dt2').first()
        self.assertEquals(dt.code, dt2.code)

        # Rollback test
        dt3 = DeviceType(code='dt3', description='DESCRIPTION3')
        self.session.add(dt3)
        self.session.rollback()
        dt = self.session.query(DeviceType).filter_by(code='dt3').first()
        self.assertTrue(dt is None)

        # Delete record
        dt = self.session.query(DeviceType).filter_by(code='dt2').first()
        self.session.delete(dt)
        self.session.commit()
        self.assertTrue(self.session.query(DeviceType).filter_by(code='dt2').count()==0)
