import numpy as np
from scipy import interpolate as inter
from matplotlib import pyplot as plt

x = np.array([1.5, 1.9, 2.1, 2.4, 2.6, 3.1])
f = np.array([1.0628, 1.3961, 1.5432, 1.7349, 1.8423, 2.0397])
s = inter.CubicSpline(x,f, bc_type="natural")

print("s.x = ", s.x)
print("Cubic Spline - Column: ")
print("Coefficients = \n", s.c)

m = x.shape[0] - 1
for i in range(m):
    print(f"Coef of S{i} = ", s.c[:,i])

print("Cubic Spline - Colunm: ")
print("Dao ham bac 0 =\n", s.derivative(0).c)
print("Dao ham bac 1 =\n", s.derivative().c)
print("Dao ham bac 2 =\n", s.derivative(2).c)
print("Dao ham bac 3 =\n", s.derivative(3).c)

S_d1 = s.derivative()
S_d2 = s.derivative(2)
print("f'(2) = ", S_d1(2.5))
print("f''(2) = ", S_d2(2.5))

plt.scatter(x,f)
h = 0.02
for i in range(m):
    segment_x = np.linspace(x[i], x[i+1], 50)
    plt.plot(segment_x, s(segment_x), '--')
    plt.plot(segment_x, S_d1(segment_x), label=f"S'_{i}")
    plt.plot(segment_x, S_d2(segment_x), label=f"S''_{i}")
plt.legend()
plt.show()