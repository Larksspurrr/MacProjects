import sympy as sym

iterations: dict = {}
current_x_val: float = 0.5

def f(x):
    return 2*x**3 + x**2 - x + 7
    # return x**3 - 4*x**2 + 1

x = sym.Symbol('x')
fprime = sym.diff(f(x), x)

def newtons(x_val):
    denominator = fprime.subs(x, x_val)
    if denominator == 0:
        return sym.zoo
    else:
        return x_val - (f(x_val) / denominator)

for i in range(1, 11):
    iterations[f"x_{i}"] = round(newtons(current_x_val), 5)
    current_x_val = iterations[f"x_{i}"]

print([(key, value) for key, value in iterations.items()], end="\n")
