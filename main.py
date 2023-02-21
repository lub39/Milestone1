from System import System
from Solution import Solution

#   Defining the System

system_obj = System("SixNodeTransmission")

system_obj.add_generator_element("G1", "A", 100)
system_obj.add_transformer_element("T1", "A", "B", 125, 20, 230, 0.085, 10)

system_obj.add_line_element("L2", "Partridge", "B", "C", 25, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L1", "Partridge", "B", "D", 10, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L3", "Partridge", "C", "E", 20, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L6", "Partridge", "D", "E", 35, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L4", "Partridge", "D", "F", 20, 1.5, 2, 0, 0, 19.5, 0, 39, 0)
system_obj.add_line_element("L5", "Partridge", "E", "F", 10, 1.5, 2, 0, 0, 19.5, 0, 39, 0)

system_obj.add_transformer_element("T2", "G", "F", 200, 18, 230, 0.105, 12)

system_obj.add_generator_element("G2", "G", 100)


#   Printing z and y bus matrices

solution_obj = Solution(system_obj)
solution_obj.build_y_matrix()
solution_obj.print_y_matrix()
