import numpy as np
import matplotlib.pyplot as plt

def coefficients(x_data, y_data):
    n = len(x_data)
    a = y_data.copy() * 1.0

    for k in range(1,n):
        a[k:n] = (a[k:n] - a[k-1]) / (x_data[k:n] - x_data[k-1])
    return a

def evalute_poly(a, x_data , x):
    n = len(x_data) - 1
    p = a[n]
    for k in range(1,n+1):
        p = a[n-k] + p * (x - x_data[n-k])
    return p

def divided_diff(x_data, y_data):
    n = len(y_data)
    diff_table = np.zeros([n,n])
    diff_table[ :, 0] = y_data

    for j in range(1,n):
        for i in range(0, n-j):
            diff_table[i, j] = (diff_table[i+1, j-1] - diff_table[i,j-1]) / (x_data[i+j] - x_data[i])
    return diff_table

def main():
    x_data = np.array([-1.2, 0.3, 1.1])
    y_data = np.array([-5.76, -5.61, -3.69])
    a_coef = coefficients(x_data, y_data)
    dt = divided_diff(x_data, y_data)

    interval = 0.1
    x_plt = np.arange(x_data[0], x_data[len(x_data)-1] + interval, interval)
    y_plt = evalute_poly(a_coef, x_data, x_plt)
    print("Diff table: \n", dt)
    print("\na = ", a_coef)

    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, 'ro', label='Dữ liệu gốc')
    plt.plot(x_plt, y_plt, 'b-', label='Đa thức nội suy')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Đồ thị nội suy Newton')
    plt.legend()
    plt.grid(True)
    plt.show()

main()