import numpy as np

A = np.array([[8, -6, 2],[-4, 11, -7],[4, -7, 6]])
b = np.array([[28],[-40],[33]])
L = np.array([[2, 0 ,0],[-1, 2, 0],[1, -1, 1]])
U = np.array([[4, -3, 1], [0, 4, -3], [0, 0, 2]])

y = np.linalg.solve(L, b)
x = np.linalg.solve(U, y)

print("A = \n", A)
print("b = \n", b)
print("A = LU = \n", L, "\n * \n",U)
print("Ax = b, Found x: \n", x)