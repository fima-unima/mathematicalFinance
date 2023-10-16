import numpy as np  # import package numpy 
from scipy.optimize import minimize 

# parameters 
S0 = 5
u = 3/2
m = 7/6
d = 2/3
R = 1.05
K = 3

def f(x,K):  # define the payoff of a call option as a function
    return max(0,x-K)

def superhedging_price(S0,u,m,d,R,f,K): 
    targetfunction = lambda phi: phi[0] + phi[1]*S0  # targetfunction that we want to minimize over the trading strategy phi. Defined as a LAMBDA function
    cons = ({'type': 'ineq', 'fun': lambda phi: phi[0]*R + phi[1]*u*S0 - f(u*S0,K)}, # 3 constraints
            {'type': 'ineq', 'fun': lambda phi: phi[0]*R + phi[1]*m*S0 - f(m*S0,K)},
            {'type': 'ineq', 'fun': lambda phi: phi[0]*R + phi[1]*d*S0 - f(d*S0,K)})
    return minimize(targetfunction, x0 = (max(f(u*S0,K),f(m*S0,K),f(d*S0,K)),0), constraints=cons) # minimization. Choosing an initial value x0 that always fulfills the constraints (just the maximal possible payoff in the bankaccount)

# Apply it to the above parameters
superhedging_price(S0,u,m,d,R,f,K)   