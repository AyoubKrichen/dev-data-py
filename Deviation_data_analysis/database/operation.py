import sys
sys.path.append('..')

from sqlalchemy import create_engine as ce, Column, Float, Integer
from database.database_models import Train_data, Test_data, Ideal_func
import pandas as pd


class DataProcessor:
    def __init__(self):
        self.df_ideal = None
        self.df_train = None
        self.df_test = None

    def generating_columns(self):
        """
        Dynamically generates 'y' columns for Ideal_func, Train_data, and Test_data classes.
        """
        # Generating Y columns for each ideal function
        for i in range(1,51): 
            setattr(Ideal_func, 'y{}'.format(i),Column(Float))

        # Generating Y columns for each train function
        for i in range(1,5): 
            setattr(Train_data, 'y{}'.format(i),Column(Float))

        # Generating Y column for test function
        for i in range(1,4): 
            setattr(Test_data, 'y{}'.format(i),Column(Float))

    def data_loading(self):
        """
        Loads data from CSV files into pandas DataFrames.
        """
        self.df_ideal = pd.read_csv("data/ideal.csv")
        self.df_train = pd.read_csv("data/train.csv")
        self.df_test = pd.read_csv("data/test.csv")
        return self.df_ideal, self.df_train, self.df_test
    
    def get_dataframes(self):
        """
        Returns the loaded dataframes for ideal, train, and test data.
        """
        return self.df_ideal, self.df_train, self.df_test

# Example usage
if __name__ == "__main__":
    # Create a DataProcessor instance
    data_processor = DataProcessor()

    # Generate columns dynamically
    data_processor.generate_columns()

    # Load data from CSV files
    data_processor.load_data()

    # Retrieve dataframes
    df_ideal, df_train, df_test = data_processor.get_dataframes()

