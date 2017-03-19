# Test suite
import unittest
import sqlalchemy
import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, User

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
        # Insert user
        user1 = User(name='user1', fullname='USER1', password = 'pwd')
        self.session.add(user1)
        self.session.commit()

        # Check if inserted
        user = self.session.query(User).filter_by(name='user1').first()
        self.assertEquals(user.name, user1.name)

        # Check for non insertion
        user = self.session.query(User).filter_by(name='userFake').first()
        self.assertTrue(user is None)

        # Check Update
        user = self.session.query(User).filter_by(name='user1').first()
        user.password = 'pwdChg'
        self.session.commit()
        userTst = self.session.query(User).filter_by(name='user1').first()
        self.assertEquals(userTst.password, 'pwdChg')

        # Check printout (to see this you have to run nosetest --nocapture
        user = self.session.query(User).filter_by(name='user1').first()
        print('User = %s'%user)

        # Insert a second record and check insertion
        user2 = User(name='user2', fullname='USER2', password = 'pwd')
        self.session.add(user2)
        self.session.commit()
        user = self.session.query(User).filter_by(name='user2').first()
        self.assertEquals(user.name, user2.name)

        # Rollback test
        user3 = User(name='user3', fullname='USER3', password = 'pwd')
        self.session.add(user3)
        self.session.rollback()
        user = self.session.query(User).filter_by(name='user3').first()
        self.assertTrue(user is None)

        # Delete record
        user = self.session.query(User).filter_by(name='user2').first()
        self.session.delete(user)
        self.session.commit()
        self.assertTrue(self.session.query(User).filter_by(name='user2').count()==0)

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
        # Insert user
        user1 = User(name='user1', fullname='USER1', password = 'pwd')
        self.session.add(user1)
        self.session.commit()

        # Check if inserted
        user = self.session.query(User).filter_by(name='user1').first()
        self.assertEquals(user.name, user1.name)

        # Check for non insertion
        user = self.session.query(User).filter_by(name='userFake').first()
        self.assertTrue(user is None)

        # Check Update
        user = self.session.query(User).filter_by(name='user1').first()
        user.password = 'pwdChg'
        self.session.commit()
        userTst = self.session.query(User).filter_by(name='user1').first()
        self.assertEquals(userTst.password, 'pwdChg')

        # Check printout (to see this you have to run nosetest --nocapture
        user = self.session.query(User).filter_by(name='user1').first()
        print('User = %s'%user)

        # Insert a second record and check insertion
        user2 = User(name='user2', fullname='USER2', password = 'pwd')
        self.session.add(user2)
        self.session.commit()
        user = self.session.query(User).filter_by(name='user2').first()
        self.assertEquals(user.name, user2.name)

        # Rollback test
        user3 = User(name='user3', fullname='USER3', password = 'pwd')
        self.session.add(user3)
        self.session.rollback()
        user = self.session.query(User).filter_by(name='user3').first()
        self.assertTrue(user is None)

        # Delete record
        user = self.session.query(User).filter_by(name='user2').first()
        self.session.delete(user)
        self.session.commit()
        self.assertTrue(self.session.query(User).filter_by(name='user2').count()==0)

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
        # Insert user
        user1 = User(name='user1', fullname='USER1', password = 'pwd')
        self.session.add(user1)
        self.session.commit()

        # Check if inserted
        user = self.session.query(User).filter_by(name='user1').first()
        self.assertEquals(user.name, user1.name)

        # Check for non insertion
        user = self.session.query(User).filter_by(name='userFake').first()
        self.assertTrue(user is None)

        # Check Update
        user = self.session.query(User).filter_by(name='user1').first()
        user.password = 'pwdChg'
        self.session.commit()
        userTst = self.session.query(User).filter_by(name='user1').first()
        self.assertEquals(userTst.password, 'pwdChg')

        # Check printout (to see this you have to run nosetest --nocapture
        user = self.session.query(User).filter_by(name='user1').first()
        print('User = %s'%user)

        # Insert a second record and check insertion
        user2 = User(name='user2', fullname='USER2', password = 'pwd')
        self.session.add(user2)
        self.session.commit()
        user = self.session.query(User).filter_by(name='user2').first()
        self.assertEquals(user.name, user2.name)

        # Rollback test
        user3 = User(name='user3', fullname='USER3', password = 'pwd')
        self.session.add(user3)
        self.session.rollback()
        user = self.session.query(User).filter_by(name='user3').first()
        self.assertTrue(user is None)

        # Delete record
        user = self.session.query(User).filter_by(name='user2').first()
        self.session.delete(user)
        self.session.commit()
        self.assertTrue(self.session.query(User).filter_by(name='user2').count()==0)
