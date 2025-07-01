import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod


class LeastSquaresMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
        self.basis_functions = [x**n * (1 - x) for n in range(1, n_terms + 1)]


    def solve(self, n_terms=3, precision=1e-6):
        self.generate_basis_functions(n_terms)

        x = sp.Symbol('x')
        u = sp.Function('u')    
        f = self.equation if isinstance(self.equation, sp.Equality) else self.equation.rhs

        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_aprox = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))

        L_u = sp.diff(u_aprox, x, 2)  # L(u) = u''

        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        for i in range(n_terms):
            phi_i = self.basis_functions[i]
            L_phi_i = sp.diff(phi_i, x, 2)
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                L_phi_j = sp.diff(phi_j, x, 2)
                A[i, j] = sp.integrate(L_phi_j * L_phi_i, (x, self.domain[0], self.domain[1]))

            b[i] = sp.integrate(f * L_phi_i, (x, self.domain[0], self.domain[1]))

        b_np = []
        for i in range(n_terms):
            valor_real = sp.re(b[i].evalf())
            b_np.append(float(valor_real))
        b_np = np.array(b_np, dtype=np.float64)

        A_np = np.array(A.tolist(), dtype=np.float64)
        a_np = np.linalg.solve(A_np, b_np)

        solution = sum(a_np[i] * self.basis_functions[i] for i in range(n_terms))
        return sp.simplify(solution)
