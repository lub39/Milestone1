import numpy as np
import math
import pandas as pd


class Line:

    ep = 8.854e-12
    f = 60  # Hz

    def __init__(self, name: str, codeword: str, bus1, bus2, length, d, num_cond,
                 axaxis, ayaxis, bxaxis, byaxis, cxaxis, cyaxis, vbase):

        self.name = name
        self.codeword = codeword
        self.bus1 = bus1
        self.bus2 = bus2
        self.length = length
        self.d = d
        self.num_cond = num_cond
        self.axaxis = axaxis
        self.ayaxis = ayaxis
        self.bxaxis = bxaxis
        self.byaxis = byaxis
        self.cxaxis = cxaxis
        self.cyaxis = cyaxis
        self.vbase = vbase
        self.buses = [self.bus1, self.bus2]

    def calc_y(self):

        s_base = 100    # MVA
        z_base = self.vbase**2/s_base

        d_ab = ((self.axaxis - self.bxaxis) ** 2 - (self.ayaxis - self.byaxis) ** 2) ** (1 / 2)
        d_bc = ((self.bxaxis - self.cxaxis) ** 2 - (self.byaxis - self.cyaxis) ** 2) ** (1 / 2)
        d_ca = ((self.cxaxis - self.axaxis) ** 2 - (self.cyaxis - self.ayaxis) ** 2) ** (1 / 2)
        d_eq = np.cbrt(d_ab*d_bc*d_ca)

        if self.codeword == "Partridge":
            self.gmr = 0.0217    # ft
            self.rad = 0.02675  # ft
            self.resistance = 0.385   # Ohm/mi

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

        ind = 2e-7*math.log(d_eq/d_sl)*1609.344*self.length
        x = 2*math.pi*Line.f*ind
        z = (r + 1j*x)/z_base
        y_se = 1/z

        c = (2*math.pi*Line.ep*self.length*1609.344)/math.log(d_eq/d_sc)
        b = 2*math.pi*Line.f*c*z_base
        y_sh = 1j*b

        y_df = pd.DataFrame()

        y_df.loc[self.bus1, self.bus1] = (1/2)*y_sh + y_se
        y_df.loc[self.bus2, self.bus2] = (1/2)*y_sh + y_se
        y_df.loc[self.bus1, self.bus2] = -y_se
        y_df.loc[self.bus2, self.bus1] = -y_se

        self.y = y_df

