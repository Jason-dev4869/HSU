from numpy import sign

def f(x):
    return x**4 - 2*x**3 - 7*x**2 + 3

def df(x):
    return 4*x**3 - 6*x**2 - 14*x

def newton_raphson(f, df, a,b, tol=1e-9):
    fa = f(a)
    if fa == 0:
        return a
    fb = f(b)
    if fb == 0:
        return b
    if sign(fa) == sign(fb):
        raise Exception(f"Cannot found variable in [{a},{b}]")
    x = (a + b) / 2
    while abs(f(x)) >= tol:
        x = x - f(x) / df(x)
    return x

def main():
    start, end = 0.1, 3
    tol = 1e-9
    x = newton_raphson(f,df,start,end,tol)
    print(f"The root of the equation is {x:6.4f}")

main()