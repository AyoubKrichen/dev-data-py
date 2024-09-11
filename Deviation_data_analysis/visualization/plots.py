
import sys
sys.path.append('..')

import math
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from processing.calculations import DataCalculation

class VisualizeData:
    
    def __init__(self, df_test, df_train, df_ideal):
        self.df_test = df_test
        self.df_train = df_train
        self.df_ideal = df_ideal

    def graph_line_2_funct(self, xdata_input, ydata1_input, ydata2_input, color1, color2, legend1, legend2):
        """
        Create a line graph for two functions.
        """
        graph = figure(width=500, height=500, x_axis_label='X', y_axis_label='Y', background_fill_color="#fafafa")
        graph.line(xdata_input, ydata1_input, line_width=2, color=color1, alpha=0.5, legend_label=legend1)
        graph.line(xdata_input, ydata2_input, line_width=2, color=color2, alpha=0.4, legend_label=legend2)
        graph.legend.location = "top_left"
        return graph

    def graph_patch(self, x_test, y_test, x_colored, y_colored, x_ideal, y_ideal, x_patch, y_patch, N_y_ideal):
        """
        Create a patch graph to visualize deviation.
        """
        graph = figure(width=500, height=500, x_axis_label='X', y_axis_label='Y', background_fill_color="#fafafa")
        graph.circle(x_test, y_test, size=3, color="purple", alpha=0.8, legend_label="test y")
        graph.legend.location = "top"
        graph.circle(x_colored, y_colored, size=5, color="red", alpha=1, legend_label="Mapped points")
        graph.multi_line(x_ideal, y_ideal, line_width=8, color="gray", alpha=0.8, legend_label="ideal " + N_y_ideal)
        graph.patch(x_patch, y_patch, color="gray", alpha=0.3, legend_label="ideal " + N_y_ideal)
        return graph

    def visualize(self):
        """
        Main function to visualize the test and ideal data with deviation.
        """
        # Prepare data for plotting
        data_calculation_instance = DataCalculation(self.df_test, self.df_train, self.df_ideal)
        ideal_funct_list,i_ideal_list,max_train_dev_list = data_calculation_instance.ideal_func_list()

        x_test = self.df_test["x"]
        y_test = self.df_test["y"]
        x_ideal = self.df_ideal["x"]
        x_colored = self.df_test.loc[self.df_test["Delta_Y_test"] > 0]["x"]
        y_colored = self.df_test.loc[self.df_test["Delta_Y_test"] > 0]["y"]

        y_ideal_train_list = []
        deviation_graphs_list = []

        # Create a graph for mapped points
        graph_test_4ideals = figure(width=500, height=500, x_axis_label='X', y_axis_label='Y', background_fill_color="#fafafa")
        graph_test_4ideals.circle(x_test, y_test, size=3, color="purple", alpha=0.8, legend_label="test y")
        graph_test_4ideals.legend.location = "top"
        graph_test_4ideals.circle(x_colored, y_colored, size=5, color="red", alpha=1, legend_label="Mapped points")

        for column in range(4):
            # Plot the training function and its corresponding ideal
            y_train = self.df_train["y{}".format(column + 1)]
            N_y_ideal = "y{}".format(i_ideal_list[column])
            y_ideal = self.df_ideal[N_y_ideal]
            
            y_ideal_train_list.append(
                self.graph_line_2_funct(
                    x_ideal, y_train, y_ideal, "red", "blue", f"train y{column + 1}", f"ideal {N_y_ideal}"
                )
            )

            # Show mapped points in each ideal function
            thickness = math.sqrt(2) / 2
            x_patch = np.concatenate([x_ideal, x_ideal[::-1]])
            y_patch = np.concatenate([y_ideal - thickness, (y_ideal + thickness)[::-1]])
            
            x_ideal_colored = self.df_test.loc[
                (self.df_test["Delta_Y_test"] > 0) & (self.df_test["N_ideal_funct"] == N_y_ideal)
            ]["x"]
            y_ideal_colored1 = self.df_test.loc[
                (self.df_test["Delta_Y_test"] > 0) & (self.df_test["N_ideal_funct"] == N_y_ideal)
            ]["y"]
            
            deviation_graphs_list.append(
                self.graph_patch(x_test, y_test, x_ideal_colored, y_ideal_colored1, 
                                 x_ideal, y_ideal, x_patch, y_patch, N_y_ideal)
            )

            # Add to the global graph
            graph_test_4ideals.multi_line(x_ideal, y_ideal, line_width=8, color="gray", alpha=0.8, legend_label="ideal " + N_y_ideal)
            graph_test_4ideals.patch(x_patch, y_patch, color="gray", alpha=0.3, legend_label="ideal " + N_y_ideal)

        # Create the grid layout with all graphs
        p = gridplot([y_ideal_train_list, deviation_graphs_list, [graph_test_4ideals]])
        output_file("output/data_visualization.html")
        show(p)

