import numpy as np  # Import packages numpy and matplotlib
import matplotlib.pyplot as plt 
from scipy.stats import norm  # Import norm to get access to the normal distribution function

T = 10 
S0 = 200
K_Max = 250 # largest K that we consider
r = 0.05
sigma = 0.5
N = np.array([2, 5, 10, 100])
delta_N = T/N    # formuals from the lecture notes
r_N = np.exp(r*delta_N)-1
u_N = np.exp(sigma*np.sqrt(delta_N))
d_N = 1/u_N



def black_scholes_price(T,S0,K,r,sigma):  # function to calculate the Black-Scholes price
    d1 = 1/(sigma*np.sqrt(T))*( np.log(S0/K)+(r+(sigma**2)/2)*T )
    d2 = d1-sigma*np.sqrt(T)
    return S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)

def binomial_model(N, S0, u, d, r, K):   # function to calculate option prices in the binomial model
    q = (1 + r - d) / (u - d)
    # make stock price tree
    stock = np.zeros([N + 1, N + 1])
    for i in range(N + 1):
        for j in range(i + 1):
            stock[j, i] = S0 * (u ** (i - j)) * (d ** j)
    # Generate option prices recursively
    option = np.zeros([N + 1, N + 1])
    option[:, N] = np.maximum(np.zeros(N + 1), (stock[:, N] - K))
    for i in range(N - 1, -1, -1):
        for j in range(0, i + 1):
            option[j, i] = (
                1 / (1 + r) * (q * option[j, i + 1] + (1-q) * option[j + 1, i + 1])
            )
    return option[0,0]  # we only need to return the initial price

# Function in terms of K
values_BS = np.zeros(50) # variables for the call values
values_N2 = np.zeros(50)
values_N5 = np.zeros(50)
values_N10 = np.zeros(50)
values_N100 = np.zeros(50)
K = np.linspace(5,K_Max,50)  # values for K
for i in range(50):
    values_BS[i] = black_scholes_price(T,S0,K[i],r,sigma)
    values_N2[i] = binomial_model(N[0], S0, u_N[0], d_N[0], r_N[0], K[i])
    values_N5[i] = binomial_model(N[1], S0, u_N[1], d_N[1], r_N[1], K[i])
    values_N10[i] = binomial_model(N[2], S0, u_N[2], d_N[2], r_N[2], K[i])
    values_N100[i] = binomial_model(N[3], S0, u_N[3], d_N[3], r_N[3], K[i])

plt.plot(K,values_BS, label="Black-Scholes-price")
plt.plot(K,values_N2, label=r'$N=2$', linewidth = 0.5)
plt.plot(K,values_N5, label=r'$N=5$', linewidth = 0.5)
plt.plot(K,values_N10, label=r'$N=10$', linewidth = 0.5)
plt.plot(K,values_N100, label=r'$N=100$', linewidth = 0.5)
plt.title("Black-Scholes-price and binomial prices of a Call")
plt.legend(loc="best")
plt.xlabel("K")
plt.show()
