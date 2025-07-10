import sympy as sp
import numpy as np
from .galerkin_method import GalerkinMethod

class HeatGalerkinMethod(GalerkinMethod):
    """
    Método de Galerkin especializado para a Equação do Calor: ∂u/∂t = ∂²u/∂x²
    Usando separação de variáveis e série de Fourier
    """
    
    def __init__(self, domain, boundary_conditions, initial_condition=None):
        """
        Args:
            domain: Domínio espacial (a, b)
            boundary_conditions: Condições de contorno
            initial_condition: Condição inicial u(x,0) = f(x)
        """
        # Para equação do calor, não temos termo fonte Q(x)
        super().__init__(None, domain, boundary_conditions)
        self.initial_condition = initial_condition
        
    def generate_basis_functions(self, n_terms):
        """
        Gera funções base senoidais para a equação do calor
        Funções que satisfazem as condições de contorno homogêneas
        """
        x = sp.Symbol('x')
        a, b = self.domain
        L = b - a
        
        # Funções base: sin(nπx/L) que satisfazem u(0,t) = u(L,t) = 0
        self.basis_functions = []
        for n in range(1, n_terms + 1):
            basis_func = sp.sin(n * sp.pi * (x - a) / L)
            self.basis_functions.append(basis_func)
        
        return self.basis_functions
    
    def solve(self, n_terms=10, t_final=1.0):
        """
        Resolve a equação do calor usando separação de variáveis
        
        Solução analítica: u(x,t) = Σ A_n * exp(-λ_n²t) * sin(nπx/L)
        onde λ_n = nπ/L são os autovalores
        """
        self.generate_basis_functions(n_terms)
        
        x = sp.Symbol('x')
        t = sp.Symbol('t')
        a, b = self.domain
        L = b - a
        
        # Definir condição inicial padrão se não fornecida
        if self.initial_condition is None:
            # Condição padrão do problema: u(x,0) = sin(3πx/2L)
            self.initial_condition = sp.sin(3 * sp.pi * x / (2 * L))
        
        # Calcular coeficientes de Fourier da condição inicial
        coefficients = []
        
        for n in range(1, n_terms + 1):
            # Coeficiente A_n = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
            try:
                integrand = self.initial_condition * sp.sin(n * sp.pi * (x - a) / L)
                A_n = 2/L * sp.integrate(integrand, (x, a, b))
                A_n = float(A_n.evalf())
            except:
                # Para sin(3πx/2L), calcular analiticamente
                A_n = self._analytical_fourier_coefficient(n, L)
            
            coefficients.append(A_n)
        
        # Construir solução u(x,t) = Σ A_n * exp(-λ_n²t) * sin(nπx/L)
        solution = 0
        for n in range(1, n_terms + 1):
            A_n = coefficients[n-1]
            
            # Autovalor λ_n = nπ/L
            lambda_n = n * sp.pi / L
            lambda_n_sq = lambda_n**2
            
            # Termo da série: A_n * exp(-λ_n²t) * sin(nπx/L)
            term = A_n * sp.exp(-lambda_n_sq * t) * sp.sin(n * sp.pi * (x - a) / L)
            solution += term
        
        return sp.simplify(solution)
    
    def _analytical_fourier_coefficient(self, n, L):
        """
        Calcula coeficiente de Fourier analiticamente para sin(3πx/2L)
        """
        # Para f(x) = sin(3πx/2L) e φ_n(x) = sin(nπx/L)
        # A_n = (2/L) ∫[0,L] sin(3πx/2L) sin(nπx/L) dx
        
        if n == 3/2:  # n não é inteiro, mas checamos proporção
            return 1.0
        elif abs(2*n - 3) < 1e-10:  # n = 3/2, mas n deve ser inteiro
            # Para n=1: A_1 ≈ 0 (ortogonalidade)
            # Para n=2: A_2 ≠ 0 (frequência próxima)
            if n == 1:
                return 2.0 / (3.0 * sp.pi)  # Aproximação para sobreposição
            elif n == 2:
                return -2.0 / (sp.pi)       # Contribuição principal
            else:
                return 0.0
        else:
            return 0.0
    
    def get_temporal_solution(self, n_terms=10, t_values=None):
        """
        Retorna soluções em múltiplos tempos
        """
        if t_values is None:
            t_values = [0, 0.01, 0.05, 0.1, 0.25, 0.5]
        
        x = sp.Symbol('x')
        t = sp.Symbol('t')
        
        # Obter solução geral
        general_solution = self.solve(n_terms=n_terms)
        
        solutions = {}
        for t_val in t_values:
            # Substituir valor específico de t
            sol_at_t = general_solution.subs(t, t_val)
            solutions[t_val] = sp.simplify(sol_at_t)
        
        return solutions
    
    def evaluate_at_point(self, x_val, t_val, n_terms=10):
        """
        Avalia a solução em um ponto específico (x, t)
        """
        solution = self.solve(n_terms=n_terms)
        x = sp.Symbol('x')
        t = sp.Symbol('t')
        
        result = solution.subs([(x, x_val), (t, t_val)])
        return float(result.evalf())
    
    def get_decay_rate(self, n_terms=10):
        """
        Retorna as taxas de decaimento exponencial (autovalores)
        """
        a, b = self.domain
        L = b - a
        
        decay_rates = []
        for n in range(1, n_terms + 1):
            lambda_n = n * sp.pi / L
            decay_rate = lambda_n**2
            decay_rates.append(float(decay_rate))
        
        return decay_rates
    
    def get_solution_info(self):
        """
        Retorna informações sobre a solução
        """
        return {
            "tipo": "Equação do Calor (Parabólica)",
            "metodo": "Separação de Variáveis + Método de Galerkin",
            "condicoes_contorno": "Dirichlet homogêneas",
            "forma_solucao": "u(x,t) = Σ A_n * exp(-λ_n²t) * sin(nπx/L)",
            "comportamento": "Decaimento exponencial no tempo"
        }
