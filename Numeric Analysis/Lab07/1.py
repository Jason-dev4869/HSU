import numpy as np
from scipy.integrate import trapezoid
from scipy.integrate import simpson
from scipy.integrate import romb

def f(x):
    return np.sqrt(x) * np.cos(x)

a, b = 0, 6
n = 100

#Riemann
def riemann_sum_integration(f, a, b, n):
    x = np.linspace(a, b, n+1)
    dx = (b - a) / n
    areas = f(x[:-1]) + f(x[1:])
    return dx * np.sum(areas) / 2

riemann_integral = riemann_sum_integration(f, a, b, n)
print(f"Riemann: {riemann_integral:.4f}")

# Quy tắc hình thang
x = np.linspace(a,b,n+1)
trapezoidal_integral = trapezoid(f(x),x)
print(f"Quy tac hinh thang: {trapezoidal_integral:.4f}")

# Quy tắc hình thang đệ quy
def recursive_trapezoidal(f, a, b, tol=1e-6):
    n = 1
    old_integral = 0
    new_integral = f(a) + f(b)
    while abs(new_integral - old_integral) >= tol:
        n *= 2
        old_integral = new_integral
        x = np.linspace(a, b, n+1)
        new_integral = sum(f(x[:-1]) + f(x[1:])) * (b-a) / n
    return new_integral / 2

recursive_integral = recursive_trapezoidal(f, a, b, 1e-6)
print(f"Quy tac hinh thang de quy: {recursive_integral:.4f}")

#Simpson
simpson_integral = simpson(f(np.linspace(a, b, 101)), dx=(b-a)/100)
print(f"Simpson: {simpson_integral:.4f}")

#Romberg
romberg_integral = romb(f(np.linspace(a, b, 2**8+1)), dx=(b-a)/(2**8), show=False)
print(f"Romberg: {romberg_integral:.4f}")