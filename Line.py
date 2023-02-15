import numpy as np
import math
import pandas as pd


class Line:

    ep = 8.854e-12 * 1609

    def __init__(self, name, bus1, bus2, length, f, rad, gmr, d, resistance, num_cond, d_ab, d_bc, d_ca):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.length = length
        self.f = f
        self.rad = rad
        self.gmr = gmr
        self.d = d
        self.resistance = resistance
        self.num_cond = num_cond
        self.d_ab = d_ab
        self.d_bc = d_bc
        self.d_ca = d_ca

        self.buses = [self.bus1, self.bus2]

    def calc_y(self):
        if self.num_cond == 1:
            d_sl = self.gmr
            d_sc = self.rad
            r = self.resistance*self.length
        elif self.num_cond == 2:
            d_sl = math.sqrt(self.gmr*self.d)
            d_sc = math.sqrt(self.rad*self.d)
            r = (self.resistance*self.length)/2
        elif self.num_cond == 3:
            d_sl = np.cbrt(self.gmr*self.d**2)
            d_sc = np.cbrt(self.rad*self.d**2)
            r = (self.resistance*self.length)/3
        else:
            d_sl = 1.0941*np.power(4, 1/(self.gmr*self.d**3))
            d_sc = 1.0941*np.power(4, 1/(self.rad*self.d**3))
            r = (self.resistance*self.length)/4

        d_eq = np.cbrt(self.d_ab*self.d_bc*self.d_ca)

        l = 2e-7*math.log(d_eq/d_sl)*1609*self.length
        x = 2*math.pi*self.f*l
        z = r + 1j*x
        y_se = 1/z

        c = (2*math.pi*Line.ep*self.length)/math.log(d_eq/d_sc)
        b = 2*math.pi*self.f*c
        y_sh = 1j*b

        y_df = pd.DataFrame()

        y_df.loc[self.bus1, self.bus1] = (1/2)*y_sh + y_se
        y_df.loc[self.bus2, self.bus2] = (1/2)*y_sh + y_se
        y_df.loc[self.bus1, self.bus2] = -((1/2)*y_sh + y_se + (1/2)*y_sh)
        y_df.loc[self.bus2, self.bus1] = -((1/2)*y_sh + y_se + (1/2)*y_sh)

        self.y = y_df

