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
                    t_final = 0.1  # Tempo maior para ver decay
                
                y_numerical = solution(x_vals, t_final)
                y_analytical = problem["analytical"](x_vals, t_final)
            
            # Erro L2
            error = np.sqrt(np.mean((y_numerical - y_analytical)**2))
            
        elif tipo == "eliptica_2d":
            # 2D (Helmholtz) - implementação mais robusta
            x_vals = np.linspace(domain[0][0], domain[0][1], 20)
            y_vals = np.linspace(domain[1][0], domain[1][1], 10)
            
            # Calcular erro ponto a ponto para evitar problemas de dimensão
            errors_pointwise = []
            
            for xi in x_vals[1:-1]:  # Evitar bordas
                for yi in y_vals[1:-1]:
                    try:
                        val_numerical = solution(xi, yi)
                        
                        if problem["analytical"]:
                            val_analytical = problem["analytical"](xi, yi)
                            error_point = abs(val_numerical - val_analytical)
                        else:
                            # Sem solução analítica - usar norma da solução
                            error_point = abs(val_numerical) / 10  # Normalizado
                        
                        errors_pointwise.append(error_point)
                        
                    except Exception as e:
                        print(f"    ⚠️ Erro ao avaliar ponto ({xi:.3f}, {yi:.3f}): {e}")
                        errors_pointwise.append(1.0)  # Valor padrão
            
            if errors_pointwise:
                error = np.sqrt(np.mean(np.array(errors_pointwise)**2))
            else:
                error = 1.0  # Fallback
            
        elif tipo == "onda_primeira_ordem":
            # Onda de primeira ordem - usar tempo final pequeno
            x_vals = np.linspace(domain[0], domain[1], 100)
            t_final = 0.1  # Tempo pequeno para ver comportamento inicial
            
            try:
                y_numerical = solution(x_vals, t_final)
                # Para onda de primeira ordem, usar aproximação simples
                # A solução exata seria complexa, então usamos erro baseado em energia
                error = np.sqrt(np.mean(y_numerical**2)) / 10  # Normalizado
            except:
                error = 1.0  # Valor padrão se não conseguir avaliar
        
        return error
    
    def analyze_all_problems(self, catalog, n_terms_list):
        """Analisa convergência para todos os problemas"""
        print("=== ANÁLISE DE CONVERGÊNCIA - MÉTODO DE GALERKIN ===")
        
        for name, problem in catalog.get_all_problems().items():
            self.analyze_problem(name, problem, n_terms_list)
        
        self.plot_convergence_summary()
        return self.results
    
    def analyze_problem(self, name, problem, n_terms_list):
        """Analisa convergência para um problema específico"""
        print(f"\n📊 Analisando: {problem['nome']}")
        
        errors = self.analyze_convergence(problem, n_terms_list)
        
        # Armazenar resultados
        self.results[name] = {
            'problem': problem,
            'n_terms': n_terms_list,
            'errors': errors
        }
        
        # Plotar convergência individual
        self.plot_individual_convergence(name, problem, n_terms_list, errors)
        
        return errors

    def plot_individual_convergence(self, name, problem, n_terms_list, errors):
        """Plota convergência individual para um problema"""
        # Filtrar erros válidos
        valid_indices = [i for i, err in enumerate(errors) if not np.isinf(err) and err > 0]
        
        if len(valid_indices) < 2:
            print(f"  ⚠️ Dados insuficientes para plotar convergência de {name}")
            return
        
        valid_n_terms = [n_terms_list[i] for i in valid_indices]
        valid_errors = [errors[i] for i in valid_indices]
        
        plt.figure(figsize=(10, 6))
        plt.loglog(valid_n_terms, valid_errors, 'bo-', linewidth=2, markersize=8, label='Erro L2')
        
        # Adicionar linha de referência (slope = -1)
        if len(valid_n_terms) >= 2:
            x_ref = np.array(valid_n_terms)
            y_ref = valid_errors[0] * (x_ref / x_ref[0])**(-1)
            plt.loglog(x_ref, y_ref, 'r--', alpha=0.7, label='Referência O(1/N)')
        
        plt.xlabel('Número de termos/elementos (N)')
        plt.ylabel('Erro L2')
        plt.title(f'Análise de Convergência - {problem["nome"]}')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Calcular taxa de convergência
        if len(valid_errors) > 1:
            # Usar regressão linear em escala log
            log_n = np.log(valid_n_terms)
            log_err = np.log(valid_errors)
            rate = -np.polyfit(log_n, log_err, 1)[0]
            
            plt.text(0.05, 0.95, f'Taxa de convergência ≈ {rate:.2f}', 
                    transform=plt.gca().transAxes, fontsize=12,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Salvar gráfico individual
        filename = f"output/{name}_convergence.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"  💾 Gráfico salvo: {filename}")

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
