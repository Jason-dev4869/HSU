import math

def f(x):
    return math.sqrt(x) * math.cos(x)

def trapezoidal_rule_recursive(f, a, b, n, tol):
    h = (b - a) / n
    sum = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        sum += f(a + i * h)
    
    integral = sum * h
    if n == 1:
        return integral
    else:
        prev_integral = trapezoidal_rule_recursive(f, a, b, n // 2, tol)
        if abs(integral - prev_integral) < tol:
            return integral
        else:
            return prev_integral

def integral_with_trapezoidal_rule(f, a, b, tol):
    n = 2
    result = trapezoidal_rule_recursive(f, a, b, n, tol)
    return result

a = 0
b = math.pi
tolerance = 1e-6

result = integral_with_trapezoidal_rule(f, a, b, tolerance)
print(f"Result: {result}")