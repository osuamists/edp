import sympy as sp
import numpy as np
from .galerkin_method import GalerkinMethod

class Helmholtz2DMethod(GalerkinMethod):
    """
    Método de Galerkin especializado para a Equação de Helmholtz 2D:
    ∂²φ/∂x² + ∂²φ/∂y² + λφ = 0
    
    Problema de autovalor em domínio retangular [0,1] × [0,γ]
    """
    
    def __init__(self, domain, boundary_conditions, lambda_param=None):
        """
        Args:
            domain: Domínio 2D ((x_min, x_max), (y_min, y_max))
            boundary_conditions: Condições de contorno Dirichlet
            lambda_param: Parâmetro λ da equação (será calculado como autovalor)
        """
        super().__init__(None, domain, boundary_conditions)
        self.lambda_param = lambda_param
        self.gamma = sp.Symbol('gamma', positive=True)  # Parâmetro do domínio
        
    def generate_basis_functions_2d(self, n_terms_x, n_terms_y):
        """
        Gera funções base 2D para o domínio retangular
        φ_mn(x,y) = sin(mπx) * sin(nπy/γ)
        """
        x = sp.Symbol('x')
        y = sp.Symbol('y')
        
        # Domínio [0,1] × [0,γ]
        (x_min, x_max), (y_min, y_max) = self.domain
        
        self.basis_functions_2d = []
        self.mode_indices = []
        
        for m in range(1, n_terms_x + 1):
            for n in range(1, n_terms_y + 1):
                # Função base: sin(mπx) * sin(nπy/γ)
                phi_x = sp.sin(m * sp.pi * x)
                phi_y = sp.sin(n * sp.pi * y / self.gamma)
                basis_func = phi_x * phi_y
                
                self.basis_functions_2d.append(basis_func)
                self.mode_indices.append((m, n))
        
        return self.basis_functions_2d
    
    def calculate_eigenvalues(self, n_terms_x=3, n_terms_y=3):
        """
        Calcula os autovalores da equação de Helmholtz 2D
        λ_mn = π²(m² + n²/γ²)
        """
        eigenvalues = {}
        
        for m in range(1, n_terms_x + 1):
            for n in range(1, n_terms_y + 1):
                # Autovalor: λ_mn = π²(m² + n²/γ²)
                lambda_mn = sp.pi**2 * (m**2 + n**2 / self.gamma**2)
                eigenvalues[(m, n)] = lambda_mn
        
        return eigenvalues
    
    def solve_eigenvalue_problem(self, gamma_value=1.0, n_terms_x=3, n_terms_y=3):
        """
        Resolve o problema de autovalor para um valor específico de γ
        """
        # Substituir γ por valor numérico
        eigenvalues = self.calculate_eigenvalues(n_terms_x, n_terms_y)
        
        numerical_eigenvalues = {}
        eigenfunctions = {}
        
        x = sp.Symbol('x')
        y = sp.Symbol('y')
        
        for (m, n), lambda_val in eigenvalues.items():
            # Calcular autovalor numérico
            lambda_numerical = float(lambda_val.subs(self.gamma, gamma_value))
            numerical_eigenvalues[(m, n)] = lambda_numerical
            
            # Autofunção correspondente
            phi_mn = sp.sin(m * sp.pi * x) * sp.sin(n * sp.pi * y / gamma_value)
            eigenfunctions[(m, n)] = phi_mn
        
        return numerical_eigenvalues, eigenfunctions
    
    def solve(self, gamma_value=1.0, n_terms_x=3, n_terms_y=3):
        """
        Resolve a equação de Helmholtz 2D
        Retorna os primeiros modos (autofunções) e autovalores
        """
        self.generate_basis_functions_2d(n_terms_x, n_terms_y)
        
        # Resolver problema de autovalor
        eigenvalues, eigenfunctions = self.solve_eigenvalue_problem(
            gamma_value, n_terms_x, n_terms_y
        )
        
        # Ordenar por autovalor (frequência)
        sorted_modes = sorted(eigenvalues.items(), key=lambda x: x[1])
        
        solutions = {}
        for i, ((m, n), lambda_val) in enumerate(sorted_modes):
            mode_name = f"φ_{m}{n}"
            solutions[mode_name] = {
                "eigenvalue": lambda_val,
                "eigenfunction": eigenfunctions[(m, n)],
                "mode_numbers": (m, n),
                "frequency": np.sqrt(lambda_val) if lambda_val > 0 else 0
            }
        
        return solutions
    
    def get_fundamental_mode(self, gamma_value=1.0):
        """
        Retorna o modo fundamental (menor autovalor)
        """
        solutions = self.solve(gamma_value=gamma_value)
        
        # Encontrar modo com menor autovalor
        min_eigenvalue = float('inf')
        fundamental_mode = None
        
        for mode_name, mode_data in solutions.items():
            if mode_data["eigenvalue"] < min_eigenvalue:
                min_eigenvalue = mode_data["eigenvalue"]
                fundamental_mode = mode_data
        
        return fundamental_mode
    
    def evaluate_at_point(self, x_val, y_val, mode="φ_11", gamma_value=1.0):
        """
        Avalia uma autofunção específica em um ponto (x, y)
        """
        solutions = self.solve(gamma_value=gamma_value)
        
        if mode not in solutions:
            available_modes = list(solutions.keys())
            raise ValueError(f"Modo '{mode}' não encontrado. Disponíveis: {available_modes}")
        
        eigenfunction = solutions[mode]["eigenfunction"]
        x = sp.Symbol('x')
        y = sp.Symbol('y')
        
        result = eigenfunction.subs([(x, x_val), (y, y_val)])
        return float(result.evalf())
    
    def get_resonance_frequencies(self, gamma_value=1.0, n_terms_x=5, n_terms_y=5):
        """
        Calcula as frequências de ressonância (raízes quadradas dos autovalores)
        """
        eigenvalues, _ = self.solve_eigenvalue_problem(gamma_value, n_terms_x, n_terms_y)
        
        frequencies = {}
        for (m, n), lambda_val in eigenvalues.items():
            if lambda_val > 0:
                frequency = np.sqrt(lambda_val)
                frequencies[(m, n)] = frequency
        
        # Ordenar por frequência
        sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1])
        
        return sorted_frequencies
    
    def analyze_gamma_dependence(self, gamma_values, mode=(1, 1)):
        """
        Analisa como o autovalor varia com γ para um modo específico
        """
        m, n = mode
        results = []
        
        for gamma_val in gamma_values:
            # λ_mn = π²(m² + n²/γ²)
            lambda_val = sp.pi**2 * (m**2 + n**2 / gamma_val**2)
            results.append({
                "gamma": gamma_val,
                "eigenvalue": float(lambda_val),
                "frequency": float(sp.sqrt(lambda_val))
            })
        
        return results
    
    def get_solution_info(self):
        """
        Retorna informações sobre a solução
        """
        return {
            "tipo": "Equação de Helmholtz 2D (Elíptica)",
            "metodo": "Separação de Variáveis + Método de Galerkin",
            "condicoes_contorno": "Dirichlet homogêneas",
            "forma_solucao": "φ_mn(x,y) = sin(mπx) * sin(nπy/γ)",
            "autovalores": "λ_mn = π²(m² + n²/γ²)",
            "problema": "Autovalor - encontrar frequências de ressonância"
        }
    
    def get_mode_shape(self, mode=(1, 1), gamma_value=1.0, grid_size=50):
        """
        Gera dados para plotar a forma do modo
        """
        m, n = mode
        x = sp.Symbol('x')
        y = sp.Symbol('y')
        
        # Autofunção
        phi_mn = sp.sin(m * sp.pi * x) * sp.sin(n * sp.pi * y / gamma_value)
        
        # Criar grade
        x_vals = np.linspace(0, 1, grid_size)
        y_vals = np.linspace(0, gamma_value, grid_size)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        # Avaliar função na grade
        Z = np.zeros_like(X)
        for i in range(grid_size):
            for j in range(grid_size):
                Z[i, j] = float(phi_mn.subs([(x, X[i, j]), (y, Y[i, j])]))
        
        return X, Y, Z
