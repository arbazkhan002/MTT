from scipy import stats # Import the scipy.stats module
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
# Definitions of different parameters. (float() used to avoid problems with Python integer division)
M = float(2.7) # Geometric mean == median
s = float(0.5) # Geometric standard deviation
mu = np.log(M) # Mean of log(X)
sigma = np.log(s) # Standard deviation of log(X)
shape = sigma # Scipy's shape parameter
scale = np.exp(mu) # Scipy's scale parameter
median = np.exp(mu)
mode = np.exp(mu - sigma**2) # Note that mode depends on both M and s
mean = np.exp(mu + (sigma**2/2)) # Note that mean depends on both M and s
x = np.linspace(0, 10, num=400) # values for x-axis
#~ pdf = stats.lognorm.pdf(x, s, loc=M, scale=M) # probability distribution
dist=stats.lognorm([s],loc=M)
#~ print pdf
#~ plt.figure()
# Figure on linear scale
#~ plt.subplot(121)
pl.plot(x, dist.pdf(x))
#~ plt.fill_between(x, pdf, where=(x < M/s), alpha=0.15)
#~ plt.fill_between(x, pdf, where=(x > M*s), alpha=0.15)
#~ plt.fill_between(x, pdf, where=(x < M/s**2), alpha=0.15)
#~ plt.fill_between(x, pdf, where=(x > M*s**2), alpha=0.15)
#~ plt.vlines(mode, 0, pdf.max(), linestyle=':', label='Mode')
#~ plt.vlines(mean, 0, stats.lognorm.pdf(mean, shape, loc=0, scale=scale), linestyle='--', color='green', label='Mean')
#~ plt.vlines(median, 0, stats.lognorm.pdf(median, shape, loc=0, scale=scale), color='blue', label='Median')
#~ plt.ylim(ymin=0)
#~ plt.xlabel('Radius (microns)')
#~ plt.title('Linear scale')
#~ leg=plt.legend()
pl.savefig("graphtex", format="ps")
plt.show()
