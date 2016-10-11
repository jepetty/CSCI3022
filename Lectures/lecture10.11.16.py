# calculating the p-value for problem 1:
from scipy.stats.distributions import chi2

print("example 1: ", 1 - chi2.cdf(22.15, 2))

from scipy.stats import chisquare
print("example 1: ", chisquare([138, 83, 64, 64, 67, 84], [115.14, 85.5, 84.36, 86.86, 64.5, 63.64], 3))

# calculating the p-value for problem 2:
from scipy.stats import norm
print("example2: ", 1.0 - norm.cdf(1.28))

# example 3:
import pandas as pd
mpg = pd.read_csv("../data/jp-us-mpg.dat", delim_whitespace=True)
print("example 3: ", mpg.head())
from numpy import mean
print("Japan: ", mean(mpg["Japan"].dropna()))
print("USA: ", mean(mpg["US"].dropna()))
from numpy import var
japan = mpg["Japan"].dropna()
us = mpg["US"].dropna()
jp_var = (var(japan) * len(japan))/(float(len(japan) - 1))
us_var = (var(us) * len(us))/(float(len(us) - 1))