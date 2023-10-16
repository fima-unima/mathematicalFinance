# Parameters
S=5; K=5; R=1.02; u=1.2; N=10  # Take care: recursive function option_value -> do not choose N too large
q = (R-1/u)/(u-1/u)

def price(k, ups):  # Compute the stock price after 'ups'-times going up and 'k-ups'-times down
    return S * (u ** (2 * ups - k))

def am_option_value(k, ups, call):  # Attention: recursive function: gets very slow for large N. call=1 denotes a call option
    """
    Compute the option price for a node 'k' timesteps in the future
    and 'ups' growth events. Note that thus there are 'k - ups' decay events.
    """
    # Compute the exercise profit
    stockPrice = price(k, ups)
    if call: 
        exerciseProfit = max(0, stockPrice-K)
    else: 
        exerciseProfit = max(0, K - stockPrice)
    # Base case (this is a leaf (end node) of the tree)
    if k == N: return exerciseProfit
    # Recursive case: compute the expected value in the next step 
    expected = (q * am_option_value(k + 1, ups + 1, call) + (1 - q) * am_option_value(k + 1, ups, call))/R
    # Value of an American option
    return max(expected, exerciseProfit)

print('Computed American Call option price: ' + str(am_option_value(0,0,1)))  # option_value(0,0,1) computes the price in t=0 of an American call option
print('Computed American Put option price: ' + str(am_option_value(0,0,0)))
