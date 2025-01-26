import numpy as np

a = np.ones((5,5))
print(a)
print("-----------------")
a[0,:] = 0
a[-1,:] = 0
a[:,0] = 0
a[:,-1] = 0
print(a)