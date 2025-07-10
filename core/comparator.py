import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from .methods.galerkin_method import GalerkinMethod
from .methods.rayleigh_ritz_method import RayleighRitzMethod
# Métodos especializados para os problemas do trabalho
from .methods.wave_method import WaveGalerkinMethod
from .methods.heat_method import HeatGalerkinMethod
from .methods.helmholtz_2d_method import Helmholtz2DMethod
from .problems import EDPCatalog

class EDPComparator:
    """
    Classe para comparar métodos numéricos resolvendo múltiplas EDPs
    do catálogo e analisando convergência.
    """
    
    def __init__(self):
        self.x = sp.Symbol('x')
        self.catalog = EDPCatalog()
        self.methods = {
            'Galerkin': GalerkinMethod,
            'Rayleigh-Ritz': RayleighRitzMethod
        }
        # Métodos especializados para problemas específicos
        self.specialized_methods = {
            'poisson_trabalho': {
                'Galerkin': GalerkinMethod,
                'Rayleigh-Ritz': RayleighRitzMethod
            },
            'onda_trabalho': {
                'Wave-Galerkin': WaveGalerkinMethod
            },
            'calor_trabalho': {
                'Heat-Galerkin': HeatGalerkinMethod
            },
            'helmholtz_trabalho': {
                'Helmholtz-2D': Helmholtz2DMethod
            }
        }
    
    def get_available_problems(self):
        """
        Retorna os problemas disponíveis no catálogo.
        """
        return {key: value["nome"] for key, value in self.catalog.problems.items()}
    
    def get_problem_details(self, problem_name):
        """
        Retorna detalhes de um problema específico.
        """
        if problem_name not in self.catalog.problems:
            raise ValueError(f"Problema {problem_name} não encontrado")
        
        return self.catalog.problems[problem_name]
    
    def solve_equation(self, problem_name, method_name, n_terms):
        """
        Resolve um problema específico com um método específico.
        """
        if problem_name not in self.catalog.problems:
            raise ValueError(f"Problema {problem_name} não encontrado")
        
        problem_data = self.catalog.problems[problem_name]
        
        # Verificar se há método especializado para este problema
        if problem_name in self.specialized_methods:
            if method_name in self.specialized_methods[problem_name]:
                return self._solve_with_specialized_method(problem_name, method_name, n_terms)
            else:
                available_methods = list(self.specialized_methods[problem_name].keys())
                raise ValueError(f"Para o problema {problem_name}, métodos disponíveis: {available_methods}")
        
        # Usar métodos tradicionais para problemas elípticos (Poisson)
        if method_name not in self.methods:
            raise ValueError(f"Método {method_name} não encontrado")
        
        method_class = self.methods[method_name]
        
        # Verificar se o problema é adequado para os métodos disponíveis
        if problem_data.get('tipo') not in ['eliptica', None]:
            raise ValueError(f"Problema {problem_name} é do tipo '{problem_data.get('tipo')}' - métodos atuais só suportam problemas elípticos 1D")
        
        # Adaptar as condições de contorno para o formato esperado pelos métodos
        bc = problem_data['boundary_conditions']
        boundary_conditions = []
        for condition in bc:
            if condition[0] == "dirichlet" and isinstance(condition[1], (int, float)):
                boundary_conditions.append((condition[1], condition[2]))
        
        # Para problema de Poisson, usar diretamente o termo fonte
        if problem_name == "poisson_trabalho":
            # Para ∂²Ω/∂x² = Q(x), onde Q(x) = -1
            # Convertemos para -u'' = -Q(x) = -(-1) = 1
            equation_for_method = sp.Integer(1)
        else:
            equation_for_method = problem_data['equation']
        
        # Criar instância do método
        method = method_class(
            equation_for_method,
            problem_data['domain'],
            boundary_conditions
        )
        
        # Resolver
        solution = method.solve(n_terms=n_terms)
        return solution
    
    def _solve_with_specialized_method(self, problem_name, method_name, n_terms):
        """
        Resolve problema usando método especializado
        """
        problem_data = self.catalog.problems[problem_name]
        method_class = self.specialized_methods[problem_name][method_name]
        
        if problem_name == 'onda_trabalho':
            # Equação da onda: ∂u/∂t = λ²∂²u/∂x²
            lambda_param = problem_data.get('lambda', 4)
            method = method_class(
                equation=problem_data['equation'],
                domain=problem_data['domain'],
                lambda_param=lambda_param
            )
            return method.solve(n_terms=n_terms)
            
        elif problem_name == 'calor_trabalho':
            # Equação do calor: ∂u/∂t = ∂²u/∂x²
            method = method_class(
                equation=problem_data['equation'],
                domain=problem_data['domain']
            )
            return method.solve(n_terms=n_terms)
            
        elif problem_name == 'helmholtz_trabalho':
            # Equação de Helmholtz: ∂²φ/∂x² + ∂²φ/∂y² + λφ = 0
            method = method_class(
                equation=problem_data['equation'],
                domain=problem_data['domain'],
                lambda_param=1,  # Parâmetro λ padrão
                gamma=1  # Parâmetro γ padrão
            )
            return method.solve(n_terms_x=n_terms, n_terms_y=n_terms)
        
        return None
    
    def calculate_error(self, problem_name, method_name, n_terms, n_points=200):
        """
        Calcula o erro entre a solução numérica e a exata.
        """
        problem_data = self.catalog.problems[problem_name]
        
        # Obter solução numérica
        numerical_solution = self.solve_equation(problem_name, method_name, n_terms)
        exact_solution = problem_data['analytical']
        
        # Avaliar em pontos do domínio
        domain = problem_data['domain']
        x_vals = np.linspace(domain[0], domain[1], n_points)
        
        # Converter para funções numéricas
        num_func = sp.lambdify(self.x, numerical_solution, modules=['numpy'])
        exact_func = sp.lambdify(self.x, exact_solution, modules=['numpy'])
        
        y_num = num_func(x_vals)
        y_exact = exact_func(x_vals)
        
        # Calcular erro máximo e erro RMS
        max_error = np.max(np.abs(y_num - y_exact))
        rms_error = np.sqrt(np.mean((y_num - y_exact)**2))
        
        return max_error, rms_error, x_vals, y_num, y_exact
    
    def convergence_analysis(self, problem_name, method_name, n_terms_list=[2, 3, 4, 5, 6, 7, 8]):
        """
        Analisa convergência variando o número de termos.
        """
        max_errors = []
        rms_errors = []
        
        for n_terms in n_terms_list:
            try:
                max_err, rms_err, _, _, _ = self.calculate_error(problem_name, method_name, n_terms)
                max_errors.append(max_err)
                rms_errors.append(rms_err)
            except Exception as e:
                print(f"Erro ao calcular com {n_terms} termos: {e}")
                max_errors.append(np.nan)
                rms_errors.append(np.nan)
        
        return n_terms_list, max_errors, rms_errors
    
    def plot_solutions(self, problem_name, method_name, n_terms=5, save_path=None):
        """
        Plota a comparação entre solução numérica e exata.
        """
        problem_data = self.catalog.problems[problem_name]
        max_error, rms_error, x_vals, y_num, y_exact = self.calculate_error(
            problem_name, method_name, n_terms
        )
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_exact, 'k-', linewidth=3, label='Solução Exata', zorder=10)
        plt.plot(x_vals, y_num, 'r--', linewidth=2, alpha=0.8, 
                label=f'{method_name} (n={n_terms})')
        
        plt.title(f'{problem_data["nome"]}')
        plt.xlabel('x')
        plt.ylabel('u(x)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Adicionar informações de erro
        plt.text(0.02, 0.98, f'Erro máx: {max_error:.2e}\nErro RMS: {rms_error:.2e}',
                transform=plt.gca().transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        return plt.gcf()
    
    def plot_convergence(self, problem_name, method_name, save_path=None):
        """
        Plota gráfico de convergência.
        """
        n_terms_list, max_errors, rms_errors = self.convergence_analysis(problem_name, method_name)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Erro máximo
        ax1.semilogy(n_terms_list, max_errors, 'bo-', linewidth=2, markersize=6)
        ax1.set_xlabel('Número de Termos')
        ax1.set_ylabel('Erro Máximo')
        ax1.set_title(f'Convergência - Erro Máximo\n{problem_name} - {method_name}')
        ax1.grid(True, alpha=0.3)
        
        # Erro RMS
        ax2.semilogy(n_terms_list, rms_errors, 'ro-', linewidth=2, markersize=6)
        ax2.set_xlabel('Número de Termos')
        ax2.set_ylabel('Erro RMS')
        ax2.set_title(f'Convergência - Erro RMS\n{problem_name} - {method_name}')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        return fig
    
    def compare_all_problems(self, method_name='Galerkin', n_terms=5):
        """
        Compara os problemas que podem ser resolvidos pelos métodos disponíveis.
        """
        # Por enquanto, apenas o problema de Poisson pode ser resolvido
        solvable_problems = ['poisson_trabalho']
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        for problem_name in solvable_problems:
            problem_data = self.catalog.problems[problem_name]
            max_error, rms_error, x_vals, y_num, y_exact = self.calculate_error(
                problem_name, method_name, n_terms
            )
            
            ax.plot(x_vals, y_exact, 'k-', linewidth=3, label='Solução Exata')
            ax.plot(x_vals, y_num, 'r--', linewidth=2, alpha=0.8, 
                   label=f'{method_name} (n={n_terms})')
            
            ax.set_title(f'{problem_data["nome"]}')
            ax.set_xlabel('x')
            ax.set_ylabel('u(x)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Adicionar erro
            ax.text(0.02, 0.98, f'Erro máx: {max_error:.2e}\nErro RMS: {rms_error:.2e}',
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.suptitle(f'Equação de Poisson - Método {method_name} (n={n_terms})', fontsize=14)
        plt.tight_layout()
        
        return fig
    
    def get_problem_analysis(self):
        """
        Retorna análise dos 4 problemas do trabalho.
        """
        analysis = {}
        
        problems = self.catalog.problems
        
        for name, data in problems.items():
            analysis[name] = {
                'nome': data['nome'],
                'description': data['description'],
                'tipo': data.get('tipo', 'indefinido'),
                'solucionavel': name == 'poisson_trabalho'  # Apenas Poisson por enquanto
            }
        
        return analysis
    
    def full_analysis_report(self, method_name='Galerkin'):
        """
        Gera um relatório completo de análise para os problemas do trabalho.
        """
        print(f"\n{'='*70}")
        print(f"RELATÓRIO DE ANÁLISE - PROBLEMAS DO TRABALHO")
        print(f"MÉTODO: {method_name.upper()}")
        print(f"{'='*70}")
        
        analysis = self.get_problem_analysis()
        
        print(f"\nPROBLEMAS IDENTIFICADOS:")
        print("-" * 50)
        
        for name, info in analysis.items():
            print(f"\n{info['nome']}")
            print(f"  Descrição: {info['description']}")
            print(f"  Tipo: {info['tipo']}")
            print(f"  Solucionável com métodos atuais: {'SIM' if info['solucionavel'] else 'NÃO'}")
            
            if info['solucionavel']:
                # Análise de convergência apenas para problemas solucionáveis
                try:
                    n_terms_list, max_errors, rms_errors = self.convergence_analysis(name, method_name)
                    
                    print("  Convergência (Número de termos -> Erro máximo):")
                    for n, max_err in zip(n_terms_list[-4:], max_errors[-4:]):  # Últimos 4 valores
                        if not np.isnan(max_err):
                            print(f"    n={n}: {max_err:.6e}")
                    
                    # Taxa de convergência
                    valid_errors = [err for err in max_errors if not np.isnan(err)]
                    if len(valid_errors) >= 2:
                        ratio = valid_errors[-2] / valid_errors[-1] if valid_errors[-1] > 0 else 0
                        print(f"  Taxa de melhoria: {ratio:.2f}x")
                        
                except Exception as e:
                    print(f"  Erro na análise: {e}")
            else:
                print("  → Requer implementação de métodos específicos para EDPs dependentes do tempo/2D")
        
        print(f"\n{'='*70}")
        print("OBSERVAÇÕES:")
        print("- Métodos atuais (Galerkin/Rayleigh-Ritz) são adequados para problemas elípticos 1D")
        print("- Problemas 2, 3 e 4 requerem métodos específicos para:")
        print("  * Equações hiperbólicas (Onda)")
        print("  * Equações parabólicas (Calor)")  
        print("  * Equações elípticas 2D (Helmholtz)")
        print(f"{'='*70}")
    
    def analyze_all_trabalho_problems(self, n_terms=5, save_plots=True, plot_dir="plots"):
        """
        Analisa todos os quatro problemas do trabalho
        """
        import os
        if save_plots and not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
        
        problems = ['poisson_trabalho', 'onda_trabalho', 'calor_trabalho', 'helmholtz_trabalho']
        results = {}
        
        print("=== ANÁLISE COMPLETA DOS PROBLEMAS DO TRABALHO ===\n")
        
        for problem_name in problems:
            problem_data = self.catalog.get_problem(problem_name)
            print(f"🔍 {problem_data['nome']}")
            print(f"   Equação: {problem_data['description']}")
            print(f"   Tipo: {problem_data['tipo']}")
            print(f"   Domínio: {problem_data['domain']}")
            
            try:
                if problem_name == 'poisson_trabalho':
                    # Problema elíptico - usar métodos tradicionais
                    results[problem_name] = self._analyze_poisson_problem(problem_name, n_terms, save_plots, plot_dir)
                elif problem_name == 'onda_trabalho':
                    # Problema hiperbólico - usar método especializado
                    results[problem_name] = self._analyze_wave_problem(problem_name, n_terms, save_plots, plot_dir)
                elif problem_name == 'calor_trabalho':
                    # Problema parabólico - usar método especializado
                    results[problem_name] = self._analyze_heat_problem(problem_name, n_terms, save_plots, plot_dir)
                elif problem_name == 'helmholtz_trabalho':
                    # Problema elíptico 2D - usar método especializado
                    results[problem_name] = self._analyze_helmholtz_problem(problem_name, n_terms, save_plots, plot_dir)
                
                print(f"   ✅ Resolvido com sucesso!")
                
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                results[problem_name] = {'status': 'error', 'message': str(e)}
            
            print()
        
        return results
    
    def _analyze_poisson_problem(self, problem_name, n_terms, save_plots, plot_dir):
        """
        Análise específica para o problema de Poisson
        """
        # Comparar métodos Galerkin e Rayleigh-Ritz
        methods = ['Galerkin', 'Rayleigh-Ritz']
        results = {'solutions': {}, 'convergence': {}, 'plots': []}
        
        for method in methods:
            solution = self.solve_equation(problem_name, method, n_terms)
            max_error, rms_error, x_vals, y_num, y_exact = self.calculate_error(
                problem_name, method, n_terms
            )
            
            results['solutions'][method] = {
                'solution': solution,
                'max_error': max_error,
                'rms_error': rms_error
            }
            
            # Análise de convergência
            n_list, max_errs, rms_errs = self.convergence_analysis(problem_name, method)
            results['convergence'][method] = {
                'n_terms': n_list,
                'max_errors': max_errs,
                'rms_errors': rms_errs
            }
        
        if save_plots:
            # Plot comparação de soluções
            plt.figure(figsize=(12, 8))
            
            # Subplot 1: Soluções
            plt.subplot(2, 2, 1)
            problem_data = self.catalog.get_problem(problem_name)
            _, _, x_vals, _, y_exact = self.calculate_error(problem_name, 'Galerkin', n_terms)
            
            plt.plot(x_vals, y_exact, 'k-', linewidth=3, label='Exata')
            
            for method in methods:
                _, _, _, y_num, _ = self.calculate_error(problem_name, method, n_terms)
                plt.plot(x_vals, y_num, '--', linewidth=2, label=f'{method}')
            
            plt.title('Comparação de Soluções')
            plt.xlabel('x')
            plt.ylabel('u(x)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Subplot 2: Convergência (erro máximo)
            plt.subplot(2, 2, 2)
            for method in methods:
                conv_data = results['convergence'][method]
                plt.semilogy(conv_data['n_terms'], conv_data['max_errors'], 'o-', label=method)
            
            plt.title('Convergência - Erro Máximo')
            plt.xlabel('Número de Termos')
            plt.ylabel('Erro Máximo')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Subplot 3: Convergência (erro RMS)
            plt.subplot(2, 2, 3)
            for method in methods:
                conv_data = results['convergence'][method]
                plt.semilogy(conv_data['n_terms'], conv_data['rms_errors'], 's-', label=method)
            
            plt.title('Convergência - Erro RMS')
            plt.xlabel('Número de Termos')
            plt.ylabel('Erro RMS')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Subplot 4: Erro absoluto
            plt.subplot(2, 2, 4)
            _, _, x_vals, y_gal, y_exact = self.calculate_error(problem_name, 'Galerkin', n_terms)
            _, _, _, y_rr, _ = self.calculate_error(problem_name, 'Rayleigh-Ritz', n_terms)
            
            plt.plot(x_vals, np.abs(y_gal - y_exact), '-', label='Erro Galerkin')
            plt.plot(x_vals, np.abs(y_rr - y_exact), '-', label='Erro Rayleigh-Ritz')
            plt.title('Distribuição do Erro')
            plt.xlabel('x')
            plt.ylabel('|Erro|')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plot_path = f"{plot_dir}/poisson_analysis.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            results['plots'].append(plot_path)
        
        return results
    
    def _analyze_wave_problem(self, problem_name, n_terms, save_plots, plot_dir):
        """
        Análise específica para o problema da onda
        """
        results = {'solutions': {}, 'temporal_analysis': {}, 'plots': []}
        
        # Resolver usando método especializado
        solution = self.solve_equation(problem_name, 'Wave-Galerkin', n_terms)
        results['solutions']['Wave-Galerkin'] = {'solution': solution}
        
        # Análise temporal usando método direto
        from .methods.wave_method import WaveGalerkinMethod
        
        problem_data = self.catalog.get_problem(problem_name)
        lambda_param = problem_data.get('lambda', 4)
        
        method = WaveGalerkinMethod(
            equation=problem_data['equation'],
            domain=problem_data['domain'],
            lambda_param=lambda_param
        )
        
        method.solve(n_terms)
        
        # Soluções em diferentes tempos
        time_values = [0, 0.01, 0.02, 0.05, 0.1]
        temporal_solutions = {}
        
        for t_val in time_values:
            sol_at_t = method.evaluate_at_time(t_val, n_terms)
            temporal_solutions[t_val] = sol_at_t
        
        results['temporal_analysis'] = temporal_solutions
        
        if save_plots:
            plt.figure(figsize=(12, 8))
            
            # Plot soluções em diferentes tempos
            x_vals = np.linspace(0.01, 0.99, 100)  # Evitar bordas
            
            for i, (t_val, solution) in enumerate(temporal_solutions.items()):
                plt.subplot(2, 3, i+1)
                
                # Converter solução para valores numéricos
                x_sym = sp.Symbol('x')
                y_vals = []
                for x_val in x_vals:
                    try:
                        val = float(solution.subs(x_sym, x_val))
                        y_vals.append(val)
                    except:
                        y_vals.append(0)
                
                plt.plot(x_vals, y_vals, 'b-', linewidth=2)
                plt.title(f't = {t_val:.2f}')
                plt.xlabel('x')
                plt.ylabel('u(x,t)')
                plt.grid(True, alpha=0.3)
                plt.ylim(-1.5, 1.5)
            
            # Último subplot: evolução no tempo em pontos específicos
            plt.subplot(2, 3, 6)
            x_points = [0.25, 0.5, 0.75]
            
            for x_point in x_points:
                u_values = []
                for t_val, solution in temporal_solutions.items():
                    x_sym = sp.Symbol('x')
                    try:
                        u_val = float(solution.subs(x_sym, x_point))
                        u_values.append(u_val)
                    except:
                        u_values.append(0)
                
                plt.plot(time_values, u_values, 'o-', label=f'x = {x_point}')
            
            plt.title('Evolução Temporal')
            plt.xlabel('Tempo')
            plt.ylabel('u(x,t)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plot_path = f"{plot_dir}/wave_analysis.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            results['plots'].append(plot_path)
        
        return results
    
    def _analyze_heat_problem(self, problem_name, n_terms, save_plots, plot_dir):
        """
        Análise específica para o problema do calor
        """
        results = {'solutions': {}, 'temporal_analysis': {}, 'plots': []}
        
        # Resolver usando método especializado
        solution = self.solve_equation(problem_name, 'Heat-Galerkin', n_terms)
        results['solutions']['Heat-Galerkin'] = {'solution': solution}
        
        # Análise temporal usando método direto
        from .methods.heat_method import HeatGalerkinMethod
        
        problem_data = self.catalog.get_problem(problem_name)
        
        method = HeatGalerkinMethod(
            equation=problem_data['equation'],
            domain=problem_data['domain']
        )
        
        method.solve(n_terms)
        
        # Soluções em diferentes tempos
        time_values = [0, 0.01, 0.02, 0.05, 0.1]
        temporal_solutions = {}
        
        for t_val in time_values:
            sol_at_t = method.evaluate_at_time(t_val, n_terms)
            temporal_solutions[t_val] = sol_at_t
        
        results['temporal_analysis'] = temporal_solutions
        
        if save_plots:
            plt.figure(figsize=(12, 8))
            
            # Plot soluções em diferentes tempos
            x_vals = np.linspace(0.01, 0.99, 100)  # Evitar bordas
            
            for i, (t_val, solution) in enumerate(temporal_solutions.items()):
                plt.subplot(2, 3, i+1)
                
                # Converter solução para valores numéricos
                x_sym = sp.Symbol('x')
                y_vals = []
                for x_val in x_vals:
                    try:
                        val = float(solution.subs(x_sym, x_val))
                        y_vals.append(val)
                    except:
                        y_vals.append(0)
                
                # Solução analítica para comparação (só no primeiro subplot)
                if i == 0 and t_val == 0:
                    # Condição inicial: sin(3πx/2)
                    y_analytical = np.sin(3 * np.pi * x_vals / 2)
                    plt.plot(x_vals, y_analytical, 'k--', linewidth=1, alpha=0.7, label='Analítica')
                elif t_val > 0:
                    # Solução exata: sin(3πx/2) * exp(-(3π/2)²*t)
                    L = problem_data['domain'][1] - problem_data['domain'][0]
                    y_analytical = np.sin(3 * np.pi * x_vals / (2 * L)) * np.exp(-(3 * np.pi / (2 * L))**2 * t_val)
                    plt.plot(x_vals, y_analytical, 'k--', linewidth=1, alpha=0.7, label='Analítica')
                
                plt.plot(x_vals, y_vals, 'r-', linewidth=2, label='Numérica')
                plt.title(f't = {t_val:.2f}')
                plt.xlabel('x')
                plt.ylabel('u(x,t)')
                plt.grid(True, alpha=0.3)
                if i == 0:
                    plt.legend()
            
            # Último subplot: decaimento temporal
            plt.subplot(2, 3, 6)
            x_point = 0.5  # Ponto central
            
            u_values_numerical = []
            u_values_analytical = []
            
            for t_val, solution in temporal_solutions.items():
                x_sym = sp.Symbol('x')
                try:
                    u_val = float(solution.subs(x_sym, x_point))
                    u_values_numerical.append(abs(u_val))
                except:
                    u_values_numerical.append(0)
                
                # Valor analítico
                if t_val == 0:
                    u_analytical = np.sin(3 * np.pi * x_point / 2)
                else:
                    L = problem_data['domain'][1] - problem_data['domain'][0]
                    u_analytical = np.sin(3 * np.pi * x_point / (2 * L)) * np.exp(-(3 * np.pi / (2 * L))**2 * t_val)
                u_values_analytical.append(abs(u_analytical))
            
            plt.semilogy(time_values, u_values_numerical, 'ro-', label='Numérica')
            plt.semilogy(time_values, u_values_analytical, 'k--', label='Analítica')
            plt.title('Decaimento Temporal')
            plt.xlabel('Tempo')
            plt.ylabel('|u(0.5, t)|')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plot_path = f"{plot_dir}/heat_analysis.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            results['plots'].append(plot_path)
        
        return results
    
    def _analyze_helmholtz_problem(self, problem_name, n_terms, save_plots, plot_dir):
        """
        Análise específica para o problema de Helmholtz
        """
        results = {'solutions': {}, 'eigenvalue_analysis': {}, 'plots': []}
        
        # Resolver usando método especializado
        solution = self.solve_equation(problem_name, 'Helmholtz-2D', n_terms)
        results['solutions']['Helmholtz-2D'] = {'solution': solution}
        
        # Análise de autovalores usando método direto
        from .methods.helmholtz_2d_method import Helmholtz2DMethod
        
        problem_data = self.catalog.get_problem(problem_name)
        
        method = Helmholtz2DMethod(
            equation=problem_data['equation'],
            domain=((0, 1), (0, 1)),
            lambda_param=1,
            gamma=4
        )
        
        method.solve(n_terms_x=n_terms, n_terms_y=n_terms)
        
        # Obter espectro de autovalores
        spectrum = method.get_eigenvalue_spectrum(n_terms_x=n_terms, n_terms_y=n_terms)
        results['eigenvalue_analysis'] = spectrum
        
        if save_plots:
            plt.figure(figsize=(15, 10))
            
            # Plot da primeira solução (modo fundamental)
            plt.subplot(2, 3, 1)
            x_vals = np.linspace(0, 1, 50)
            y_vals = np.linspace(0, 1, 50)
            
            try:
                mode_data = method.evaluate_mode(0, x_vals, y_vals)
                
                X, Y = np.meshgrid(x_vals, y_vals)
                contour = plt.contourf(X, Y, mode_data, levels=20, cmap='viridis')
                plt.colorbar(contour)
                plt.title('Modo Fundamental')
                plt.xlabel('x')
                plt.ylabel('y')
            except:
                plt.text(0.5, 0.5, 'Modo\nFundamental', 
                        ha='center', va='center', transform=plt.gca().transAxes)
                plt.title('Solução 2D')
            
            # Plot espectro de autovalores
            plt.subplot(2, 3, 2)
            eigenvals = spectrum['eigenvalues'][:min(10, len(spectrum['eigenvalues']))]
            mode_labels = [f"({m},{n})" for m, n in spectrum['mode_indices'][:len(eigenvals)]]
            
            plt.bar(range(len(eigenvals)), eigenvals)
            plt.title('Espectro de Autovalores')
            plt.xlabel('Modo')
            plt.ylabel('Eigenvalue')
            plt.xticks(range(len(mode_labels)), mode_labels, rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Plot valores de λ correspondentes
            plt.subplot(2, 3, 3)
            lambda_vals = spectrum['lambda_values'][:len(eigenvals)]
            
            plt.bar(range(len(lambda_vals)), lambda_vals, color='red', alpha=0.7)
            plt.title('Valores de λ')
            plt.xlabel('Modo')
            plt.ylabel('λ')
            plt.xticks(range(len(mode_labels)), mode_labels, rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Plots dos primeiros modos
            for i in range(min(3, len(method.eigenmodes))):
                plt.subplot(2, 3, 4+i)
                try:
                    mode_data = method.evaluate_mode(i, x_vals, y_vals)
                    m, n = spectrum['mode_indices'][i]
                    
                    contour = plt.contourf(X, Y, mode_data, levels=15, cmap='RdBu')
                    plt.title(f'Modo ({m},{n})')
                    plt.xlabel('x')
                    plt.ylabel('y')
                    if i == 0:
                        plt.colorbar(contour)
                except Exception as e:
                    plt.text(0.5, 0.5, f'Modo {i+1}\n(erro)', 
                            ha='center', va='center', transform=plt.gca().transAxes)
                    plt.title(f'Modo {i+1}')
            
            plt.tight_layout()
            plot_path = f"{plot_dir}/helmholtz_analysis.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            results['plots'].append(plot_path)
        
        return results
