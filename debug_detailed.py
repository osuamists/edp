"""
Debug detalhado dos problemas
"""

import numpy as np
from core import EDPCatalog, GalerkinSolver

def debug_poisson():
    print("🔍 DEBUG DETALHADO - POISSON 1D")
    print("-" * 40)
    
    catalog = EDPCatalog()
    solver = GalerkinSolver()
    problem = catalog.get_problem('poisson_1d')
    
    print(f"Solução analítica: {problem['analytical']}")
    
    # Testar com poucos termos
    solution = solver.solve(problem, 3)
    
    # Avaliar em alguns pontos
    x_test = np.array([0.2, 0.5, 0.8])
    y_num = solution(x_test)
    y_exact = problem['analytical'](x_test)
    
    print(f"x = {x_test}")
    print(f"Numérico  = {y_num}")
    print(f"Analítico = {y_exact}")
    print(f"Diferença = {y_num - y_exact}")
    
    # Verificar se todas as diferenças são zero
    if np.allclose(y_num, y_exact, atol=1e-10):
        print("⚠️ Soluções são numericamente idênticas!")
        print("Isso sugere que a solução analítica pode ser representada exatamente pelas funções de base.")
    
def debug_heat():
    print("\n🔍 DEBUG DETALHADO - CALOR 1D")
    print("-" * 40)
    
    catalog = EDPCatalog()
    solver = GalerkinSolver()
    problem = catalog.get_problem('heat_1d')
    
    # Testar com poucos termos
    solution = solver.solve(problem, 3)
    
    # Avaliar em t = 0.1
    x_test = np.array([0.2, 0.5, 0.8])
    t_test = 0.1
    y_num = solution(x_test, t_test)
    y_exact = problem['analytical'](x_test, t_test)
    
    print(f"x = {x_test}, t = {t_test}")
    print(f"Numérico  = {y_num}")
    print(f"Analítico = {y_exact}")
    print(f"Diferença = {y_num - y_exact}")
    
    if np.allclose(y_num, y_exact, atol=1e-10):
        print("⚠️ Soluções são numericamente idênticas!")

def test_non_trivial_poisson():
    print("\n🔍 TESTE COM POISSON MAIS COMPLEXO")
    print("-" * 40)
    
    # Vou criar um problema temporário com solução não trivial
    from core.galerkin_solver import GalerkinSolver
    
    solver = GalerkinSolver()
    
    # Problema com solução u = x(1-x)(0.5-x) 
    problem_custom = {
        "domain": (0, 1),
        "boundary_conditions": [("dirichlet", 0, 0), ("dirichlet", 1, 0)],
        "analytical": lambda x: x * (1 - x) * (0.5 - x),
        "source": lambda x: 2 - 6*x,  # -d²u/dx² = 2 - 6x
        "tipo": "eliptica_1d"
    }
    
    solution = solver.solve(problem_custom, 5)
    
    x_test = np.array([0.2, 0.4, 0.6, 0.8])
    y_num = solution(x_test)
    y_exact = problem_custom['analytical'](x_test)
    
    print(f"x = {x_test}")
    print(f"Numérico  = {y_num}")
    print(f"Analítico = {y_exact}")
    print(f"Erro abs  = {np.abs(y_num - y_exact)}")
    print(f"Erro L2   = {np.sqrt(np.mean((y_num - y_exact)**2)):.6f}")

if __name__ == '__main__':
    debug_poisson()
    debug_heat()
    test_non_trivial_poisson()
