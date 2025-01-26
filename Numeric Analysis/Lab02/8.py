import numpy as np

n = 4
a = np.random.randint(0, 10, size=(n,n))
print("Array: \n", a)
b = np.zeros((n,n), dtype=int)
for i in range(n):
    for j in range(n):
        b[j][i] = a[i][j]

print("Array Transposed: \n", b)