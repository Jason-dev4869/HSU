import numpy as np

def f(x):
    return x**3 + 10*x**2 + 5

tol=1e-4
a,b = 0,1

def bisection(f, a, b, tol):
    if f(a)*f(b) >= 0:
        print("Bisection method fails.")
    
    iteration = 0
    while (b - a)/2 > tol:
        c = (a + b)/2
        if f(c) == 0 or (b - a)/2 < tol:
            return c, iteration
        elif f(a)*f(c) < 0:
            b = c
        else:
            a = c
        iteration += 1
    return (a + b)/2, iteration

root, iteration = bisection(f, a, b, tol)
print(f"Root: {root}, Iteration: {iteration}")