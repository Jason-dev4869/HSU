import numpy as np

n = 8
a = np.zeros((n,n))
a[0::2, 0::2] = 1 
a[1::2, 1::2] = 1
print(a)