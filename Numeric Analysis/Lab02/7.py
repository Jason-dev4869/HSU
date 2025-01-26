import numpy as np

n = 6
a = np.random.randint(0, 10, size=n)
S_index_even = np.sum(a[::2])
S_index_odd = np.sum(a[1::2])
print("Array: ", a)
print("Sum of even indices: ", S_index_even)
print("Sum of odd indices: ", S_index_odd)