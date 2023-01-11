import pandas as pd
from periodictable import *
from tabulate import tabulate
from IPython.display import HTML


class UltimateProxmate(object):
    """
    Class including methods to compute
    - the reamaining components/oxygen in percent of elementary analysis.
    -
    - heating value using the empirical Boie equation (1952)
    """

    def __init__(self, sample_name, carbon, hydrogen, nitrogen, sulfur=0, ash=0, moisture=0, volatiles=0):
        self.sample = sample_name
        self.c = carbon
        self.h = hydrogen
        self.n = nitrogen
        self.s = sulfur
        self.moist = moisture
        self.ash = ash
        self.vol = volatiles
        self.o = 100 - (self.c + self.h + self.n + self.s + self.ash + self.moist)

    def remain_content_chn(self):
        """ hello """

        remain = 100 - (self.c + self.h + self.n)
        return remain

    def fix_carbon(self):
        fix_c = 100 - (self.moist + self.vol + self.ash)
        return fix_c

    def results_wf(self):
        wf_base = (100 - self.moist) / 100
        c_wf = self.c / wf_base
        h_wf = self.h / wf_base
        o_wf = self.o / wf_base
        n_wf = self.n / wf_base
        s_wf = self.s / wf_base
        moist_wf = 0.0
        ash_wf = self.ash / wf_base
        vol_wf = self.vol / wf_base
        lhv_wf, hhv_wf = self.h_boie(c_wf, h_wf, s_wf, n_wf, o_wf, moist_wf)

        return c_wf, h_wf, o_wf, n_wf, s_wf, ash_wf, vol_wf, moist_wf, lhv_wf, hhv_wf

    def results_waf(self):
        waf_base = (100 - self.moist - self.ash) / 100
        c_waf = self.c / waf_base
        h_waf = self.h / waf_base
        o_waf = self.o / waf_base
        n_waf = self.n / waf_base
        s_waf = self.s / waf_base
        moist_waf = 0.0
        ash_waf = 0.0
        vol_waf = self.vol / waf_base
        lhv_waf, hhv_waf = self.h_boie(c_waf, h_waf, s_waf, n_waf, o_waf, moist_waf)

        return c_waf, h_waf, o_waf, n_waf, s_waf, ash_waf, vol_waf, moist_waf, lhv_waf, hhv_waf

    def h_boie(self, c_wt, h_wt, s_wt, n_wt, o_wt, moist_wt):
        """Computes the lower and upper heating value using the boie equation """
        lhv = 34800 * c_wt + 93800 * h_wt + 10460 * s_wt + 6280 * n_wt - 10800 * o_wt - 2450 * moist_wt
        hhv = 34800 * c_wt + 93800 * h_wt + 10460 * s_wt + 6280 * n_wt - 10800 * o_wt
        return lhv / 100, hhv / 100

    # def print_chnso(oxygen(1)):
    #    pd

    # def print_chn(self):
    #    return HTML(self.df.to_html(index=False))

    def print_results(self):
        name = self.sample
        lhv, hhv = self.h_boie(self.c, self.h, self.s, self.n, self.o, self.moist)

        results_wf = self.results_wf()
        results_waf = self.results_waf()
        pd.options.display.float_format = '{:.2f}'.format
        df = pd.DataFrame({
            name: ['carbon [wt%]', 'hydrogen [wt%]', 'oxygen [wt%]', 'nitrogen [wt%]', 'sulfur [wt%]', 'ash [wt%]',
                   'volatiles [wt%]', 'moisture [wt%]', 'lower heating value [kJ/kg]', 'higher heating value [kJ/kg]'],
            'row': [self.c, self.h, self.o, self.n, self.s, self.ash, self.vol, self.moist, lhv, hhv],
            'wf': results_wf,
            'waf': results_waf
        })
        return tabulate(df, headers='keys')


def mass_to_mol(element, mass):
    el = elements.symbol(element)
    atomic_w = el.mass
    n_mol = mass / atomic_w
    return n_mol


def oc_hc_ratio(wtp_c, wtp_h, wtp_o):
    c_nmol = mass_to_mol('C', wtp_c)
    print(c_nmol)
    h_nmol = mass_to_mol('H', wtp_h)
    print(h_nmol)
    o_nmol = mass_to_mol('O', wtp_o)
    oc_ratio = o_nmol / c_nmol
    hc_ratio = h_nmol / c_nmol
    return oc_ratio, hc_ratio
