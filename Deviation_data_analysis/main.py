import sys
sys.path.append('..')

from database.database_models import Ideal_func, Test_data, Train_data, DatabaseManager
from database.operation import DataProcessor
from processing.calculations import DataCalculation
from sqlalchemy.ext.declarative import declarative_base
from visualization.plots import VisualizeData
# import bokeh modules 


Base = declarative_base()

# Initialization
if __name__ == "__main__":
    session_creation_instance = DatabaseManager()
    engine,Session = session_creation_instance.session_creation()

    data_processor_instance = DataProcessor()

    #Generating columns
    data_processor_instance.generating_columns()

    #Data reading
    df_ideal, df_train, df_test = data_processor_instance.data_loading()

    # #determine the 4 ideal functions/lists
    data_calculation_instance = DataCalculation(df_test, df_train, df_ideal)
    data_calculation_instance.ideal_func_list()
    data_calculation_instance.deviations_calculation()
    df_test = data_calculation_instance.df_test_update()

    df_ideal.to_sql('usersIdeal', engine, index=False, if_exists='replace')
    df_train.to_sql('usersTrain', engine, index=False, if_exists='replace')
    df_test.to_sql('usersTest', engine, index=False, if_exists='replace')

    #Visualize data
    visualizer = VisualizeData(df_test, df_train, df_ideal)
    visualizer.visualize()



