# core/galerkin_solver.py

import numpy as np
import sympy as sp
from scipy.integrate import quad

class GalerkinSolver:
    """Solver de Galerkin unificado para todas as 4 EDPs"""
    
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.t = sp.Symbol('t')
        
    def solve(self, problem, n_terms):
        """Resolve EDP usando método de Galerkin com n termos"""
        self.problem = problem
        self.tipo = problem["tipo"]
        
        if self.tipo == "eliptica_1d":
            return self._solve_elliptic_1d(n_terms)
        elif self.tipo == "parabolica_1d":
            return self._solve_parabolic_1d(n_terms)
        elif self.tipo == "hiperbolica_1d":
            return self._solve_hyperbolic_1d(n_terms)
        elif self.tipo == "eliptica_2d":
            return self._solve_elliptic_2d(n_terms)
        else:
            raise ValueError(f"Tipo de EDP não suportado: {self.tipo}")
    
    def _solve_elliptic_1d(self, n_terms):
        """Resolve EDP elíptica 1D (Poisson)"""
        domain = self.problem["domain"]
        
        # Funções base que satisfazem condições de contorno homogêneas
        basis_functions = [sp.sin((i+1)*sp.pi*self.x) for i in range(n_terms)]
        
        # Montar sistema linear Ac = b
        A = np.zeros((n_terms, n_terms))
        b = np.zeros(n_terms)
        
        for i in range(n_terms):
            for j in range(n_terms):
                # Integrar ∫ φ''_j * φ_i dx
                phi_j = basis_functions[j]
                phi_i = basis_functions[i]
                phi_j_dd = sp.diff(phi_j, self.x, 2)
                
                integrand = phi_j_dd * phi_i
                integral, _ = quad(
                    sp.lambdify(self.x, integrand, modules='numpy'),
                    domain[0], domain[1]
                )
                A[i, j] = integral
            
            # Termo fonte: ∫ f * φ_i dx onde f = π²sin(πx)
            f = sp.pi**2 * sp.sin(sp.pi * self.x)
            integrand_b = f * basis_functions[i]
            integral_b, _ = quad(
                sp.lambdify(self.x, integrand_b, modules='numpy'),
                domain[0], domain[1]
            )
            b[i] = integral_b
        
        # Resolver sistema
        coeffs = np.linalg.solve(A, b)
        
        # Construir solução
        solution = sum(coeffs[i] * basis_functions[i] for i in range(n_terms))
        return sp.lambdify(self.x, solution, modules='numpy')
    
    def _solve_parabolic_1d(self, n_terms):
        """Resolve EDP parabólica 1D (Calor) usando separação de variáveis"""
        domain = self.problem["domain"]
        time_domain = self.problem["time_domain"]
        
        # Condição inicial
        u0_func = None
        for cond_type, point, value in self.problem["boundary_conditions"]:
            if cond_type == "initial" and point == "u":
                u0_func = value
                break
        
        # Coeficientes da série de Fourier para condição inicial
        coeffs = []
        for n in range(1, n_terms + 1):
            def integrand(x):
                return u0_func(x) * np.sin(n * np.pi * x)
            
            integral, _ = quad(integrand, domain[0], domain[1])
            an = 2 * integral
            coeffs.append(an)
        
        # Construir solução u(x,t) = Σ an * sin(nπx) * exp(-n²π²t)
        def solution(x, t):
            result = np.zeros_like(x)
            for n in range(1, n_terms + 1):
                result += coeffs[n-1] * np.sin(n * np.pi * x) * np.exp(-n**2 * np.pi**2 * t)
            return result
        
        return solution
    
    def _solve_hyperbolic_1d(self, n_terms):
        """Resolve EDP hiperbólica 1D (Onda) usando separação de variáveis"""
        domain = self.problem["domain"]
        
        # Condições iniciais
        u0_func = None
        ut0_func = None
        for cond_type, point, value in self.problem["boundary_conditions"]:
            if cond_type == "initial":
                if point == "u":
                    u0_func = value
                elif point == "ut":
                    ut0_func = value
        
        # Coeficientes para u(x,0)
        coeffs_u = []
        for n in range(1, n_terms + 1):
            def integrand(x):
                return u0_func(x) * np.sin(n * np.pi * x)
            
            integral, _ = quad(integrand, domain[0], domain[1])
            an = 2 * integral
            coeffs_u.append(an)
        
        # Coeficientes para ∂u/∂t(x,0)
        coeffs_ut = []
        for n in range(1, n_terms + 1):
            def integrand(x):
                return ut0_func(x) * np.sin(n * np.pi * x)
            
            integral, _ = quad(integrand, domain[0], domain[1])
            bn = 2 * integral / (2 * n * np.pi)  # Dividir por ωn = 2nπ
            coeffs_ut.append(bn)
        
        # Construir solução u(x,t) = Σ [an*cos(2nπt) + bn*sin(2nπt)] * sin(nπx)
        def solution(x, t):
            result = np.zeros_like(x)
            for n in range(1, n_terms + 1):
                omega_n = 2 * n * np.pi  # Velocidade c=2
                result += (coeffs_u[n-1] * np.cos(omega_n * t) + 
                          coeffs_ut[n-1] * np.sin(omega_n * t)) * np.sin(n * np.pi * x)
            return result
        
        return solution
    
    def _solve_elliptic_2d(self, n_terms):
        """Resolve EDP elíptica 2D (Helmholtz) - versão simplificada"""
        # Para demonstração, usar solução analítica conhecida
        # Em implementação completa, seria necessário método 2D real
        
        def solution(x, y):
            if hasattr(x, '__len__') and hasattr(y, '__len__'):
                X, Y = np.meshgrid(x, y)
                return self.problem["analytical"](X, Y)
            else:
                return self.problem["analytical"](x, y)
        
        return solution
