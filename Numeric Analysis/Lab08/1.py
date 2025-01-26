import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return y - x

def euler_method(f, x_init, y_init, x_stop, h):
    X = np.linspace(x_init, x_stop, int((x_stop - x_init) / h) + 1)
    n = len(X)
    Y = np.zeros(n)
    Y[0] = y_init
    for i in range(0, n-1):
        Y[i+1] = Y[i] + h * f(X[i], Y[i])
    return X, Y

def exact_solution(x):
    return x + 1 - 0.5 * np.exp(x)

def main():
    x_init = 0.0
    y_init = 0.5
    x_stop = 2.0
    h1 = 0.1
    h2 = 0.05

    x1, y1 = euler_method(f, x_init, y_init, x_stop, h1)
    x2, y2 = euler_method(f, x_init, y_init, x_stop, h2)

    y_exact1 = exact_solution(x1)
    y_exact2 = exact_solution(x2)

    error1 = np.abs(y_exact1 - y1)
    error2 = np.abs(y_exact2 - y2)

    print(f"Results with h = {h1}:")
    print(f"x: {x1}")
    print(f"Euler approximation: {y1}")
    print(f"Exact solution: {y_exact1}")
    print(f"Absolute error: {error1}\n")

    print(f"Results with h = {h2}:")
    print(f"x: {x2}")
    print(f"Euler approximation: {y2}")
    print(f"Exact solution: {y_exact2}")
    print(f"Absolute error: {error2}\n")

    plt.plot(x1, y1, label='Euler Method (h = 0.1)', marker='o')
    plt.plot(x1, y_exact1, label='Exact Solution', linestyle='--')
    plt.plot(x2, y2, label='Euler Method (h = 0.05)', marker='x')
    plt.plot(x2, y_exact2, label='Exact Solution (h = 0.05)', linestyle='--')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

main()
