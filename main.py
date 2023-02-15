from System import System
from Solution import Solution

#   Defining the System

system_obj = System("SixNodeTransmission")

system_obj.add_generator_element("G1", "A", 100)
system_obj.add_generator_element("G2", "G", 100)

system_obj.add_transformer_element("T1", "A", "B", 100, 125, 0.085, 10)
system_obj.add_transformer_element("T2", "G", "F", 100, 200, 0.105, 12)

system_obj.add_line_element("L1", "B", "D", 10, 60, 0.0394/12, 0.0217, 1.5, 0.385, 2, 19.5, 19.5, 39)
system_obj.add_line_element("L2", "B", "C", 25, 60, 0.0394/12, 0.0217, 1.5, 0.385, 2, 19.5, 19.5, 39)
system_obj.add_line_element("L3", "C", "E", 20, 60, 0.0394/12, 0.0217, 1.5, 0.385, 2, 19.5, 19.5, 39)
system_obj.add_line_element("L4", "D", "F", 20, 60, 0.0394/12, 0.0217, 1.5, 0.385, 2, 19.5, 19.5, 39)
system_obj.add_line_element("L5", "E", "F", 10, 60, 0.0394/12, 0.0217, 1.5, 0.385, 2, 19.5, 19.5, 39)
system_obj.add_line_element("L6", "D", "E", 35, 60, 0.0394/12, 0.0217, 1.5, 0.385, 2, 19.5, 19.5, 39)

#   Printing z and y bus matrices

solution_obj = Solution(system_obj)
solution_obj.build_y_matrix()
solution_obj.print_y_matrix()
