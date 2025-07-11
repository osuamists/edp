#!/usr/bin/env python3
"""
Teste específico do solver
"""

import sys
sys.path.insert(0, 'core')
import numpy as np

try:
    from problems import EDPCatalog
    from galerkin_solver import GalerkinSolver
    
    print("Testando solver específico...")
    
    # Testar Onda
    catalog = EDPCatalog()
    problem = catalog.get_problem('wave_1d')
    solver = GalerkinSolver()
    
    print("Resolvendo com 5 termos...")
    solution = solver.solve(problem, 5)
    print("✅ Solver funcionou!")
    
    # Testar a solução
    x_test = np.linspace(0, 1, 10)
    t_test = 0.1
    u_vals = solution(x_test, t_test)
    print(f"✅ Solução avaliada: {len(u_vals)} pontos")
    print(f"   Valores: {u_vals[:3]}...")
    
    print("Sistema funcionando!")
    
except Exception as e:
    print(f"❌ Erro específico: {e}")
    import traceback
    traceback.print_exc()
