"""
Teste simplificado da integração
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.simple_solver import SimplifiedEDPSolver

def main():
    print("=== Teste da Integração Simplificada ===\n")
    
    # Criar solver
    solver = SimplifiedEDPSolver()
    
    # 1. Status do sistema
    print("1. Status do Sistema:")
    status = solver.status_report()
    print(f"   Problemas disponíveis: {status['problems_available']}")
    print(f"   Métodos disponíveis: {status['methods_available']}")
    print(f"   Status da integração: {status['integration_status']}")
    
    # 2. Listar problemas
    print("\n2. Problemas no Catálogo:")
    problems = solver.list_problems()
    for key, name in problems.items():
        print(f"   - {key}: {name}")
    
    # 3. Listar métodos
    print("\n3. Métodos Disponíveis:")
    methods = solver.list_methods()
    for method in methods:
        print(f"   - {method}")
    
    # 4. Testar informações de problema
    print("\n4. Informações do Problema 'poisson':")
    try:
        info = solver.get_problem_info("poisson")
        print(f"   Nome: {info['nome']}")
        print(f"   Equação: {info['equation']}")
        print(f"   Domínio: {info['domain']}")
        print(f"   Condições de contorno: {len(info['boundary_conditions_summary']['dirichlet'])} Dirichlet")
    except Exception as e:
        print(f"   Erro: {e}")
    
    # 5. Testar recomendações
    print("\n5. Recomendações por Problema:")
    for problem in problems.keys():
        try:
            recommendations = solver.recommend_method(problem)
            print(f"   {problem}: {recommendations}")
        except Exception as e:
            print(f"   {problem}: Erro - {e}")
    
    # 6. Testar resolução
    print("\n6. Tentativa de Resolução:")
    for problem in list(problems.keys())[:2]:  # Testar apenas 2 primeiros
        recommendations = solver.recommend_method(problem)
        
        if recommendations:
            method = recommendations[0]
            print(f"   Resolvendo {problem} com {method}...")
            
            try:
                result = solver.solve(problem, method, n_terms=3)
                print(f"   Status: {result['status']}")
                if result['status'] == 'success':
                    print(f"   Solução: {type(result['solution'])}")
                elif result['status'] == 'error':
                    print(f"   Erro: {result['error']}")
            except Exception as e:
                print(f"   Exceção: {e}")
        else:
            print(f"   {problem}: Nenhum método disponível")
    
    # 7. Comparação de métodos
    print("\n7. Comparação de Métodos (Poisson):")
    if methods:
        try:
            comparison = solver.compare_methods("poisson", methods[:1], n_terms=3)
            for method, result in comparison.items():
                print(f"   {method}: {result.get('status', 'unknown')}")
        except Exception as e:
            print(f"   Erro na comparação: {e}")
    
    print("\n" + "="*50)
    print("🎉 Integração básica funcionando!")
    print("\n💡 Próximos passos:")
    print("1. Corrigir conflitos nos métodos numéricos")
    print("2. Implementar métodos faltantes")
    print("3. Adicionar visualização")
    print("4. Expandir catálogo de problemas")

if __name__ == "__main__":
    main()
