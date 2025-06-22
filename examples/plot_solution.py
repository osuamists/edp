import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Importar os métodos implementados
from core.methods.galerkin_method import GalerkinMethod
# Exemplo futuro: from core.methods.rayleigh_ritz_method import RayleighRitzMethod

# 1. Definir a EDP simbólica
x = sp.Symbol('x')
u = sp.Function('u')
equation = sp.diff(u(x), x, 2) + sp.pi**2 * sp.sin(sp.pi * x)
domain = (0, 1)
boundary_conditions = [(0, 0), (1, 0)]

# 2. Lista de métodos a comparar
metodos = {
    "Galerkin": GalerkinMethod,
    # "Rayleigh-Ritz": RayleighRitzMethod,
    # "Colocação": ColocacaoMethod,
    # ...
}

# 3. Avaliação dos métodos
x_vals = np.linspace(domain[0], domain[1], 200)
y_real = np.sin(np.pi * x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_real, label="Solução Exata: sin(πx)", linewidth=2, color='black')

for nome, classe in metodos.items():
    metodo = classe(equation, domain, boundary_conditions)
    solution_sym = metodo.solve(n_terms=3)
    u_aprox = sp.lambdify(x, solution_sym, modules='numpy')

    # Avaliação ponto a ponto (segura)
    y_aprox = np.array([float(u_aprox(xi)) for xi in x_vals])
    erro = np.max(np.abs(y_aprox - y_real))
    
    plt.plot(x_vals, y_aprox, '--', label=f"{nome} (erro máx: {erro:.1e})")

plt.title("Comparação dos Métodos Numéricos")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
