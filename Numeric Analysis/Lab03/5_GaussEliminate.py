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
    A = np.array([[1, 2, -1], [2, 5, -4], [3, 4, 2]], dtype=float)
    b = np.array([3, 5, 12], dtype=float)
    x = gauss_eliminate(A, b)
    print("x = \n",x)

    # Vô nghiệm (hệ nonsingular/linear dependent/phụ thuộc tuyến tính)
    A = np.array([[1, 1], [2, 2]], dtype=float)
    b = np.array([2, 2], dtype=float)
    x = gauss_eliminate(A, b)
    print("x = \n",x)

    # Vô số nghiệm (hệ singular/linear dependent/phụ thuộc tuyến tính)
    A = np.array([[1, 1], [2, 2]], dtype=float)
    b = np.array([2, 4], dtype=float)
    x = gauss_eliminate(A, b)
    print("x = \n",x)

main()