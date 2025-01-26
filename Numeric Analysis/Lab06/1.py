import numpy as np

x = np.array([0, 0.1, 0.2, 0.3, 0.4])
f = np.array([0.0000, 0.0819, 0.1341, 0.1646, 0.1797])
h = 0.1

f_prime_0 = (-3*f[0] + 4*f[1] - f[2]) / (2*h)
f_double_prime_0 = (f[1] - 2*f[0] + f[2]) / (h**2)

f_prime_02 = (f[3] - f[1]) / (2*h)
f_double_prime_02 = (f[3] - 2*f[2] + f[1]) / (h**2)

print(f"f'(0) = {f_prime_0:.4f}, f''(0) = {f_double_prime_0:.4f}")
print(f"f'(0.2) = {f_prime_02:.4f}, f''(0.2) = {f_double_prime_02:.4f}")
