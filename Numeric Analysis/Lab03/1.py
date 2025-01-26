import numpy as np

a = np.array([[2.1, -0.6, 1.1],[3.2, 4.7, -0.8],[3.1, -6.5, 4.1]])
print("Origin Array: \n", a)
b = np.linalg.det(a)
print("Determinat of Array: \n", b)