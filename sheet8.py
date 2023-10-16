import numpy as np  # import package numpy 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# parameters
R = 1.05
S0 = 5
u = 3/2
m = 1.1
d = 2/3

# matrix and vector of the system of equations
A = np.array([[u*S0,m*S0,d*S0], [1,1,1]])
b1 = np.array([S0*R, 1])

def solve_underdetermined_system(A, b):  # function to find a solution to the underdetermined system of equations (the one with the smallest norm)
    m, n = A.shape  # dimensions of A
    Q, R1 = np.linalg.qr(np.transpose(A), mode='complete')  # QR-decomposition of the transposed of A
    R2 = np.array(R1[0:m,0:m])  # select the quadratic non-zero part of A
    z = np.matmul(np.linalg.inv(np.transpose(R2)), b)  # formula, see exercise sheet
    q = np.matmul(Q, np.append(z,0))  # solution
    return q

q = solve_underdetermined_system(A, b1)  # solution with smallest norm

# derive a non-zero solution x to Ax=0 (might and will have negative entries)
fix_q1 = 0.1 
x1 = np.linalg.solve(A[0:2,1:3], [-fix_q1*u*S0, -fix_q1]) # solve the system of 2 equations and 2 unknowns without q1
x = np.append(fix_q1, x1)  # x is a non-zero solution to Ax=0. Now: every linear combination q+lambda*x for real lambda, that does not have negative entries, is an EMM

# We build the set of all EMMs now, pretty technical, maybe you find a nicer solution :)
check = 1  # help variable for the while loop
l = 0  # for the linear combination
q_set = q # for the set of all EMMs 
while check==1:
    l = l + 0.001
    z = q + l*x  # candidate for the next EMM -> must check non-negativity
    if (z[0]>0)*(z[1]>0)*(z[2]>0):
        q_set = np.column_stack((q_set,z)) # add the candidate to our set
    else:
        check = 0

check = 1 # doing the same for the other direction now
l = 0
while check==1:
    l = l + 0.001
    z = q - l*x
    if (z[0]>0)*(z[1]>0)*(z[2]>0):
        q_set = np.column_stack((z,q_set))
    else:
        check = 0

#3d Plot of the set of EMMs
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(q_set[0,:], q_set[1,:], q_set[2,:], 'blue')
plt.title("Set of EMMs in the trinomial model")
ax.set_xlabel(r'$q_1$')
ax.set_ylabel(r'$q_2$')
ax.set_zlabel(r'$q_3$')
plt.show()