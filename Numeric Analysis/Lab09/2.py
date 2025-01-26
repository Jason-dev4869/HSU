import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def system2(x, y):
    y1, y2 = y
    dy1_dx = y2
    dy2_dx = -(1 - 0.2 * x) * y1**2
    return [dy1_dx, dy2_dx]

y_init2 = [0, 0]
x_span2 = (0, math.pi / 2)
x_eval2 = np.linspace(0, math.pi / 2, 100)

sol2 = solve_ivp(system2, x_span2, y_init2, t_eval=x_eval2)

plt.plot(sol2.t, sol2.y[0], label="y(x)", color="green")
plt.xlabel("x")
plt.ylabel("y(x)")
plt.grid(True)
plt.legend()
plt.show()
