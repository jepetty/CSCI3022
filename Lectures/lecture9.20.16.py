# lecture 9.20.16
from numpy.random import binomial 
from numpy.random import normal
from numpy.random import poisson
from collections import Counter
from scipy.stats import norm
from scipy.stats import expon
import matplotlib.pyplot as plt

def main():
	jessBinomial()
	print("standard deviation: ", jessNormal())
	jessExponential()
	Jordan()

def jessBinomial():
	trials = binomial(10, 0.5, 340)
	count = Counter(trials)

def jessNormal():
	mean, sd = 1, 0.002
	res = norm.cdf(1.003, mean, sd) - norm.cdf(0.997, mean, sd)
	print("probability of rejection: ", 1-res)
	for x in range(100):
		sd = 0.002 - x/100000
		res = 1 - (norm.cdf(1.003, mean, sd) - norm.cdf(0.997, mean, sd))
		if res < 0.01:
			return sd

def jessExponential():
	lmbd = 1/2
	val = expon.cdf(4, 1/lmbd)
	print("more than 4 hours: ", 1-val)
	print("more than 8 hours given more than 4 hours: ", 1-val)


def Jordan():
	res = binomial(10, 0.5, 340)
	Counter(res)

	a = 1 - expon.cdf(8, 2)
	print(a / (1 - expon.cdf(4,2)))

def manyExperiments():
	res = binomial(10, 0.5, (1000, 340))
	two_or_less = sum(1 for experiment in res if any(y <= 2 for y in experiment))
	print(two_or_less)
	zeros = sum(1 for experiment in res if any(y == 0 for y in experiment))
	print(zeros)
	plt.hist(res[0])
	plt.show()

if __name__ == "__main__":
	main()


# important probability libraries: 
	# all the numpy.random -> basically use numpy to look up every library
	# scipy.stats has normal distribution cdf -> very useful
	# matplotlib.pyplot for plotting!