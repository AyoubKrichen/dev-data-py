import sys
sys.path.append('..')

from database.operation import DataProcessor
import math
from bokeh.plotting import figure, output_file, show  
from bokeh.layouts import row
import pandas as pd

class DataCalculation:
    def __init__(self, df_test, df_train, df_ideal):
        self.df_test = df_test
        self.df_train = df_train
        self.df_ideal = df_ideal
        self.max_train_dev_dict = {}

    def ideal_func_list(self):
        """
        Identify the ideal functions and calculate the deviation between training and ideal functions.
        """
        df_4_ideal_functions = pd.DataFrame()
        train_columns_leng = len(self.df_train.columns)
        ideal_columns_leng = len(self.df_ideal.columns)
        ideal_funct_list = []
        i_ideal_list = []

        for column_i in range(1, train_columns_leng):
            # Determine the 4 ideal functions
            min_sum = float("inf")
            i_ideal = 0
            for i in range(1, ideal_columns_leng):
                column_train = self.df_train["y{}".format(column_i)] 
                column_ideal = self.df_ideal["y{}".format(i)]
                sum_diff = ((column_train -column_ideal)**2).sum()

                if sum_diff < min_sum: 
                    min_sum = sum_diff
                    i_ideal = i
            
            y_i_ideal = "y{}".format(i_ideal)
            ideal_funct_list.append(min_sum)
            i_ideal_list.append(i_ideal)
            df_4_ideal_functions[y_i_ideal] = self.df_ideal[y_i_ideal]

            # Calculate deviation between the 4 ideal functions and the training data
            column_ideal = df_4_ideal_functions[y_i_ideal]
            column_train = self.df_train["y{}".format(column_i)]
            max_difference = abs(column_ideal - column_train).max()
            self.max_train_dev_dict[y_i_ideal] = max_difference

        return ideal_funct_list, i_ideal_list, self.max_train_dev_dict

    def deviations_calculation(self):
        """
        Calculate the deviations between test data and ideal functions.
        """
        ideal_func_calculated = False
        if not ideal_func_calculated:
            ideal_funct_list, i_ideal_list, self.max_train_dev_dict = self.ideal_func_list()
            ideal_func_calculated = True
        
        self.min_test_dev_list = []
        self.no_ideal_funct_list = []
        ideal_ts_dev = {}
        min_test_dev_list_non0 = []
        test_rows_leng = len(self.df_test.index)

        for test_row in range(test_rows_leng):
            # Calculate deviation between test (B) and the 4 ideal functions (C)
            min_test_dev = float("inf")
            j1 = self.df_train.loc[self.df_train["x"] == self.df_test["x"][test_row]].index[0]
            
            for i in range(4):
                dev_key = "x{}y{}".format(test_row, i)
                ideal_ts_dev[dev_key] = abs(self.df_test["y"][test_row] - self.df_ideal["y{}".format(i_ideal_list[i])][j1])
                dev_num = ideal_ts_dev[dev_key]
                
                if min_test_dev > dev_num:
                    min_test_dev = dev_num
                    y_dev = "y{}".format(i_ideal_list[i])
                    i_dev = i

            y_deviation = "y{}".format(i_ideal_list[i_dev])

            # Verify if the test deviation is valid
            if min_test_dev <= self.max_train_dev_dict[y_deviation] * math.sqrt(2):
                self.min_test_dev_list.append(min_test_dev)
                self.no_ideal_funct_list.append(y_dev)
            else:
                self.min_test_dev_list.append(None)
                self.no_ideal_funct_list.append(None)

            min_test_dev_list_non0.append(min_test_dev)

        print("self.min_test_dev_list", self.min_test_dev_list)
        return self.min_test_dev_list, self.no_ideal_funct_list, self.max_train_dev_dict, min_test_dev_list_non0

    def df_test_update(self):
        """
        Update the test DataFrame by adding the 'Delta_Y_test' and 'N_ideal_funct' columns.
        """
        self.deviations_calculation()  # Ensure deviations_calculation runs only once
        self.df_test = self.df_test.assign(Delta_Y_test=self.min_test_dev_list, N_ideal_funct=self.no_ideal_funct_list)
        return self.df_test

if __name__ == "__main__":
    # Create an instance of the DataCalculation class
    data_calculation_instance = DataCalculation()

    # Perform calculations and update DataFrame
    df_updated = data_calculation_instance.df_test_update()
















