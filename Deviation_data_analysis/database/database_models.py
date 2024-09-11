import sys
sys.path.append('..')
#Import sqlalchemy models
from sqlalchemy import create_engine as ce, Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd


Base = declarative_base()

class DatabaseManager:
    def __init__(self, database_url="sqlite:///output/py_assignment.db"):
        """
        Initializes the database manager with the provided database URL.
        """    
        self.database_url = database_url
        self.engine = None
        self.Session = None
    
    def session_creation(self):
        self.engine = ce(self.database_url)
        # Create the database table
        Base.metadata.create_all(self.engine)
        #  Insert data into the database
        self.Session = sessionmaker(bind=self.engine)
        return (self.engine, self.Session)

#Represents the IdealFunctions table in the database (table2)
class Ideal_func(Base):
    __tablename__ = 'usersIdeal'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    x = Column(Float)

#Represents the TrainFunctions table in the database (table1)
class Train_data(Base):
    __tablename__ = 'usersTrain'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    x = Column(Float)
    
#Represents the TestFunctions table in the database.
class Test_data(Base):
    __tablename__ = 'usersTest'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    x = Column(Float)


