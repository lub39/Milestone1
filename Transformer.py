import math
import pandas as pd


class Transformer:

    def __init__(self, name, bus1, bus2, p_rate, v1_rate, v2_rate, z_pct, xr_ratio):

        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.p_rate = p_rate
        self.v1_rate = v1_rate
        self.v2_rate = v2_rate
        self.z_pct = z_pct
        self.xr_ratio = xr_ratio

        self.buses = [self.bus1, self.bus2]

    def calc_y(self):
        s_base = 100    # MVA
        v_base = self.v2_rate

        z_b = self.z_pct*((self.v2_rate**2/self.p_rate)/(v_base * v_base/s_base))
        r = z_b*math.cos(math.atan(self.xr_ratio))
        x = z_b*math.sin(math.atan(self.xr_ratio))

        z = r+1j*x
        y = 1/z
        y_df = pd.DataFrame()

        y_df.loc[self.bus1, self.bus1] = y
        y_df.loc[self.bus2, self.bus2] = y
        y_df.loc[self.bus1, self.bus2] = -y
        y_df.loc[self.bus2, self.bus1] = -y

        self.y = y_df
