import numpy as np  # import package numpy 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# parameters
R = 1.05
S1 = np.array([[5,0,0,0],[6,4,0,0],[7,5,5,4]])  # 2-step binomial model
S2 = np.array([[1,0,0,0,0,0,0,0], [1.5,2/3,0,0,0,0,0,0], [1.7,1.3,3/4,0.6,0,0,0,0], [2,1.6,1.45,1.2,1,0.7,0.65,0.5]]) # 3-step binomial model
n = 10
S3 = np.zeros((n,2**(n-1))) # create a (n-1)-step binomial model where "up" means multilpication with u and "down" means multilpication with d
u = 3/2
d = 2/3
S3[0,0] = 5 # initial value
for i in range(n-1):
    for j in range(i+1):
        S3[i+1,2*j] = S3[i,j]*u   # fill the price matrix with values
        S3[i+1,2*j+1] = S3[i,j]*d


# function to check no-arbitrage
def no_arbitrage_check(R, S):
    check = 1
    for i in range(np.shape(S)[0]-1):  # (number rows of S)-1
        for j in range(i+1):  # number of columns with entries not zero in row i
            check = check * (S[i,j]*R < S[i+1,2*j]) * (S[i,j]*R > S[i+1,2*j+1])  # check arbitrage conditions
    return check # 1 if arbitrage-free, 0 if arbitrage

# function to calculate the EMM
def emm_binomial(R, S):
    if no_arbitrage_check(R, S):  # calculate q only if the market is arbitrage free
        q = np.zeros((np.shape(S)[0]-1, np.shape(S)[0]-1))   # right dimension for q, initialized with zeros
        for i in range(np.shape(S)[0]-1):  # (number rows of S)-1
            for j in range(i+1):  # number of columns with entries not zero in row i
                q[i,j] = (S[i,j]*R-S[i+1,2*j+1])/(S[i+1,2*j]-S[i+1,2*j+1])              
        print("The unique EMM is given by q = " +str(np.round(q, 4)))  # round q to 4 decimal digits to avoid numerical inaccuracy
    else:
        print("There is arbitrage in the market")

emm_binomial(R, S3) # apply it to our data
#emm_binomial(R, S2)
#emm_binomial(R, S1)