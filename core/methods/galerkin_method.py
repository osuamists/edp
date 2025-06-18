import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class GalerkinMethod(NumericalMethod): 
    def generate_basis_functions(self, n_terms):
        """
        Gera funções base do tipo: x*(1 - x), x^2*(1 - x), ..., x^n*(1 - x)
        Elas automaticamente respeitam as condições de contorno u(0) = u(1) = 0
        """
        x = sp.Symbol('x')
        self.basis_functions = [x**n * (1 - x) for n in range(1, n_terms + 1)]

    def solve(self, n_terms=3, precision=1e-6):
        self.generate_basis_functions(n_terms)

        x = sp.Symbol('x')
        u = sp.Function('u')
        
        # Construir aproximação u_n = sum(a_i * phi_i)  
        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_approx = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))
        
        # Substituir na equação diferencial
        residual = self.equation.subs(u(x), u_approx)

        # Montar sistema linear A * a = b
        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        for i in range(n_terms):
            phi_i = self.basis_functions[i]
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                # Para equação -u'' = f(x), temos ∫ u'' * phi_i dx = ∫ f * phi_i dx
                # Por integração por partes: ∫ u' * phi_i' dx = ∫ f * phi_i dx
                integrand = sp.integrate(
                    sp.diff(phi_j, x) * sp.diff(phi_i, x),
                    (x, self.domain[0], self.domain[1])
                )
                A[i, j] = integrand
            
            # Lado direito: assumindo equação da forma -u'' = f(x)
            if hasattr(self.equation, 'rhs'):
                f = -self.equation.rhs
            else:
                # Se a equação não tem .rhs, assumir que é da forma -u'' = 0
                f = 0
            rhs = sp.integrate(f * phi_i, (x, self.domain[0], self.domain[1]))
            b[i] = rhs

        # Resolver sistema
        A_np = np.array(A.tolist(), dtype=np.float64)
        b_np = np.array(b.tolist(), dtype=np.float64).flatten()
        a_np = np.linalg.solve(A_np, b_np)

        # Construir solução aproximada
        solution = sum(a_np[i] * self.basis_functions[i] for i in range(n_terms))
        return sp.simplify(solution)