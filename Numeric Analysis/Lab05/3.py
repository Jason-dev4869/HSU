import numpy as np

def f(x):
    return x - np.tan(x)

def rootsearch(f,a,b,dx):
    intervals = []
    x1 = a
    f1 = f(x1)
    x2 = x1 + dx
    while x2 <= b:
        f2 = f(x2)
        if f1 * f2 < 0:
            intervals.append((x1,x2))
        x1, f1 = x2, f2
        x2 = x1 + dx
    return intervals

tol = 1e-6

def bisection(f,a,b,tol):
    if f(a) * f(b) > 0:
        return None
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        if f(c) == 0 or (b - a) / 2 < tol:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2

def main():
    a,b = 0, 20
    dx = 0.01
    intervals = rootsearch(f,a,b,dx)
    for interval in intervals:
        root = bisection(f,interval[0],interval[1],tol)
        print(root)

main()