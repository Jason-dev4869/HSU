import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 + 10*x**2 + 5

def sign(x):
    return np.sign(x)

def root_search(f,a, b, dx):
    x1 = a
    f1  = f(x1)
    x2 = a + dx
    f2 = f(x2)
    while sign(f1) == sign(f2):
        if x1 >= b:
            return None, None
        x1 = x2
        f1 = f2
        x2 = x1 + dx
        f2 = f(x2)
    return x1, x2

def main():
    a, b = 0, 1
    dx = 0.0001

    root1, root2 = root_search(f,a,b,dx)
    if root1 is not None:
        print(f"Nghiệm nằm trong khoảng [{root1}, {root2}]")
    else:
        print("None")

    x_vals = np.linspace(a - 0.5, b + 0.5, 400)
    y_vals = f(x_vals)

    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label=r"$f(x) = x^3 - 10x^2 + 5$")
    plt.axhline(0, color='black', linewidth=0.5)
    if root1 is not None:
        plt.axvline(root1, color='r', linestyle='--', label=f'Nghiệm tại x = {root1:.4f}')
    plt.title("Đồ thị của hàm f(x) = $x^3 - 10x^2 + 5$")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.show()

main()