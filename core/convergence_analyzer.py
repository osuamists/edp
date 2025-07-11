# core/convergence_analyzer.py

import numpy as np
import matplotlib.pyplot as plt

class ConvergenceAnalyzer:
    """Analisador de convergência para método de Galerkin"""
    
    def __init__(self, solver):
        self.solver = solver
        self.results = {}
    
    def analyze_convergence(self, problem, n_terms_list):
        """Analisa convergência para um problema específico"""
        errors = []
        solutions = []
        
        print(f"  Analisando convergência para {problem['nome']}...")
        
        for n_terms in n_terms_list:
            print(f"    Resolvendo com {n_terms} termos...")
            
            try:
                # Resolver com Galerkin
                solution = self.solver.solve(problem, n_terms)
                solutions.append(solution)
                
                # Calcular erro se solução analítica disponível
                error = self._calculate_error(solution, problem)
                errors.append(error)
                
                print(f"    Erro L2: {error:.2e}")
                
            except Exception as e:
                print(f"    Erro ao resolver com {n_terms} termos: {e}")
                errors.append(np.inf)
                solutions.append(None)
        
        
        return errors
    
    def _calculate_error(self, solution, problem):
        """Calcula erro L2 entre solução numérica e analítica"""
        if not problem["analytical"]:
            return 0.0
        
        domain = problem["domain"]
        tipo = problem["tipo"]
        
        if tipo in ["eliptica_1d", "parabolica_1d", "hiperbolica_1d"]:
            # 1D
            x_vals = np.linspace(domain[0], domain[1], 200)
            
            if tipo == "eliptica_1d":
                y_numerical = solution(x_vals)
                y_analytical = problem["analytical"](x_vals)
            else:
                # Para problemas temporais, usar tempo final
                t_final = problem.get("time_domain", (0, 1))[1]
                if tipo == "parabolica_1d":
                    t_final = 0.05  # Tempo menor para equação do calor
                
                y_numerical = solution(x_vals, t_final)
                y_analytical = problem["analytical"](x_vals, t_final)
            
            # Erro L2
            error = np.sqrt(np.mean((y_numerical - y_analytical)**2))
            
        elif tipo == "eliptica_2d":
            # 2D (simplificado)
            x_vals = np.linspace(domain[0][0], domain[0][1], 50)
            y_vals = np.linspace(domain[1][0], domain[1][1], 50)
            X, Y = np.meshgrid(x_vals, y_vals)
            
            Z_numerical = solution(x_vals, y_vals)
            Z_analytical = problem["analytical"](X, Y)
            
            error = np.sqrt(np.mean((Z_numerical - Z_analytical)**2))
        
        return error
    
    def analyze_all_problems(self, catalog, n_terms_list):
        """Analisa convergência para todos os problemas"""
        print("=== ANÁLISE DE CONVERGÊNCIA - MÉTODO DE GALERKIN ===")
        
        for name, problem in catalog.get_all_problems().items():
            self.analyze_problem(name, problem, n_terms_list)
        
        self.plot_convergence_summary()
        return self.results
    
    def plot_convergence_summary(self):
        """Plota resumo da convergência para todos os problemas"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        for i, (name, result) in enumerate(self.results.items()):
            ax = axes[i]
            
            n_terms = result['n_terms']
            errors = result['errors']
            problem = result['problem']
            
            # Filtrar erros infinitos
            valid_indices = [j for j, err in enumerate(errors) if not np.isinf(err)]
            valid_n_terms = [n_terms[j] for j in valid_indices]
            valid_errors = [errors[j] for j in valid_indices]
            
            if valid_errors:
                ax.loglog(valid_n_terms, valid_errors, 'bo-', linewidth=2, markersize=8)
                ax.set_xlabel('Número de Termos')
                ax.set_ylabel('Erro L2')
                ax.set_title(f'Convergência - {problem["nome"]}')
                ax.grid(True, alpha=0.3)
                
                # Adicionar taxa de convergência
                if len(valid_errors) > 1:
                    rate = -np.polyfit(np.log(valid_n_terms), np.log(valid_errors), 1)[0]
                    ax.text(0.05, 0.95, f'Taxa ≈ {rate:.2f}', 
                           transform=ax.transAxes, fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='wheat'))
            else:
                ax.text(0.5, 0.5, 'Sem dados válidos', 
                       ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f'{problem["nome"]} - Erro na análise')
        
        plt.tight_layout()
        plt.suptitle('Análise de Convergência - Método de Galerkin', 
                     fontsize=16, y=1.02)
        
        # Salvar gráfico
        plt.savefig('output/convergence_analysis.png', dpi=150, bbox_inches='tight')
        plt.show()
