"""
Testes para verificar a integração entre EDPs e métodos numéricos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.solver import EDPSolver
import numpy as np

def test_basic_integration():
    """Teste básico da integração"""
    print("=== Teste de Integração Básica ===\n")
    
    try:
        # Criar solver
        solver = EDPSolver()
        print("✓ Solver criado com sucesso")
        
        # Listar problemas
        problems = solver.list_problems()
        print(f"✓ Problemas disponíveis: {list(problems.keys())}")
        
        # Listar métodos
        methods = solver.list_methods()
        print(f"✓ Métodos disponíveis: {methods}")
        
        # Testar definição de problema
        solver.set_problem("poisson")
        print("✓ Problema 'poisson' definido com sucesso")
        
        # Testar recomendações
        recommendations = solver.recommend_method("poisson")
        print(f"✓ Recomendações para Poisson: {recommendations}")
        
        # Testar informações do problema
        info = solver.get_problem_info("poisson")
        print(f"✓ Informações do problema obtidas: {info['nome']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no teste: {e}")
        return False

def test_method_compatibility():
    """Testa a compatibilidade entre problemas e métodos"""
    print("\n=== Teste de Compatibilidade ===\n")
    
    solver = EDPSolver()
    
    # Testa todos os problemas
    problems = ["poisson", "onda_1d", "calor", "helmholtz"]
    
    for problem in problems:
        try:
            recommendations = solver.recommend_method(problem)
            print(f"✓ {problem}: {recommendations}")
        except Exception as e:
            print(f"✗ {problem}: Erro - {e}")

def test_problem_validation():
    """Testa a validação de problemas"""
    print("\n=== Teste de Validação ===\n")
    
    solver = EDPSolver()
    
    for problem_name in solver.list_problems().keys():
        try:
            solver.set_problem(problem_name)
            print(f"✓ {problem_name}: Validação passou")
        except Exception as e:
            print(f"✗ {problem_name}: Erro de validação - {e}")

def test_solve_attempt():
    """Tenta resolver um problema simples"""
    print("\n=== Teste de Resolução ===\n")
    
    solver = EDPSolver()
    
    # Tenta resolver cada problema com métodos compatíveis
    for problem_name in ["poisson"]:  # Começar só com Poisson
        try:
            recommendations = solver.recommend_method(problem_name)
            
            for method in recommendations[:2]:  # Testa os 2 primeiros métodos
                try:
                    print(f"Tentando resolver {problem_name} com {method}...")
                    result = solver.solve(problem_name, method, n_terms=3)
                    print(f"✓ {problem_name} + {method}: Sucesso")
                except Exception as e:
                    print(f"✗ {problem_name} + {method}: {e}")
                    
        except Exception as e:
            print(f"✗ Erro geral para {problem_name}: {e}")

if __name__ == "__main__":
    print("Iniciando testes de integração...\n")
    
    success = True
    success &= test_basic_integration()
    test_method_compatibility()
    test_problem_validation()
    test_solve_attempt()
    
    print(f"\n{'='*50}")
    if success:
        print("🎉 Integração funcionando corretamente!")
    else:
        print("⚠️  Alguns problemas encontrados na integração")
    
    print("\n💡 Próximos passos:")
    print("1. Implementar métodos numéricos específicos")
    print("2. Adicionar visualização de resultados")
    print("3. Criar interface gráfica")
    print("4. Adicionar mais problemas ao catálogo")
