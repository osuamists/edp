"""
Visualizador de resultados para análise de EDPs
"""

import numpy as np
import matplotlib.pyplot as plt

class ResultVisualizer:
    """Visualizador de resultados das EDPs"""
    
    def __init__(self):
        # Configurar estilo dos gráficos
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 12
    
    def plot_convergence(self, problem_name, n_values, errors, save_path=None):
        """Plota análise de convergência"""
        plt.figure(figsize=(10, 6))
        
        plt.loglog(n_values, errors, 'bo-', linewidth=2, markersize=8, label='Erro L2')
        
        # Linha de referência para convergência quadrática
        if len(n_values) > 1:
            slope = -2  # Convergência esperada
            ref_line = errors[0] * (np.array(n_values) / n_values[0]) ** slope
            plt.loglog(n_values, ref_line, 'r--', alpha=0.7, label='Referência O(h²)')
        
        plt.xlabel('Número de termos/elementos (N)')
        plt.ylabel('Erro L2')
        plt.title(f'Análise de Convergência - {problem_name.replace("_", " ").title()}')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  Gráfico de convergência salvo: {save_path}")
        
        plt.close()
    
    def plot_solution(self, problem_name, problem_config, solution_data, n, save_path=None):
        """Plota solução da EDP"""
        plt.figure(figsize=(12, 8))
        
        domain = problem_config['domain']
        tipo = problem_config['tipo']
        
        if tipo in ['eliptica_1d', 'parabolica_1d', 'hiperbolica_1d']:
            self._plot_1d_solution(problem_config, solution_data, n)
        elif tipo == 'eliptica_2d':
            self._plot_2d_solution(problem_config, solution_data, n)
        
        plt.title(f'{problem_config["nome"]} - Solução (N={n})')
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  Gráfico de solução salvo: {save_path}")
        
        plt.close()
    
    def _plot_1d_solution(self, problem_config, solution_data, n):
        """Plota solução 1D"""
        domain = problem_config['domain']
        x_vals = np.linspace(domain[0], domain[1], 200)
        
        # Solução numérica
        if problem_config['tipo'] == 'eliptica_1d':
            u_num = self._evaluate_solution_1d(solution_data, x_vals)
            plt.plot(x_vals, u_num, 'b-', linewidth=2, label='Solução Galerkin')
            
            # Solução analítica se disponível
            if 'analytical' in problem_config and problem_config['analytical']:
                u_exact = problem_config['analytical'](x_vals)
                plt.plot(x_vals, u_exact, 'r--', linewidth=2, label='Solução Analítica')
                
                # Calcular erro
                error = np.sqrt(np.trapz((u_num - u_exact)**2, x_vals))
                plt.text(0.02, 0.98, f'Erro L2: {error:.2e}', 
                        transform=plt.gca().transAxes, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        else:
            # Para EDPs temporais, plotar em tempo final
            t_final = 0.1 if problem_config['tipo'] == 'parabolica_1d' else 0.5
            u_num = self._evaluate_temporal_solution(solution_data, x_vals, t_final, problem_config['tipo'])
            plt.plot(x_vals, u_num, 'b-', linewidth=2, label=f'Solução (t={t_final})')
        
        plt.xlabel('x')
        plt.ylabel('u(x)')
        plt.grid(True, alpha=0.3)
        plt.legend()
    
    def _plot_2d_solution(self, problem_config, solution_data, n):
        """Plota solução 2D"""
        domain = problem_config['domain']
        x_vals = np.linspace(domain[0][0], domain[0][1], 50)
        y_vals = np.linspace(domain[1][0], domain[1][1], 50)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        # Avaliar solução na grade
        Z = self._evaluate_solution_2d(solution_data, X, Y)
        
        # Plotar contorno
        contour = plt.contourf(X, Y, Z, levels=20, cmap='viridis')
        plt.colorbar(contour)
        plt.xlabel('x')
        plt.ylabel('y')
    
    def _evaluate_solution_1d(self, coefficients, x_vals):
        """Avalia solução 1D usando funções de base trigonométricas"""
        n = len(coefficients)
        u = np.zeros_like(x_vals)
        
        for i in range(n):
            # Funções de base: sin(π(i+1)x) para x ∈ [0,1]
            u += coefficients[i] * np.sin(np.pi * (i + 1) * x_vals)
        
        return u
    
    def _evaluate_temporal_solution(self, coefficients, x_vals, t, eq_type):
        """Avalia solução temporal"""
        n = len(coefficients)
        u = np.zeros_like(x_vals)
        
        for i in range(n):
            k = np.pi * (i + 1)
            if eq_type == 'parabolica_1d':
                # Equação do calor: decay exponencial
                time_factor = np.exp(-k**2 * t)
            else:  # hiperbolica_1d
                # Equação da onda: oscilação
                time_factor = np.cos(k * t)
            
            u += coefficients[i] * time_factor * np.sin(k * x_vals)
        
        return u
    
    def _evaluate_solution_2d(self, coefficients, X, Y):
        """Avalia solução 2D"""
        # Para simplificar, usar base produto tensorial
        nx, ny = X.shape
        Z = np.zeros_like(X)
        
        n = int(np.sqrt(len(coefficients)))
        idx = 0
        
        for i in range(n):
            for j in range(n):
                if idx < len(coefficients):
                    basis = (np.sin(np.pi * (i + 1) * X) * 
                            np.sin(np.pi * (j + 1) * Y))
                    Z += coefficients[idx] * basis
                    idx += 1
        
        return Z
