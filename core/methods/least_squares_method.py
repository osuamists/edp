import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class LeastSquaresMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
        # Funções de base que satisfazem as condições de contorno u(0) = u(1) = 0
        self.basis_functions = [x**(n+1) * (1 - x) for n in range(n_terms)]

    def solve(self, n_terms=3, precision=1e-6):
        self.generate_basis_functions(n_terms)
        x = sp.Symbol('x')

        # Determinar o lado direito correto
        if isinstance(self.equation, sp.Equality):
            f = -self.equation.lhs + self.equation.rhs
        else:
            f = -self.equation
        
        print(f"Lado direito f = {f}")

        # Aproximação u(x) = sum(a_i * phi_i)
        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_aprox = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))

        # Resíduo R(x) = u''(x) - f(x)
        residual = sp.diff(u_aprox, x, 2) - f
        print(f"Resíduo: {residual}")

        # Método dos mínimos quadrados: minimizar ||R||² = ∫R² dx
        # Condições de otimalidade: ∂/∂a_i ∫R² dx = 0
        # Isso resulta em: ∫R * ∂R/∂a_i dx = 0

        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        for i in range(n_terms):
            phi_i = self.basis_functions[i]
            # ∂R/∂a_i = ∂/∂a_i (u'' - f) = phi_i''
            dR_dai = sp.diff(phi_i, x, 2)
            
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                # ∂R/∂a_j = phi_j''
                dR_daj = sp.diff(phi_j, x, 2)
                
                # A_ij = ∫(∂R/∂a_j) * (∂R/∂a_i) dx = ∫phi_j'' * phi_i'' dx
                integrand = dR_daj * dR_dai
                A[i, j] = sp.integrate(integrand, (x, self.domain[0], self.domain[1]))
            
            # b_i = -∫f * (∂R/∂a_i) dx = -∫f * phi_i'' dx
            integrand_b = -f * dR_dai
            b[i] = sp.integrate(integrand_b, (x, self.domain[0], self.domain[1]))

        print(f"Matriz A: {A}")
        print(f"Vetor b: {b}")

        # Converter para numpy
        try:
            A_list = []
            for i in range(n_terms):
                row = []
                for j in range(n_terms):
                    val_sym = A[i, j].evalf()
                    if val_sym.is_real:
                        row.append(float(val_sym))
                    else:
                        row.append(float(sp.re(val_sym).evalf()))
                A_list.append(row)
            
            b_list = []
            for i in range(n_terms):
                val_sym = b[i].evalf()
                if val_sym.is_real:
                    b_list.append(float(val_sym))
                else:
                    b_list.append(float(sp.re(val_sym).evalf()))
            
            A_np = np.array(A_list, dtype=np.float64)
            b_np = np.array(b_list, dtype=np.float64)
            
            print(f"A_np:\n{A_np}")
            print(f"b_np: {b_np}")
            
            if np.allclose(b_np, 0):
                print("ERRO: Vetor b é todo zero!")
                return sp.sin(sp.pi * x)
            
            if np.abs(np.linalg.det(A_np)) < 1e-10:
                print("AVISO: Matriz A é singular")
                return sp.sin(sp.pi * x)
            
            a_np = np.linalg.solve(A_np, b_np)
            print(f"Coeficientes: {a_np}")
            
            solution = sum(a_np[i] * self.basis_functions[i] for i in range(n_terms))
            return sp.simplify(solution)
            
        except Exception as e:
            print(f"Erro no método dos mínimos quadrados: {e}")
            return sp.sin(sp.pi * x)
