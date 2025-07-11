"""
Teste específico dos problemas identificados
"""

import numpy as np
from core import EDPCatalog, GalerkinSolver, ConvergenceAnalyzer

def test_poisson_fix():
    """Testa se Poisson 1D agora converge"""
    print("🔧 TESTANDO CORREÇÃO DA EQUAÇÃO DE POISSON...")
    
    catalog = EDPCatalog()
    solver = GalerkinSolver()
    problem = catalog.get_problem('poisson_1d')
    
    errors = []
    n_values = [5, 10, 15, 20]
    
    for n in n_values:
        solution = solver.solve(problem, n)
        
        # Calcular erro manualmente
        x_vals = np.linspace(0, 1, 100)
        y_num = solution(x_vals)
        y_exact = np.sin(np.pi * x_vals)
        error = np.sqrt(np.mean((y_num - y_exact)**2))
        errors.append(error)
        
        print(f"  N={n:2d}: Erro = {error:.6f}")
    
    # Verificar se está convergindo
    if errors[0] > errors[-1]:
        print("  ✅ POISSON AGORA ESTÁ CONVERGINDO!")
    else:
        print("  ❌ Poisson ainda não converge adequadamente")
    
    return errors

def test_helmholtz_fix():
    """Testa se Helmholtz 2D não dá mais NaN"""
    print("\n🔧 TESTANDO CORREÇÃO DO HELMHOLTZ 2D...")
    
    catalog = EDPCatalog()
    problem = catalog.get_problem('helmholtz_2d')
    
    try:
        # Testar solução analítica
        x, y = 0.5, 0.5
        analytical_value = problem['analytical'](x, y)
        
        if np.isnan(analytical_value):
            print("  ❌ Solução analítica ainda dá NaN")
        else:
            print(f"  ✅ HELMHOLTZ 2D SOLUÇÃO ANALÍTICA OK: {analytical_value:.6f}")
            
        return True
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def test_heat_realistic():
    """Testa se a equação do calor tem erro mais realista"""
    print("\n🔧 TESTANDO EQUAÇÃO DO CALOR COM TEMPO MAIOR...")
    
    catalog = EDPCatalog()
    solver = GalerkinSolver()
    analyzer = ConvergenceAnalyzer(solver)
    problem = catalog.get_problem('heat_1d')
    
    errors = analyzer.analyze_convergence(problem, [5, 10, 15])
    
    print(f"  Erros: {[f'{e:.2e}' for e in errors]}")
    
    if min(errors) > 1e-10:  # Erro mais realista
        print("  ✅ CALOR AGORA TEM ERRO MAIS REALISTA")
    else:
        print("  ⚠️ Calor ainda pode ter erro muito baixo")
    
    return errors

if __name__ == '__main__':
    print("=" * 60)
    print("🔍 TESTE DAS CORREÇÕES IMPLEMENTADAS")
    print("=" * 60)
    
    test_poisson_fix()
    test_helmholtz_fix()
    test_heat_realistic()
    
    print("\n" + "=" * 60)
    print("✅ TESTES DE CORREÇÃO CONCLUÍDOS")
    print("=" * 60)
