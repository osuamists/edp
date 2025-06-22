import sympy as sp 
import numpy as np 
from .numerical_method import NumericalMethod

class RayleighRitzMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
        self.basis_functions = [x**n * (1 - x) for n in range(1, n_terms + 1)]

    def solve(self, n_terms=3, precision=1e-6):  # <- Tudo abaixo deve estar indentado
        self.generate_basis_functions(n_terms)

        x = sp.Symbol('x')
        u = sp.Function('u')

        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_approx = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))

        if isinstance(self.equation, sp.Equality):
            f = self.equation.rhs
        else:
            f = self.equation

        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        for i in range(n_terms):
            phi_i = self.basis_functions[i]
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                A[i, j] = sp.integrate(sp.diff(phi_i, x) * sp.diff(phi_j, x), (x, self.domain[0], self.domain[1]))
            b[i] = sp.integrate(f * phi_i, (x, self.domain[0], self.domain[1]))
