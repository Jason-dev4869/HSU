import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

x = [0,2,3]
y = [7,11,28]

L0_coeff = [1, -5/6, 1/6]
L1_coeff = [0, 3/2, -1/2]
L2_coeff = [0, -2/3, 1/3]

L0 = poly.Polynomial(L0_coeff)
L1 = poly.Polynomial(L1_coeff)
L2 = poly.Polynomial(L2_coeff)

P = 7*L0 + 11*L1 + 28*L2

x_new = np.arange(-1.0, 4.1, 0.1)
fig = plt.figure(figsize = (10,8))
plt.plot(x_new, P(x_new), 'b', x,y, 'ro')
title = f"Langrange Polynormal P(x) = {P}"
plt.title(title)
plt.grid()
plt.xlabel('x')
plt.ylabel('y')
plt.show()