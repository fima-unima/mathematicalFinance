import numpy as np  # import package numpy 
import matplotlib.pyplot as plt 
from scipy.stats import norm

rng = np.random.default_rng() # create a random generator

# parameters
N = 1000 # number of steps
M = 10000 # number of realizations 

Z = np.zeros(M) # vector for the endpoints
for i in range(M):
    X = rng.integers(1,3,N)*2-3  # rng.integers(1,3,N) gives N-times 1 or 2, then scaling and shifting to get -1 or 1 
    Z[i] = np.sum(X)  # end points of the random walk


# Plot
plt.title('M=' + str(M) + ' random walks of N=' + str(N) + ' steps')  # Title of the plot
plt.hist(Z, bins = int(M/500), density = True)  # Histogram 
x = np.linspace(np.min(Z), np.max(Z), num = M)  # x-values for the density plot
plt.plot(x, norm.pdf(x, 0, np.sqrt(N)), color="red", label="Density of " + r'$\mathcal{N}\left(0,\sqrt{N} \right)$')  # plot of the density function
plt.legend(loc="best")  # legend
plt.show()
