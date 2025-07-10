import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class WaveGalerkinMethod(NumericalMethod):
    """
    Implementa o método de Galerkin para resolver a equação da onda 1D
    ∂u/∂t = λ²∂²u/∂x² com condições iniciais e de contorno.
    """
    
    def __init__(self, equation, domain, analytical=None, lambda_param=4):
        # Adaptar para a interface da classe base
        boundary_conditions = []  # Será definido internamente
        super().__init__(equation, domain, boundary_conditions)
        self.lambda_param = lambda_param
        self.time_steps = 100
        self.final_time = 0.1
    
    def generate_basis_functions(self, n_terms):
        """
        Implementa o método abstrato obrigatório.
        Gera funções de base espaciais que satisfazem u(0,t)=0 e u(1,t)=0.
        """
        x = sp.Symbol('x')
        a, b = self.domain
        # Funções senoidais que satisfazem as condições de contorno
        self.basis_functions = [sp.sin(n * sp.pi * x / (b - a)) for n in range(1, n_terms + 1)]
    def solve(self, n_terms=5, precision=1e-6):
        """
        Resolve a equação da onda usando método de Galerkin com separação de variáveis.
        """
        self.generate_basis_functions(n_terms)
        
        x = sp.Symbol('x')
        t = sp.Symbol('t')
        
        # Para a equação da onda ∂u/∂t = λ²∂²u/∂x²
        # Assumimos solução da forma u(x,t) = Σ a_n(t) * φ_n(x)
        
        # Usar as funções de base geradas
        self.spatial_basis = self.basis_functions
        
        # Condição inicial u(x,0) = 1 (constante)
        # Projetamos a condição inicial nas funções de base
        initial_coeffs = []
        
        for i, phi_i in enumerate(self.spatial_basis):
            # Coeficiente inicial: ∫ 1 * φ_i(x) dx / ∫ φ_i²(x) dx
            numerator = sp.integrate(1 * phi_i, (x, self.domain[0], self.domain[1]))
            denominator = sp.integrate(phi_i**2, (x, self.domain[0], self.domain[1]))
            
            if denominator != 0:
                coeff = float(numerator / denominator)
                initial_coeffs.append(coeff)
            else:
                initial_coeffs.append(0)
        
        # Para cada modo, a equação temporal é:
        # da_n/dt = -λ² * (nπ/(b-a))² * a_n
        # Solução: a_n(t) = a_n(0) * exp(-λ² * (nπ/(b-a))² * t)
        
        solution_modes = []
        eigenvalues = []
        
        for n in range(1, n_terms + 1):
            # Autovalor do n-ésimo modo
            eigenval = self.lambda_param * (n * sp.pi / (self.domain[1] - self.domain[0]))**2
            eigenvalues.append(eigenval)
            
            # Coeficiente inicial
            a_n_0 = initial_coeffs[n-1] if n-1 < len(initial_coeffs) else 0
            
            # Solução temporal para este modo
            a_n_t = a_n_0 * sp.exp(-eigenval * t)
            
            # Modo completo
            mode = a_n_t * self.spatial_basis[n-1]
            solution_modes.append(mode)
        
        # Solução completa é a soma dos modos
        solution = sum(solution_modes)
        
        # Armazenar informações adicionais
        self.eigenvalues = eigenvalues
        self.initial_coeffs = initial_coeffs
        self.solution_modes = solution_modes
        
        return solution
    
    def evaluate_at_time(self, time_value, n_terms=5):
        """
        Avalia a solução em um tempo específico.
        """
        if not hasattr(self, 'solution_modes'):
            self.solve(n_terms)
            
        x = sp.Symbol('x')
        t = sp.Symbol('t')
        
        # Substitui t pelo valor específico
        solution_at_t = sum(mode.subs(t, time_value) for mode in self.solution_modes)
        
        return solution_at_t
    
    def get_numerical_solution(self, x_points, time_points, n_terms=5):
        """
        Retorna a solução numérica em pontos específicos de espaço e tempo.
        """
        if not hasattr(self, 'solution_modes'):
            self.solve(n_terms)
            
        x_sym = sp.Symbol('x')
        t_sym = sp.Symbol('t')
        
        # Constrói a solução completa
        solution = sum(self.solution_modes)
        
        # Avalia numericamente
        results = np.zeros((len(time_points), len(x_points)))
        
        for i, t_val in enumerate(time_points):
            for j, x_val in enumerate(x_points):
                try:
                    value = float(solution.subs([(x_sym, x_val), (t_sym, t_val)]))
                    results[i, j] = value
                except:
                    results[i, j] = 0.0
                    
        return results
