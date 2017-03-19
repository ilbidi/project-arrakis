# Test suite
import unittest
import sqlalchemy
import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, SensorType

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
        st1 = SensorType(code='st1', description='DESCRIPTION1')
        self.session.add(st1)
        self.session.commit()

        # Check if inserted
        st = self.session.query(SensorType).filter_by(code='st1').first()
        self.assertEquals(st.code, st1.code)

        # Check for non insertion
        st = self.session.query(SensorType).filter_by(code='stFake').first()
        self.assertTrue(st is None)

        # Check Update
        st = self.session.query(SensorType).filter_by(code='st1').first()
        st.description = 'DESCRIPTIONChg'
        self.session.commit()
        stTst = self.session.query(SensorType).filter_by(code='st1').first()
        self.assertEquals(stTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        st = self.session.query(SensorType).filter_by(code='st1').first()
        print('SensorType = %s' % st)

        # Insert a second record and check insertion
        st2 = SensorType(code='st2', description='DESCRIPTION2')
        self.session.add(st2)
        self.session.commit()
        st = self.session.query(SensorType).filter_by(code='st2').first()
        self.assertEquals(st.code, st2.code)

        # Rollback test
        st3 = SensorType(code='st3', description='DESCRIPTION3')
        self.session.add(st3)
        self.session.rollback()
        st = self.session.query(SensorType).filter_by(code='st3').first()
        self.assertTrue(st is None)

        # Delete record
        st = self.session.query(SensorType).filter_by(code='st2').first()
        self.session.delete(st)
        self.session.commit()
        self.assertTrue(self.session.query(SensorType).filter_by(code='st2').count()==0)

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
        st1 = SensorType(code='st1', description='DESCRIPTION1')
        self.session.add(st1)
        self.session.commit()

        # Check if inserted
        st = self.session.query(SensorType).filter_by(code='st1').first()
        self.assertEquals(st.code, st1.code)

        # Check for non insertion
        st = self.session.query(SensorType).filter_by(code='stFake').first()
        self.assertTrue(st is None)

        # Check Update
        st = self.session.query(SensorType).filter_by(code='st1').first()
        st.description = 'DESCRIPTIONChg'
        self.session.commit()
        stTst = self.session.query(SensorType).filter_by(code='st1').first()
        self.assertEquals(stTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        st = self.session.query(SensorType).filter_by(code='st1').first()
        print('SensorType = %s' % st)

        # Insert a second record and check insertion
        st2 = SensorType(code='st2', description='DESCRIPTION2')
        self.session.add(st2)
        self.session.commit()
        st = self.session.query(SensorType).filter_by(code='st2').first()
        self.assertEquals(st.code, st2.code)

        # Rollback test
        st3 = SensorType(code='st3', description='DESCRIPTION3')
        self.session.add(st3)
        self.session.rollback()
        st = self.session.query(SensorType).filter_by(code='st3').first()
        self.assertTrue(st is None)

        # Delete record
        st = self.session.query(SensorType).filter_by(code='st2').first()
        self.session.delete(st)
        self.session.commit()
        self.assertTrue(self.session.query(SensorType).filter_by(code='st2').count()==0)

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
        st1 = SensorType(code='st1', description='DESCRIPTION1')
        self.session.add(st1)
        self.session.commit()

        # Check if inserted
        st = self.session.query(SensorType).filter_by(code='st1').first()
        self.assertEquals(st.code, st1.code)

        # Check for non insertion
        st = self.session.query(SensorType).filter_by(code='stFake').first()
        self.assertTrue(st is None)

        # Check Update
        st = self.session.query(SensorType).filter_by(code='st1').first()
        st.description = 'DESCRIPTIONChg'
        self.session.commit()
        stTst = self.session.query(SensorType).filter_by(code='st1').first()
        self.assertEquals(stTst.description, 'DESCRIPTIONChg')

        # Check printout (to see this you have to run nosetest --nocapture
        st = self.session.query(SensorType).filter_by(code='st1').first()
        print('SensorType = %s' % st)

        # Insert a second record and check insertion
        st2 = SensorType(code='st2', description='DESCRIPTION2')
        self.session.add(st2)
        self.session.commit()
        st = self.session.query(SensorType).filter_by(code='st2').first()
        self.assertEquals(st.code, st2.code)

        # Rollback test
        st3 = SensorType(code='st3', description='DESCRIPTION3')
        self.session.add(st3)
        self.session.rollback()
        st = self.session.query(SensorType).filter_by(code='st3').first()
        self.assertTrue(st is None)

        # Delete record
        st = self.session.query(SensorType).filter_by(code='st2').first()
        self.session.delete(st)
        self.session.commit()
        self.assertTrue(self.session.query(SensorType).filter_by(code='st2').count()==0)
