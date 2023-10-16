import networkx as nx 
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt 

# parameters
N=8
S0=7
K=9
u = 1.1
d = 0.9
R = 1.01
p = (R-d)/(u-d)
q = 1-p

X = np.empty(N+1, dtype=int)
for i in range(0,N+1):  # global variable for the plots, counts from 0 to N
    X[i]=i

def plot_tree(g,pl_title):  # function to plot a tree given the data in g 
    Z = np.empty(3)
    global N
    for k in reversed(range(0,N)):
        for l in range(-k+1,k+3,2):
            Z[0]=g.nodes[(k,l)]['value']
            Z[1]=g.nodes[(k+1,l+1)]['value']
            Z[2]=3
            plt.plot(X[k:k+2],Z[0:2],color='blue',marker='.',markersize = 10)
            Z[0]=g.nodes[(k,l)]['value']
            Z[1]=g.nodes[(k+1,l-1)]['value']
            Z[2]=3
            plt.plot(X[k:k+2],Z[0:2],color='blue',marker='.',markersize = 10)
    plt.grid(linestyle='--', linewidth=0.5, color='gray')   
    plt.title(pl_title)
    plt.show()

def graph_stock(): # function to calculate the possible stock price movements
    S=nx.Graph()
    for k in range(0,N):
        for l in range(-k+1,k+3,2):  # build the edge structure. Note that both nodes on the ede are automatically added, if not already in the graph
            S.add_edge((k,l),(k+1,l+1))
            S.add_edge((k,l),(k+1,l-1))            
    for n in S.nodes():  # give the nodes the correct values
        k=n[0]
        l=n[1]-1
        S.nodes[n]['value']=S0*((d)**((k+l)/2))*((u)**((k-l)/2))
    return S

def European_call_price(K):  # function to calculate the possible call price movements
    price = nx.Graph()    
    hedge = nx.Graph()
    S = graph_stock()
    for k in range(0,N):
            for l in range(-k+1,k+3,2):
                price.add_edge((k,l),(k+1,l+1))
                price.add_edge((k,l),(k+1,l-1))
                hedge.add_edge((k,l),(k+1,l+1))
                hedge.add_edge((k,l),(k+1,l-1))    
    for l in range(-N+1,N+3,2):
        price.nodes[(N,l)]['value'] = np.maximum(S.nodes[(N,l)]['value']-K,0)     
    for k in reversed(range(0,N)):
        for l in range(-k+1,k+3,2):
            price.nodes[(k,l)]['value'] = (price.nodes[(k+1,l+1)]['value']*p+price.nodes[(k+1,l-1)]['value']*q)/R        
    return price


def European_call_hedge(K):  # function to calculate the hedging strategy
    price = European_call_price(K)
    hedge = nx.Graph()
    S = graph_stock()
    for k in range(0,N):
            for l in range(-k+1,k+3,2):
                hedge.add_edge((k,l),(k+1,l+1))
                hedge.add_edge((k,l),(k+1,l-1))   
    for l in range(-N+1,N+3,2):
        hedge.nodes[(N,l)]['value'] = 1
    for k in reversed(range(0,N)):
        for l in range(-k+1,k+3,2):
            hedge.nodes[(k,l)]['value'] = (price.nodes[(k+1,l+1)]['value']-price.nodes[(k+1,l-1)]['value'])/(d-u)/(S.nodes[(k,l)]['value'])
    for l in range(-N+1,N+1,2):
        hedge.nodes[(N,l)]['value'] = hedge.nodes[(N-1,l+1)]['value'] 
        hedge.nodes[(N,l+2)]['value'] = hedge.nodes[(N-1,l+1)]['value'] 
    return hedge


# apply our functions
plot_tree(graph_stock(),'Possible stock prices')
plot_tree(European_call_price(float(K)), 'Possible call prices') 
plot_tree(European_call_hedge(float(K)), 'Hedging strategy: possible investments in the risky asset')
