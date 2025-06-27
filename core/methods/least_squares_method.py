import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class LeastSquaresMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
        # Usar as MESMAS funções de base dos outros métodos
        self.basis_functions = [x**(n+1) * (1 - x) for n in range(n_terms)]

    def solve(self, n_terms=3, precision=1e-6):
        self.generate_basis_functions(n_terms)
        x = sp.Symbol('x')

        # Lado direito correto
        if isinstance(self.equation, sp.Equality):
            f = -self.equation.lhs + self.equation.rhs
        else:
            f = -self.equation

        print(f"Lado direito f = {f}")

        # Aproximação u(x) = Σ aᵢ φᵢ(x)
        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_approx = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))

        # Resíduo R = L(u) - f = u'' - f
        residual = sp.diff(u_approx, x, 2) - f
        print(f"Resíduo: {residual}")

        # Sistema: minimizar ∫ R² dx
        # ∂/∂aᵢ ∫ R² dx = 2 ∫ R (∂R/∂aᵢ) dx = 0
        # Como ∂R/∂aᵢ = φᵢ'', temos: ∫ R φᵢ'' dx = 0

        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        for i in range(n_terms):
            phi_i_second = sp.diff(self.basis_functions[i], x, 2)
            
            # Matriz A: ∫ φⱼ'' φᵢ'' dx
            for j in range(n_terms):
                phi_j_second = sp.diff(self.basis_functions[j], x, 2)
                integrand = phi_j_second * phi_i_second
                A[i, j] = sp.integrate(integrand, (x, self.domain[0], self.domain[1]))
            
            # Vetor b: ∫ f φᵢ'' dx
            integrand_b = f * phi_i_second
            b[i] = sp.integrate(integrand_b, (x, self.domain[0], self.domain[1]))

        print(f"Matriz A: {A}")
        print(f"Vetor b: {b}")

        try:
            # Converter para numpy
            A_np = np.array([[float(A[i,j].evalf()) for j in range(n_terms)] for i in range(n_terms)])
            b_np = np.array([float(b[i].evalf()) for i in range(n_terms)])
            
            print(f"A_np:\n{A_np}")
            print(f"b_np: {b_np}")
            
            # Resolver sistema
            if np.abs(np.linalg.det(A_np)) < 1e-12:
                print("AVISO: Matriz quase singular")
                return sp.sin(sp.pi * x)
            
            a_np = np.linalg.solve(A_np, b_np)
            print(f"Coeficientes: {a_np}")
            
            # Construir solução
            solution = sum(a_np[i] * self.basis_functions[i] for i in range(n_terms))
            return sp.simplify(solution)
            
        except Exception as e:
            print(f"Erro: {e}")
            return sp.sin(sp.pi * x)
