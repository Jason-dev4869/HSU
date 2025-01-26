import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def system3(x, y):
    y1, y2 = y
    dy1_dx = y2
    dy2_dx = -2 * y2 - 3 * y1**2
    return [dy1_dx, dy2_dx]

y_init3 = [0, 0]
x_span3 = (0, 2)
x_eval3 = np.linspace(0, 2, 100)

sol3 = solve_ivp(system3, x_span3, y_init3, t_eval=x_eval3)

plt.plot(sol3.t, sol3.y[0], label="y(x)", color="red")
plt.xlabel("x")
plt.ylabel("y(x)")
plt.grid(True)
plt.legend()
plt.show()
