"""
EDP Solver - Script Principal
Executa análise de convergência e visualização para as 4 EDPs.
"""

import os
from core import EDPCatalog, GalerkinSolver, ConvergenceAnalyzer
from visualizer import ResultVisualizer

def main():
    """Executa análise completa das 4 EDPs com método de Galerkin."""
    
    # Criar diretório de saída se não existir
    os.makedirs('output', exist_ok=True)
    
    # Obter catálogo das EDPs
    catalog = EDPCatalog()
    
    # Inicializar solver e analisador
    solver = GalerkinSolver()
    analyzer = ConvergenceAnalyzer(solver)
    visualizer = ResultVisualizer()
    
    # Lista de problemas a serem analisados
    problem_names = ['poisson_1d', 'heat_1d', 'wave_1d', 'helmholtz_2d']
    
    print("=== EDP Solver - Análise de Convergência ===\n")
    
    for problem_name in problem_names:
        print(f"Analisando {problem_name}...")
        
        # Obter configuração do problema
        problem = catalog.get_problem(problem_name)
        
        # Executar análise de convergência
        if problem_name == 'helmholtz_2d':
            # Para 2D, usar menos pontos para não demorar muito
            n_values = [5, 10, 15, 20]
        else:
            # Para 1D, usar mais pontos
            n_values = [10, 20, 30, 40, 50]
        
        errors = analyzer.analyze_convergence(problem, n_values)
        
        # Gerar visualizações
        visualizer.plot_convergence(problem_name, n_values, errors, 
                                  save_path=f'output/{problem_name}_convergence.png')
        
        print(f"  ✓ Análise completa salva em output/{problem_name}_convergence.png\n")
    
    print("=== Análise Concluída ===")
    print("Verifique os gráficos gerados no diretório 'output/'")

if __name__ == '__main__':
    main()
