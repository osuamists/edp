import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from core.methods.galerkin_method import GalerkinMethod # CERTO



# 1. Definir variáveis simbólicas e EDP
x = sp.Symbol('x')
u = sp.Function('u')(x)
equation = sp.Eq(sp.diff(u, x, 2), -sp.pi**2 * sp.sin(sp.pi * x))
domain = (0, 1)
boundary_conditions = [(0, 0), (1, 0)]

method = GalerkinMethod(equation.rhs, domain, boundary_conditions)
solution_sym = method.solve(n_terms=3)


u_aprox = sp.lambdify(x, solution_sym, modules=['numpy'])
u_real = lambda x: np.sin(np.pi * x)

# 2. Gerar pontos para plotagem
x_vals = np.linspace(domain[0], domain[1], 200)
y_aprox = u_aprox(x_vals)
y_real = u_real(x_vals)

#3.Plotar o gráfico
plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_aprox, label='Solução Aproximada (Galerkin)', linestyle='--')
plt.plot(x_vals, y_real, label='Solução Exata: sin(πx)', linestyle='-')
plt.title('Comparação da Solução da EDP')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


