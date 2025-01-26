import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def system(x, y):
    y1, y2, y3 = y
    dy1_dx = y2
    dy2_dx = y3
    dy3_dx = 2 * y3 + 6 * x * y1
    return [dy1_dx, dy2_dx, dy3_dx]

y_init = [2, 0, 0]
x_span = (0, 5)
x_eval = np.linspace(0, 5, 100)

sol = solve_ivp(system, x_span, y_init, t_eval=x_eval)

plt.plot(sol.t, sol.y[0], label="y(x)", color="blue")
plt.xlabel("x")
plt.ylabel("y(x)")
plt.grid(True)
plt.legend()
plt.show()
