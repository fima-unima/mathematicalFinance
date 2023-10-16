import numpy as np  # import package numpy 
import matplotlib.pyplot as plt 

# parameters
S0 = 5
u = 3/2
d = 2/3
R = 1+0.05
N = 101 

def f(x,K):  # define the payoff of a call option as a function
    return max(0,x-K)

def replicating_portfolio(S0,u,d,R,f,K):  # function that the returns the value and the numbers of sharers hold in a replicating portfolio
    a = np.array([[1, -1, -S0], [0, R, u*S0], [0, R, d*S0]])   # matrices that we nees to apply linalg.solve
    b = np.array([0, f(u*S0,K), f(d*S0,K)])
    return np.linalg.solve(a,b)[0]  # apply linalg.solve to solve the system of linear equations

K = np.linspace(0, 10, 101) # strike values
values = np.zeros(N) # variable for the portfolio values

for i in range(N):
    values[i] = replicating_portfolio(S0,u,d,R,f,i/10)  # applying the function for different strikes, saving the portfolio value

# Plot
plt.title('Call option values in the 1-step binomial model')  # Title of the plot
plt.plot(np.linspace(0,10,N), values,)  # plot the option values
plt.xlabel('Strike K')
plt.ylabel('Value')
plt.show()

# Interpretation of the two edges in the graph: 
# - above the upper one (at S0*u) we are never "in the money" -> option value constantly 0
# - below the lower one (at S0*d) we are never "out of the money" -> slope of -1/R since every chang in K translates 1-to-1 into a change of the payoff (and hence 1-to-1 but discounted into a change of the option value at t=0)