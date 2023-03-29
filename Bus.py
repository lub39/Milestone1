
class Bus:

    counter = 0

    def __init__(self, name):
        self.name = name
        self.index = Bus.counter

        self.v = None

        Bus.counter = Bus.counter + 1

    def set_bus_v(self, bus_v):
        self.v = bus_v

        # Power Flow Setting Bus Data
    def setBusdata(self, bus_type: str, real_P: float, Q_or_V: float):

        if bus_type == "Swing Bus":
            self.bus_type = "Swing Bus"
            self.V = 1.0
            self.delta = 0.0
            self.P = 0.0
            self.Q = 0.0

        elif bus_type == "Load Bus":
            self.bus_type = "Load Bus"
            self.V = 0.0
            self.delta = 0.0
            self.P = real_P
            self.Q = Q_or_V

        elif bus_type == "Voltage Controlled Bus":
            self.bus_type = "Voltage Controlled Bus"
            self.V = Q_or_V
            self.delta = 0.0
            self.P = real_P
            self.Q = 0.0

        else:
            print("Type not accepted. Enter Swing Bus, Load Bus, or Voltage Controlled Bus.")
