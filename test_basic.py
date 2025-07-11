"""
Teste mais simples possível
"""

print("=== Teste Básico ===")

try:
    from core import EDPCatalog, GalerkinSolver, ConvergenceAnalyzer
    print("✓ Importações OK")
    
    catalog = EDPCatalog()
    solver = GalerkinSolver()
    analyzer = ConvergenceAnalyzer(solver)
    print("✓ Objetos criados OK")
    
    # Testar um problema simples
    problem = catalog.get_problem('poisson_1d')
    print(f"✓ Problema obtido: {problem['nome']}")
    
    # Testar solver simples
    solution = solver.solve(problem, 5)
    print(f"✓ Solver executou, tipo da solução: {type(solution)}")
    
    # Testar convergência básica
    errors = analyzer.analyze_convergence(problem, [5, 10])
    print(f"✓ Análise de convergência executou, {len(errors)} erros")
    
    print("\n✓ TODOS OS TESTES BÁSICOS PASSARAM!")
    
except Exception as e:
    import traceback
    print(f"✗ Erro: {e}")
    print("Traceback completo:")
    traceback.print_exc()
