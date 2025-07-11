#!/usr/bin/env python3
"""
Teste simples para verificar importações
"""

import sys
sys.path.insert(0, 'core')

try:
    print("Testando importações...")
    from problems import EDPCatalog
    print("✅ problems.py importado")
    
    from galerkin_solver import GalerkinSolver  
    print("✅ galerkin_solver.py importado")
    
    # Testar catálogo
    catalog = EDPCatalog()
    print("✅ EDPCatalog criado")
    
    problem = catalog.get_problem('wave_1d')
    print("✅ Problema wave_1d obtido")
    
    # Testar solver
    solver = GalerkinSolver()
    print("✅ GalerkinSolver criado")
    
    print("\nTodos os módulos funcionando!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
