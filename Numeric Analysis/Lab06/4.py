import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.cos(x)

def df_exact(x):
    return -np.sin(x)

def finite_difference(f, x, h):
    return (f(x + h) - f(x)) / h

x_values = np.arange(0, 2*np.pi, 0.1)

fd_values = finite_difference(f, x_values, 0.1)

exact_values = df_exact(x_values)

plt.figure(figsize=(8, 6))
plt.plot(x_values, fd_values, 'b--', label='Finite difference approximation')
plt.plot(x_values, exact_values, 'orange', label='Exact solution df(x) = -sin(x)')
plt.xlabel('x')
plt.ylabel('Derivative of cos(x)')
plt.title('Difference of f(x) = cos(x)')
plt.legend()
plt.grid(True)
plt.show()