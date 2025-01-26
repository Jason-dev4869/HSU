import numpy as np

n = 4
a = np.random.randint(0, 10, size=(n,n))
print("Array: \n", a)
b = np.sort(a, axis=None).reshape(n,n)
print("Sorted array: \n", b)