import numpy as np

def f(x):
    return np.sin(x) - 0.1 * x

def df(x):
    return np.cos(x) - 0.1

def newton_raphson_improve(f, df, a, b, tol = 1e-9):
    fa = f(a)
    if fa == 0.0:
        return a
    fb = f(b)
    if fb == 0.0:
        return b
    if np.sign(fa) == np.sign(fb):
        raise Exception("No found variable")
    x = (a + b) / 2.0
    for i in range(30):
        fx = f(x)
        if fx == 0.0:
            return x
        if np.sign(fa) != np.sign(fx):
            b = x
        else:
            a = x
        dfx = df(x)
        try:
            dx = -fx / dfx
        except ZeroDivisionError:
            dx = b - a
        x = x + dx
        if (b - x) * (x - a) < 0.0:
            dx = 0.5*(b - a)
            x = a + dx
        print("a={:6.4f}, b={:6.4f}, x={:6.4f}, dx={:6.4f}".format(a,b,x,dx))
        if abs(dx) < tol * max(abs(b), 1.0):
            return x
    print("Too many iterations in Newton-Raphson")

def main():
    start, end = 0.1, 3
    tol = 1e-9
    x = newton_raphson_improve(f,df,start,end,tol)
    print(f"The root of the equation is {x:6.4f}")

main()