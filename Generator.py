class Generator:

    def __init__(self, name, bus1, p_rate):
        self.name = name
        self.bus1 = bus1
        self.p_rate = p_rate
        self.buses = [self.bus1]
