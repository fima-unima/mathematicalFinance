import numpy as np  # import package numpy 
import matplotlib.pyplot as plt 
from scipy.stats import norm

rng = np.random.default_rng() # create a random generator

# parameters
mu1 = 5
mu2 = 3
sigma1 = 2
sigma2 = 1
rho = 0.2
N = 10000 # number of realizations of E[X_1+X_2|X_1]
M = 1000 # number of samples of X_2, each time given X_1 

# Realizations of X_1
x_1 = rng.normal(mu1, mu2, size = N)
est_exp = np.zeros(N)   # placeholder for our estimations

for i in range(N):
    B_2 = rng.normal(mu2, sigma2, size = M)  # simulations of B_2
    x_2 = rho*x_1[i] + (1-rho)*B_2   # use X_1 and B_2 to get simulations of X_2
    est_exp[i] = x_1[i] + np.mean(x_2)  # estimation for the conditional expectation

# Plot
plt.title('Simulation of conditional expectation')  # Title of the plot
plt.hist(est_exp, bins = int(N/10), density = True)  # Histogram with N/10 boxes, normiert für eine Dichtefunktion 
x = np.linspace(np.min(est_exp), np.max(est_exp), num = N)  # x-values for the density plot
plt.plot(x, norm.pdf(x, (1+rho)*mu1 + (1-rho)*mu2, (1+rho)*sigma1 + (1-rho)*sigma2), color="red", label="Density of " + r'$\mathcal{N}\left(\mu_\rho,\sigma_\rho \right)$')  # plot of the density function
plt.legend(loc="best")  # legend
plt.show()
