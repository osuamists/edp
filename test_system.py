"""
Teste simples do sistema EDP
"""

def test_imports():
    try:
        from core import EDPCatalog, GalerkinSolver, ConvergenceAnalyzer
        from visualizer import ResultVisualizer
        print("✓ Todas as importações funcionaram")
        return True
    except Exception as e:
        print(f"✗ Erro na importação: {e}")
        return False

def test_catalog():
    try:
        from core import EDPCatalog
        catalog = EDPCatalog()
        problems = ['poisson_1d', 'heat_1d', 'wave_1d', 'helmholtz_2d']
        
        for problem_name in problems:
            problem = catalog.get_problem(problem_name)
            print(f"✓ {problem_name}: {problem['nome']}")
        
        return True
    except Exception as e:
        print(f"✗ Erro no catálogo: {e}")
        return False

def test_solver():
    try:
        from core import EDPCatalog, GalerkinSolver
        
        catalog = EDPCatalog()
        solver = GalerkinSolver()
        
        # Testar Poisson 1D
        problem = catalog.get_problem('poisson_1d')
        solution = solver.solve(problem, 10)
        
        print(f"✓ Solver funcionou, solução: {len(solution)} coeficientes")
        return True
    except Exception as e:
        print(f"✗ Erro no solver: {e}")
        return False

if __name__ == '__main__':
    print("=== Teste do Sistema EDP ===")
    
    if test_imports():
        if test_catalog():
            if test_solver():
                print("\n✓ Todos os testes passaram!")
            else:
                print("\n✗ Falha no teste do solver")
        else:
            print("\n✗ Falha no teste do catálogo")
    else:
        print("\n✗ Falha nas importações")
