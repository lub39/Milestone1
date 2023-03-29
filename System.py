from typing import Dict, List, Optional
from Bus import Bus
from Transformer import Transformer
from Line import Line
from Generator import Generator
import numpy as np

class System:

    def __init__(self, name: str):

        self.name: str = name

        self.buses_order: List[str] = list()
        self.buses: Dict[str, Bus] = dict()
        self.y_matrix: Dict = dict()

        self.lines: Dict[str, Line] = dict()
        self.transformers: Dict[str, Transformer] = dict()
        self.generators: Optional[Generator] = None

    def __add_bus(self, bus):
        if bus not in self.buses.keys():
            self.buses[bus] = Bus(bus)
            self.buses_order.append(bus)

    def add_transformer_element(self, name, bus1, bus2, p_rate, v1_rate, v2_rate, z_pct, xr_ratio):

        self.transformers[name] = Transformer(name, bus1, bus2, p_rate, v1_rate, v2_rate, z_pct, xr_ratio)
        self.transformers[name].calc_y()
        self.__add_bus(bus1)
        self.__add_bus(bus2)

        self.y_matrix[name] = self.transformers[name]

    def add_line_element(self, name: str, codeword: str, bus1, bus2, length, d, num_cond,
                 axaxis, ayaxis, bxaxis, byaxis, cxaxis, cyaxis):

        vbase = self.transformers[list(self.transformers.keys())[0]].v2_rate

        self.lines[name] = Line(name, codeword, bus1, bus2, length, d, num_cond,
                 axaxis, ayaxis, bxaxis, byaxis, cxaxis, cyaxis, vbase)
        self.lines[name].calc_y()
        self.__add_bus(bus1)
        self.__add_bus(bus2)
        self.y_matrix[name] = self.lines[name]

    def add_generator_element(self, name, bus1, p_rate):
        self.generators = Generator(name, bus1, p_rate)
        self.__add_bus(bus1)

    def build_y_matrix(self):
        self.y_matrix_new = np.zeros((len(self.buses_order), len(self.buses_order)), dtype='complex')
        for element_name, element in self.y_matrix.items():

            for row in element.buses:
                for col in element.buses:
                    index_row = self.buses[row].index
                    index_col = self.buses[col].index

                    self.y_matrix_new[index_row, index_col] = self.y_matrix_new[index_row, index_col] + element.y.loc[row, col]

    def print_y_matrix(self):
        print("Y-bus matrix:")
        i = 0
        while i < len(self.buses):
            j = 0
            print("\nRow " + str(i + 1))
            while j < len(self.buses):
                print(self.y_matrix_new[i][j])
                j += 1
            i = i + 1

    def setBusData(self, bus: str, bus_type: str, real_P: float, Q_or_V: float):
        self.buses[bus].setBusdata(bus_type, real_P, Q_or_V)







