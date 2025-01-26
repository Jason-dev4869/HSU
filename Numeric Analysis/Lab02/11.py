import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-np.pi, np.pi, 0.1)
y_sin = np.sin(x)
y_cos = np.cos(x)
plt.title('Lab 02 Excercise 11', loc = 'center')
plt.plot(x, y_sin, color = 'b')
plt.plot(x, y_cos, color = 'r', linestyle = '--')
plt.grid(True)
plt.legend()
plt.show()