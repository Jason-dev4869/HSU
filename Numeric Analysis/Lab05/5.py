import numpy as np

def f(x):
    return x**2 - 2

def false_position_method(f,a,b,tol=1e-9):
    if f(a)*f(b) >= 0:
        print("Bisection method fails.")
        return None
    c = a
    while abs(b - a) > tol:
        c = a - (f(a) * (b - a)) / (f(b) - f(a))
        if f(c) == 0.0:
            return c
        if f(c)*f(a) < 0:
            b = c
        else:
            a = c
    return (a + b)/2

def main():
    a,b = 0,2
    tol = 1e-9
    root = false_position_method(f,a,b,tol)
    print(f"root = {root}")

main()