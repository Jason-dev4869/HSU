import numpy as np

def gauss_eliminate(MA, vb):
    n = len(vb)
    A = MA.copy()
    b = vb.copy()

    for k in range(0, n - 1):    
        for  i in range(k + 1, n):
            if A[i, k] != 0.0:
                lam = A [i, k] / A[k, k]
                A[i,k:n] = A[i, k:n] - lam * A[k,k:n]
                b[i] = b[i] - lam * b[k]
    
    for k in range(n-1, -1, -1):
        b[k] = (b[k] - np.dot(A[i, k + 1:n], b[k + 1:n])) / A[k,k]
    return b

def main():
    A = np.array([[0, 2, 3], [1, 1, 1], [2, 0, 1]], dtype=float)
    b = np.array([[13], [6], [5]], dtype=float)
    x = gauss_eliminate(A, b)
    print("Result: \n" , x)

main()