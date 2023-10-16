import numpy as np  # import package numpy 

rng = np.random.default_rng() # create a random generator

# (ii)
N = 100 # number of realizations
rng.integers(1, 11, size = N)  # N discrete realizations; note that the right interval bound is excluded
rng.normal(0, 1, size = N) # standard normally distributed (mean=0, stddeviation=1)
rng.exponential(3, size = N) # exponetially distributed

# (iii) Online shop
def shop_simulator(N):   # create a function
    anz_tests = N  # variable for the current number of available tests
    count_consumers = 0  # count the number of consumers
    while anz_tests>0:   # while loop to test if there are tests left
        anz_tests -= rng.integers(1, 11, size = 1) # Note: a-=1 is the short version for a=a-1. We subtract the demand of the current consumer from our available test number
        count_consumers += 1 # count the consumer 
    return print("The " + str(N) + " tests were sold out after " + str(count_consumers) + " consumers.")  # print the result

shop_simulator(50)
shop_simulator(500)
shop_simulator(1000)

