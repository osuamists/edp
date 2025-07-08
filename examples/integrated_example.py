"""
Exemplo de uso do sistema integrado EDP + Métodos Numéricos
"""

from core.solver import EDPSolver
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Criar o solver principal
    solver = EDPSolver()
    
    print("=== Sistema Integrado de Resolução de EDPs ===\n")
    
    # 1. Listar problemas disponíveis
    print("1. Problemas disponíveis:")
    problems = solver.list_problems()
    for key, name in problems.items():
        print(f"   - {key}: {name}")
    
    # 2. Listar métodos disponíveis
    print("\n2. Métodos numéricos disponíveis:")
    methods = solver.list_methods()
    for method in methods:
        print(f"   - {method}")
    
    # 3. Exemplo: Resolver equação de Poisson
    print("\n3. Resolvendo equação de Poisson com método de Galerkin:")
    
    try:
        # Obter informações do problema
        info = solver.get_problem_info("poisson")
        print(f"   Problema: {info['nome']}")
        print(f"   Equação: {info['equation']}")
        print(f"   Domínio: {info['domain']}")
        
        # Resolver com método de Galerkin
        result = solver.solve("poisson", "galerkin", n_terms=5)
        print(f"   Método usado: {result['method']}")
        print(f"   Solução obtida: {result['solution']}")
        
    except Exception as e:
        print(f"   Erro: {e}")
    
    # 4. Exemplo: Comparar métodos para Poisson
    print("\n4. Comparando métodos para equação de Poisson:")
    
    try:
        comparison = solver.compare_methods(
            "poisson", 
            ["galerkin", "rayleigh_ritz", "least_squares"],
            n_terms=3
        )
        
        for method, result in comparison.items():
            if "error" in result:
                print(f"   {method}: ERRO - {result['error']}")
            else:
                print(f"   {method}: Sucesso")
                
    except Exception as e:
        print(f"   Erro na comparação: {e}")
    
    # 5. Recomendações de métodos
    print("\n5. Recomendações de métodos por problema:")
    for problem_name in problems.keys():
        recommendations = solver.recommend_method(problem_name)
        print(f"   {problem_name}: {recommendations}")

def example_custom_problem():
    """
    Exemplo de como resolver um problema específico passo a passo
    """
    print("\n=== Exemplo Detalhado: Equação de Poisson ===")
    
    solver = EDPSolver()
    
    # Definir problema personalizado
    problem_name = "poisson"
    method_name = "galerkin"
    
    # Resolver
    result = solver.solve(problem_name, method_name, n_terms=4)
    
    # Plotar resultado (se possível)
    try:
        plot_solution(result)
    except Exception as e:
        print(f"Erro no plot: {e}")

def plot_solution(result):
    """
    Plota a solução obtida
    """
    # Esta função precisaria ser adaptada baseada no formato da solução
    # retornada pelos métodos numéricos
    print("Plot da solução seria implementado aqui")
    print(f"Domínio: {result['domain']}")
    print(f"Método: {result['method']}")

if __name__ == "__main__":
    main()
    example_custom_problem()
