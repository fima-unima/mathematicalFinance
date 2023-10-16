import networkx as nx 
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt 

# parameters
N = 8
S0 = 7
K = 9

d = -0.1  # we denote here d=-0.1 instead of 0.9, as it would be in the notation of the lecture. u and r analogue
u = 0.1  
r = 0.1

p = (r-d)/(u-d)
q = (u-r)/(u-d)

# function to plot a tree using networkx
def plot_tree(g, pl_title):
    plt.figure(figsize=(20,10))
    pos={}
    lab={}    
    for n in g.nodes():
        pos[n]=(n[0],n[1])
        if g.nodes[n]['value'] is not None: lab[n]=float("{0:.2f}".format(g.nodes[n]['value']))
    elarge=g.edges(data=True)
    nx.draw_networkx_labels(g,pos,lab,font_size=15,font_family='sans-serif')
    nx.draw_networkx_nodes(g,pos,node_color='red',alpha=0.4,node_size=1000)
    nx.draw_networkx_edges(g,pos,edge_color='blue',alpha=0.9,width=3,edgelist=elarge)
    plt.ylim(-N+0.5,N+1.5) 
    plt.xlim(-0.5,N+0.5)
    plt.title(pl_title)
    plt.show()
    
# build the stock price process
def graph_stock():
    S=nx.Graph()
    for k in range(0,N):
        for l in range(-k+1,k+3,2):
            S.add_edge((k,l),(k+1,l+1))
            S.add_edge((k,l),(k+1,l-1))          
    for n in S.nodes():
        k=n[0]
        l=n[1]-1
        S.nodes[n]['value']=S0*((1.0+u)**((k+l)/2))*((1.0+d)**((k-l)/2))
    return S

# build the call price process
def European_call_price(K):
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
            price.nodes[(k,l)]['value'] = (price.nodes[(k+1,l+1)]['value']*p+price.nodes[(k+1,l-1)]['value']*q)/(1+r)        
    return price


call_price = European_call_price(K)

print('Underlying asset prices:')
plot_tree(graph_stock(), 'Stock price process')
print('European call prices:')
plot_tree(call_price, 'Call price process')
print('Price at time 0 of the European call option:',float("{0:.4f}".format(call_price.nodes[(0,1)]['value'])))


