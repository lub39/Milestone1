from System import System
import numpy as np


class Solution:

    def __init__(self, system: System):
        self.system = system

    def build_y_matrix(self):
        self.y_matrix = np.zeros((len(self.system.buses), len(self.system.buses)), dtype='complex')
        self.bus_order = list()

        for element_name, element in self.system.y_elements.items():

            for row in element.buses:
                for col in element.buses:
                    index_row = self.system.buses[row].index
                    index_col = self.system.buses[col].index

                    self.y_matrix[index_row, index_col] = self.y_matrix[index_row, index_col] + element.y.loc[row, col]

    def print_y_matrix(self):
        print("Y-bus matrix:")
        i = 0
        while i < len(self.system.buses):
            j = 0
            print("\nRow " + str(i + 1))
            while j < len(self.system.buses):
                print(self.y_matrix[i][j])
                j += 1
            i = i + 1
