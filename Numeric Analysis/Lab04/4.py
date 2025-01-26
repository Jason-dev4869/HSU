import numpy as np

def neville(x_data, y_data, x):
    m = len(x_data)
    y = y_data.copy() * 1.0

    for k in range(1, m):
        y[0:m - k] = ((x - x_data[k:m]) * y[0:m - k] + (x_data[0:m - k] - x) * y[1:m - k + 1] / (x_data[0:m - k] - x_data[k:m]))
    return y[0]

def main():
    x_data = np.array([0, 0.5, 1, 1.5, 2])
    y_data = np.array([-1.00, 1.75, 4.00, 5.75, 7.00])

    x = np.pi / 4
    y = neville(x_data, y_data, x)
    print("y = ",y)
    
main()