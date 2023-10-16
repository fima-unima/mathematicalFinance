import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# parameters
p = 1/2
u = 1.5
d = 0.8
r = 0.02
q = (1+r-d)/(u-d)
x0 = 100
S0 = 10
gamma = 1/2
theta = 1/(1-gamma)
N = 10**4

# optimal portfolio
a_star = ((1+r)*x0)/((u-d)*q*(1-q)) * ((p**theta)*((1-q)**theta) - (q**theta)*((1-p)**theta))/((p**theta)*((1-q)**(theta*gamma))+((1-p)**theta)*(q**(theta*gamma)))   # formula from exercise 12.1

# set of a's that we test
upper = (x0*(1+r))/(1+r-d) # upper bound for a: otherwise, negative realizations of V_1 would be possible -> not allowed for power utilities
a_set = np.concatenate((np.arange(a_star/4, a_star, 1), np.arange(a_star, upper, 1)))  
a_set_values = np.zeros(a_set.size)  # variable for the Monte Carlo realizations

rng = np.random.default_rng() # create a random generator
j = -1 # counter
for a in a_set:
    j += 1
    b = x0-a
    for i in range(N):  # monte carlo simulation
        if rng.uniform(0,1)>p:
             a_set_values[j] += ((b*(1+r)+a*u)**gamma)/gamma  # utility of V_1 if stock goes up
        else:
             a_set_values[j] += ((b*(1+r)+a*d)**gamma)/gamma  # utility if stock goes down
    a_set_values[j] = a_set_values[j]/N


a_set_smoothed = savgol_filter(a_set_values, 151, 4)  # we smooth the curve by a polynomial of order 4, to better see the result
plt.plot(a_set, a_set_values)
plt.plot(a_set, a_set_smoothed, color='red')
plt.title('Expected utility of investment in a stock with '+r'$S_0=$'+str(S0)+r'$, u=$'+str(u)+r'$, d=$'+str(d)+r'$, p=$'+str(p)+r'$, r=$'+str(r))
plt.xlabel(r'$a$')
plt.ylabel(r'$\mathbb{E}[U(V_1)]$')
plt.xticks([a_star/4, a_star], [r'$\frac{a^*}{4}$',r'$a^*=$'+str(round(a_star,2))])
plt.show()
