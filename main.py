from System import System
from Solution import Solution
from PowerFlow import PowerFlow

#   Defining the System

system_obj = System("SixNodeTransmission")

system_obj.add_generator_element("G1", "Bus1", 100)
system_obj.add_transformer_element("T1", "Bus1", "Bus2", 125, 20, 230, 0.085, 10)

system_obj.add_line_element("L2", "Partridge", "Bus2", "Bus3", 25, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L1", "Partridge", "Bus2", "Bus4", 10, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L3", "Partridge", "Bus3", "Bus5", 20, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L6", "Partridge", "Bus4", "Bus5", 35, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L4", "Partridge", "Bus4", "Bus6", 20, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L5", "Partridge", "Bus5", "Bus6", 10, 1.5, 2, 0, 0, 19.5, 0, 39, 0)

system_obj.add_transformer_element("T2", "Bus7", "Bus6", 200, 18, 230, 0.105, 12)

system_obj.add_generator_element("G2", "Bus7", 100)


# Y-bus matrix

system_obj.build_y_matrix()
system_obj.print_y_matrix()

# solution_obj = Solution(system_obj)
# solution_obj.build_y_matrix()
# solution_obj.print_y_matrix()

system_obj.setBusData("Bus1", "Swing Bus", 0, 0)
system_obj.setBusData("Bus2", "Load Bus", 0, 0)
system_obj.setBusData("Bus3", "Load Bus", 110, 50)
system_obj.setBusData("Bus4", "Load Bus", 100, 70)
system_obj.setBusData("Bus5", "Load Bus", 100, 65)
system_obj.setBusData("Bus6", "Load Bus", 0, 0)
system_obj.setBusData("Bus7", "Voltage Controlled Bus", 200, 1)


# Power Flow
PowerFlow(system_obj)
