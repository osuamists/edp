# ALTERADO: A manipulação de sys.path foi removida.
# A execução com "python -m" já cuida para que os módulos sejam encontrados.
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


# Importar os métodos implementados
from core.methods.galerkin_method import GalerkinMethod
from core.methods.rayleigh_ritz_method import RayleighRitzMethod
# Exemplo futuro: from core.methods.rayleigh_ritz_method import RayleighRitzMethod

# 1. Definir os componentes da EDP: -u'' = f(x)
x = sp.Symbol('x')

# ALTERADO: Definimos APENAS o lado direito da equação, o f(x).
f_de_x = sp.pi**2 * sp.sin(sp.pi * x)

domain = (0, 1)
boundary_conditions = [(0, 0), (1, 0)]

# 2. Lista de métodos a comparar
metodos = {
    "Galerkin": GalerkinMethod,
    "Rayleigh-Ritz": RayleighRitzMethod,
    # "Rayleigh-Ritz": RayleighRitzMethod,
    # ...
}

# 3. Preparação do Gráfico
x_vals = np.linspace(domain[0], domain[1], 200)
y_real = np.sin(np.pi * x_vals)


plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_real, 'k-', linewidth=3, alpha=0.8, label="Solução Exata: sin(πx)")


# 4. Avaliação dos métodos
for nome, classe in metodos.items():
    print(f"--- Rodando método: {nome} ---")
    
    # ALTERADO: Passamos f_de_x em vez da equação inteira para a classe.
    metodo = classe(f_de_x, domain, boundary_conditions)
    
    solution_sym = metodo.solve(n_terms=3)

    # NOVO: Adicionamos uma verificação para garantir que a solução foi encontrada
    # Isso evita o erro 'NoneType' se o método solve() falhar.
    if solution_sym is not None:
        u_aprox_func = sp.lambdify(x, solution_sym, modules='numpy')

        # Avaliação ponto a ponto
        y_aprox = u_aprox_func(x_vals) # Usando a forma vetorizada, mais limpa
        erro = np.max(np.abs(y_aprox - y_real))
        
        plt.plot(x_vals, y_aprox, '--', label=f"{nome} (erro máx: {erro:.1e})")
        print(f"Solução encontrada. Erro máximo: {erro:.2e}")
    else:
        print(f"O método {nome} falhou em encontrar uma solução.")


plt.title("Comparação dos Métodos Numéricos")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()