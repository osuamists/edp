# test_simple.py

"""
Teste simples do EDP Solver
"""

from core.problems import EDPCatalog
from core.galerkin_solver import GalerkinSolver
import numpy as np

def test_poisson():
    """Teste simples da equação de Poisson"""
    print("Testando Equação de Poisson...")
    
    catalog = EDPCatalog()
    problem = catalog.get_problem("poisson")
    
    solver = GalerkinSolver(problem)
    solution = solver.solve(3)
    
    # Testar em alguns pontos
    x_test = np.array([0.25, 0.5, 0.75])
    y_numerical = solution(x_test)
    y_analytical = problem["analytical"](x_test)
    
    print(f"x = {x_test}")
    print(f"Numérico: {y_numerical}")
    print(f"Analítico: {y_analytical}")
    print(f"Erro: {np.abs(y_numerical - y_analytical)}")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("TESTE SIMPLES DO EDP SOLVER")
    print("=" * 50)
    
    try:
        test_poisson()
        print("\n✓ Teste concluído com sucesso!")
    except Exception as e:
        print(f"\n✗ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
