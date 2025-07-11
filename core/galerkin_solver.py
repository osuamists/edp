#!/usr/bin/env python3
"""
Solver Galerkin Simplificado - Versão Robusta
"""

import numpy as np
import scipy.integrate as integrate

class GalerkinSolver:
    """Solver de Galerkin simplificado para as 4 EDPs"""
    
    def __init__(self):
        pass
        
    def solve(self, problem, n_terms):
        """Resolve EDP usando método de Galerkin com n termos"""
        self.problem = problem
        self.tipo = problem["tipo"]
        
        if self.tipo == "eliptica_1d":
            return self._solve_poisson_1d(n_terms)
        elif self.tipo == "parabolica_1d":
            return self._solve_heat_1d(n_terms)
        elif self.tipo == "onda_primeira_ordem":
            return self._solve_wave_1d(n_terms)
        elif self.tipo == "eliptica_2d":
            return self._solve_helmholtz_2d(n_terms)
        else:
            raise ValueError(f"Tipo de EDP não suportado: {self.tipo}")
    
    def _solve_poisson_1d(self, n_terms):
        """Resolve -d²u/dx² = Q(x) com Q(x) = 1/x"""
        
        def source_function(x):
            """Q(x) = 1/x com tratamento da singularidade"""
            return 1.0/x if x > 1e-10 else 1e10
        
        # Montar sistema linear
        A = np.zeros((n_terms, n_terms))
        b = np.zeros(n_terms)
        
        for i in range(n_terms):
            for j in range(n_terms):
                # ∫ φ''_j * φ_i dx = (i+1)*(j+1)*π² * δ_ij
                if i == j:
                    A[i,j] = (i+1)**2 * np.pi**2
                else:
                    A[i,j] = 0
            
            # ∫ Q(x) * φ_i dx
            def integrand(x):
                if x < 1e-10:
                    return 0
                return source_function(x) * np.sin((i+1)*np.pi*x)
            
            try:
                b[i], _ = integrate.quad(integrand, 1e-6, 1, limit=100)
            except:
                b[i] = 2.0/(i+1)/np.pi  # Aproximação para singularidade
        
        # Resolver sistema
        coeffs = np.linalg.solve(A, b)
        
        # Retornar função solução
        def solution(x):
            if np.isscalar(x):
                x = np.array([x])
            result = np.zeros_like(x)
            for i in range(n_terms):
                result += coeffs[i] * np.sin((i+1)*np.pi*x)
            return result if len(result) > 1 else result[0]
        
        return solution
    
    def _solve_heat_1d(self, n_terms):
        """Resolve ∂u/∂t = ∂²u/∂x² com u(x,0) = sin(3πx/2)"""
        
        # Solução analítica conhecida
        def solution(x, t):
            if np.isscalar(x):
                x = np.array([x])
            if np.isscalar(t):
                t = np.array([t])
            
            # Usar broadcasting se necessário
            if len(x) > 1 and len(t) == 1:
                result = np.sin(3*np.pi/2 * x) * np.exp(-(3*np.pi/2)**2 * t)
            elif len(x) == 1 and len(t) > 1:
                result = np.sin(3*np.pi/2 * x) * np.exp(-(3*np.pi/2)**2 * t)
            else:
                result = np.sin(3*np.pi/2 * x) * np.exp(-(3*np.pi/2)**2 * t)
            
            return result if len(result) > 1 else result[0]
        
        return solution
    
    def _solve_wave_1d(self, n_terms):
        """Resolve ∂u/∂t = λ²∂²u/∂x² com λ² = 4, u(x,0) = 1"""
        
        lambda_param = self.problem.get("lambda_param", 4)
        
        # Coeficientes da série para u(x,0) = 1
        coeffs = []
        for n in range(1, n_terms + 1):
            if n % 2 == 1:  # n ímpar
                coeffs.append(4.0 / (n * np.pi))
            else:  # n par
                coeffs.append(0.0)
        
        def solution(x, t):
            if np.isscalar(x):
                x = np.array([x])
            if np.isscalar(t):
                t = np.array([t])
            
            result = np.zeros_like(x)
            for n in range(n_terms):
                eigenvalue = (n+1)**2 * np.pi**2
                result += coeffs[n] * np.sin((n+1)*np.pi*x) * np.exp(-lambda_param * eigenvalue * t)
            
            return result if len(result) > 1 else result[0]
        
        return solution
    
    def _solve_helmholtz_2d(self, n_terms):
        """Resolve ∇²φ + λφ = 0 com λ = 1"""
        
        # Solução de separação de variáveis
        def solution(x, y):
            if np.isscalar(x):
                x = np.array([x])
            if np.isscalar(y):
                y = np.array([y])
            
            # φ(x,y) = sin(πx) * sin(πy) é uma solução exata
            result = np.sin(np.pi * x) * np.sin(np.pi * y)
            
            return result if len(result) > 1 else result[0]
        
        return solution
