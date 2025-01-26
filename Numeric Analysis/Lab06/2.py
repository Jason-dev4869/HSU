import numpy as np

x = np.array([0, 0.1, 0.2, 0.3, 0.4])
f = np.array([0.0000, 0.0819, 0.1341, 0.1646, 0.1797])

h1 = 0.2
p = 2

g_h1 = (f[2] - f[0]) / (2 * h1)
g_h2 = (f[1] - f[0]) / (2 * (h1 / 2))

G = ((2**p) * g_h2 - g_h1) / ((2**p) - 1)

print(f"g(h=0.2) = {g_h1:.5f}")
print(f"g(h=0.1) = {g_h2:.5f}")
print(f"f'(0) = {G:.5f}")