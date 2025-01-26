import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

x = [0, 1, 2]
y = [0, 2, 1]

f  = CubicSpline(x, y , bc_type='natural')

print("y = ", f(1.5))
x_new = np.linspace(0,2,100)
y_new = f(x_new)

plt.figure(figsize = (10,8))
plt.plot(x_new, y_new, 'b')
plt.plot(x, y, 'ro')
plt.title('Cubic Spline Interpolation')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()