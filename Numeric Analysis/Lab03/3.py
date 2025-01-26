import numpy as np

A = np.array([[6, -4, 1], [-4, 6, -4], [1, -4, 6]])
B = np.array([[-14, 22], [36, -18], [6, 7]])

x = np.linalg.solve(A, B)
print("Result: \n", x)