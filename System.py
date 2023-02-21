from typing import Dict, List, Optional
from Bus import Bus
from Transformer import Transformer
from Line import Line
from Generator import Generator


class System:

    def __init__(self, name: str):

        self.name: str = name

        self.buses_order: List[str] = list()
        self.buses: Dict[str, Bus] = dict()
        self.y_elements: Dict = dict()

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

        self.y_elements[name] = self.transformers[name]

    def add_line_element(self, name: str, codeword: str, bus1, bus2, length, d, num_cond,
                 axaxis, ayaxis, bxaxis, byaxis, cxaxis, cyaxis):

        vbase = self.transformers[list(self.transformers.keys())[0]].v2_rate

        self.lines[name] = Line(name, codeword, bus1, bus2, length, d, num_cond,
                 axaxis, ayaxis, bxaxis, byaxis, cxaxis, cyaxis, vbase)
        self.lines[name].calc_y()
        self.__add_bus(bus1)
        self.__add_bus(bus2)

        self.y_elements[name] = self.lines[name]
    def add_generator_element(self, name, bus1, p_rate):
        self.generators = Generator(name, bus1, p_rate)
        self.__add_bus(bus1)







