def f(x):
    return x**2 - 2

def secant_method(f, x0, x1, tol=1e-9):
    while abs(x1 - x0) > tol:
        f0, f1 = f(x0), f(x1)
        if f1 - f0 == 0:
            return None
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x2
        return x1

def main():
    x0, x1 = 1, 2
    tol = 1e-9
    root = secant_method(f, x0, x1, tol)
    print(root)

main()