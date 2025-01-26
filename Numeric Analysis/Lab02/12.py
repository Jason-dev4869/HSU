import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2 - 2*x - 1
x = np.arange(-2, 2, 0.1)
y = f(x)
plt.title('f(x) = x^2 - 2x - 1')
plt.plot(x,y, color='b', )
x = np.arange(-2, 2, 0.5)
y = f(x)
plt.scatter(x,y, color = 'r')
plt.grid(True)
plt.legend()
plt.show()