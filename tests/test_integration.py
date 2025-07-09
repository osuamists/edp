"""
Teste completo do sistema EDP
"""

import sys
import os
# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sympy as sp
import numpy as np
from core.problems import EDPCatalog
from core.methods.least_squares_method import LeastSquaresMethod

def test_catalog():
    """Testar catálogo de problemas"""
    print("=== TESTE 1: CATÁLOGO DE PROBLEMAS ===")
    try:
        catalog = EDPCatalog()
        print("✓ Catálogo criado com sucesso")
        
        # Listar problemas
        print("Problemas disponíveis:")
        for key, problem in catalog.problems.items():
            print(f"  - {key}: {problem['nome']}")
        
        # Testar problema específico
        test_problem = catalog.get_problem("test_problem")
        print(f"✓ Problema teste carregado: {test_problem['nome']}")
        
        return catalog, test_problem
        
    except Exception as e:
        print(f"✗ Erro no catálogo: {e}")
        return None, None

def test_least_squares(test_problem):
    """Testar método dos mínimos quadrados"""
    print("\n=== TESTE 2: MÉTODO DOS MÍNIMOS QUADRADOS ===")
    
    try:
        # Configurar método
        method = LeastSquaresMethod()
        method.domain = list(test_problem['domain'])
        method.equation = test_problem['equation']
        
        print(f"✓ Método configurado")
        print(f"  Domínio: {method.domain}")
        print(f"  Equação: {method.equation}")
        
        best_error = float('inf')
        best_solution = None
        
        for n_terms in [2, 3]:  # REDUZIR para 2 e 3 termos apenas
            print(f"\n--- Testando com {n_terms} termos ---")
            
            try:
                solution = method.solve(n_terms=n_terms)
                
                if solution is not None:
                    print(f"✓ Solução obtida: {solution}")
                    
                    # Verificar qualidade
                    is_good = method.verify_solution(solution)
                    
                    if is_good:
                        print(f"✓ Solução com {n_terms} termos é ACEITÁVEL")
                        
                        # CORREÇÃO: Cálculo de erro mais robusto
                        try:
                            x = sp.Symbol('x')
                            analytical = sp.sin(sp.pi * x)
                            
                            error = calculate_solution_error(solution, analytical, method.domain)
                            print(f"  Erro L2: {error:.8f}")
                            
                            if error < best_error:
                                best_error = error
                                best_solution = solution
                        except Exception as e:
                            print(f"  AVISO: Não foi possível calcular erro L2: {e}")
                    else:
                        print(f"⚠ Solução com {n_terms} termos precisa melhorar")
                else:
                    print(f"✗ Falha com {n_terms} termos")
                    
            except Exception as e:
                print(f"✗ Erro com {n_terms} termos: {e}")
                import traceback
                traceback.print_exc()
                
        return best_solution, best_error if best_solution is not None else None
        
    except Exception as e:
        print(f"✗ Erro no método dos mínimos quadrados: {e}")
        return None, None

def calculate_solution_error(numerical, analytical, domain):
    """Calcular erro L2 entre solução numérica e analítica"""
    x = sp.Symbol('x')
    
    # Diferença quadrática
    diff_squared = (numerical - analytical)**2
    
    # Integrar no domínio
    error_integral = sp.integrate(diff_squared, (x, domain[0], domain[1]))
    
    # Erro L2
    return float(sp.sqrt(error_integral).evalf())

def test_integration():
    """Testar integração simbólica"""
    print("\n=== TESTE 3: INTEGRAÇÃO SIMBÓLICA ===")
    
    x = sp.Symbol('x')
    
    test_cases = [
        (x**2, (x, 0, 1), 1/3, "Polinômio simples"),
        (sp.sin(sp.pi * x), (x, 0, 1), 2/sp.pi, "Seno"),
        (sp.sin(sp.pi * x)**2, (x, 0, 1), 1/2, "Seno ao quadrado"),
        (sp.sin(sp.pi * x) * sp.sin(2*sp.pi * x), (x, 0, 1), 0, "Ortogonalidade")
    ]
    
    for func, limits, expected, description in test_cases:
        try:
            result = sp.integrate(func, limits)
            numerical_result = float(result.evalf())
            expected_val = float(expected)
            error = abs(numerical_result - expected_val)
            
            print(f"  {description}:")
            print(f"    ∫{func} dx = {numerical_result:.8f}")
            print(f"    Esperado: {expected_val:.8f}")
            print(f"    Erro: {error:.8e}")
            
            if error < 1e-10:
                print("    ✓ Correto")
            else:
                print("    ⚠ Possível problema")
                
        except Exception as e:
            print(f"    ✗ Erro: {e}")

def main():
    """Função principal de teste"""
    print("=== TESTE COMPLETO DO SISTEMA EDP ===\n")
    
    # Teste 1: Catálogo
    catalog, test_problem = test_catalog()
    
    if not catalog or not test_problem:
        print("❌ Falha nos testes básicos")
        return
    
    # Teste 2: Método numérico
    solution, error = test_least_squares(test_problem)
    
    # Teste 3: Integração
    test_integration()
    
    # Resumo final
    print("\n=== RESUMO FINAL ===")
    
    if solution is not None:
        print(f"✓ Sistema funcionando!")
        print(f"  Melhor solução obtida: {solution}")
        print(f"  Erro L2: {error:.8f}")
        
        if error < 0.01:
            print("🎉 EXCELENTE! Precisão muito boa")
        elif error < 0.1:
            print("👍 BOM! Precisão aceitável")
        else:
            print("⚠ RAZOÁVEL! Pode melhorar")
    else:
        print("❌ Sistema com problemas")
        
    print("\nPara usar o sistema, execute:")
    print("python examples/integrated_example.py")

if __name__ == "__main__":
    main()