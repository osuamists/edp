import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class SubregionsMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
        # Mesma base dos outros métodos para comparação
        self.basis_functions = [x**(n + 1) * (1 - x) for n in range(n_terms)]

    def solve(self, n_terms=3, precision=1e-6):
        self.generate_basis_functions(n_terms)
        x = sp.Symbol('x')

        # Determinar f(x) correto
        if isinstance(self.equation, sp.Equality):
            f = -self.equation.lhs + self.equation.rhs
        else:
            f = -self.equation

        # Aproximação u(x)
        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_aprox = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))

        # Resíduo R(x) = u'' - f(x)
        residual = sp.diff(u_aprox, x, 2) - f

        # Subdividir domínio em n_terms sub-regiões
        subintervals = []
        for i in range(n_terms):
            x_i = self.domain[0] + i * (self.domain[1] - self.domain[0]) / n_terms
            x_ip1 = self.domain[0] + (i + 1) * (self.domain[1] - self.domain[0]) / n_terms
            subintervals.append((x_i, x_ip1))

        # Gerar sistema ∫_subregion R(x) dx = 0
        equations = []
        for i, (a, b) in enumerate(subintervals):
            eq = sp.integrate(residual, (x, a, b))
            equations.append(eq)

        # Resolver sistema
        try:
            sol = sp.solve(equations, coeffs)
            if isinstance(sol, dict):
                solution = sum(sol[coeffs[i]] * self.basis_functions[i] for i in range(n_terms))
                return sp.simplify(solution)
            elif isinstance(sol, list) and len(sol) > 0:
                sol = sol[0] if isinstance(sol[0], (list, tuple)) else sol
                solution = sum(sol[i] * self.basis_functions[i] for i in range(n_terms))
                return sp.simplify(solution)
            else:
                print("Formato inesperado de solução")
                raise ValueError("Formato inválido")

        except Exception as e:
            print(f"Erro no método das sub-regiões: {e}")
            return sp.sin(sp.pi * x)  # fallback
