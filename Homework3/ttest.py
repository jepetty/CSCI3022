# Jessica Petty
# CSCI 3022
# Homework 3
# October 13, 2016

from math import sqrt

from scipy.stats import t
from numpy import mean

def degrees_of_freedom(s1, s2, n1, n2):
    """
    Compute the number of degrees of freedom using the Satterhwaite Formula
    
    @param s1 The unbiased sample variance of the first sample
    @param s2 The unbiased sample variance of the second sample
    @param n1 Thu number of observations in the first sample
    @param n2 The number of observations in the second sample
    """

    return (s1/n1 + s2/n2)**2/((s1/n1)**2/(n1-1) + (s2/n2)**2/(n2-1))

def unbiased_sample_variance(observations, mean):
    """
    Compute the unbiased sample variance

    @param observations Iterable set of observations
    @param mean The estimated mean
    """
    
    return sum((y-mean)**2 for y in observations)/(len(observations) - 1)

def t_statistic(mean1, mean2, n1, n2, svar1, svar2):
    """
    Compute the t-statistic for the given estimates
    """

    return (mean1 - mean2)/sqrt((svar1/n1 + svar2/n2))

def t_test(sample1, sample2):
    """
    Return the two-tailed p-value of a t test with unequal variance for two samples.

    @param sample1 An iterable of the first sample
    @param sample2 An iterable of the second sample
    """

    mean1 = mean(sample1)
    mean2 = mean(sample2)
    var1 = unbiased_sample_variance(sample1, mean1)
    var2 = unbiased_sample_variance(sample2, mean2)
    tstat = t_statistic(mean1, mean2, len(sample1), len(sample2), var1, var2)
    dof = degrees_of_freedom(var1, var2, len(sample1), len(sample2))
    
    return 2*(1-t.cdf(abs(tstat), dof+1))

if __name__ == "__main__":
    v1 = [5, 7, 5, 3, 5, 3, 3, 9]
    v2 = [8, 1, 4, 6, 6, 4, 1, 2]

    print("p-value is %f" % t_test(v1, v2))
    
