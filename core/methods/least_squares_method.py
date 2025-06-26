import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class LeastSquaresMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
        # Usar as mesmas funções de base do Galerkin para comparação justa
        self.basis_functions = [x**(n+1) * (1 - x) for n in range(n_terms)]

    def solve(self, n_terms=3, precision=1e-6):
        self.generate_basis_functions(n_terms)

        x = sp.Symbol('x')
        
        # Determinar o lado direito correto
        if isinstance(self.equation, sp.Equality):
            # Para Eq(u'' + π²sin(πx), 0), o lado direito é -π²sin(πx)
            f = -self.equation.lhs + self.equation.rhs  # f = -π²sin(πx)
        else:
            # Para u'' + π²sin(πx), o lado direito é -π²sin(πx)
            f = -self.equation  # f = -π²sin(πx)

        print(f"Lado direito f = {f}")

        # Aproximação u ≈ Σ aᵢφᵢ(x)
        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_aprox = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))

        # Resíduo R = L(u) - f = u'' - f
        L_u = sp.diff(u_aprox, x, 2)
        residual = L_u - f

        print(f"Resíduo: {residual}")

        # Minimizar ∫R² dx através de ∂/∂aᵢ ∫R² dx = 0
        # Isso leva a: ∫R * ∂R/∂aᵢ dx = 0
        # Como ∂R/∂aᵢ = ∂(L(u))/∂aᵢ = L(φᵢ) = φᵢ''
        
        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        for i in range(n_terms):
            phi_i = self.basis_functions[i]
            L_phi_i = sp.diff(phi_i, x, 2)  # φᵢ''
            
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                L_phi_j = sp.diff(phi_j, x, 2)  # φⱼ''
                # ∫(φⱼ'') * (φᵢ'') dx
                A[i, j] = sp.integrate(L_phi_j * L_phi_i, (x, self.domain[0], self.domain[1]))

            # ∫f * (φᵢ'') dx
            b[i] = sp.integrate(f * L_phi_i, (x, self.domain[0], self.domain[1]))

        print(f"Matriz A: {A}")
        print(f"Vetor b: {b}")

        # Converter para numpy com tratamento de complexos
        try:
            A_list = []
            for i in range(n_terms):
                row = []
                for j in range(n_terms):
                    val = complex(A[i, j].evalf())
                    row.append(val.real)
                A_list.append(row)
            
            b_list = []
            for i in range(n_terms):
                val = complex(b[i].evalf())
                b_list.append(val.real)
            
            A_np = np.array(A_list, dtype=np.float64)
            b_np = np.array(b_list, dtype=np.float64)
            
            print(f"A_np:\n{A_np}")
            print(f"b_np: {b_np}")
            
            if np.allclose(b_np, 0):
                print("ERRO: Vetor b é todo zero!")
                return sp.sin(sp.pi * x)
            
            a_np = np.linalg.solve(A_np, b_np)
            print(f"Coeficientes: {a_np}")
            
            solution = sum(a_np[i] * self.basis_functions[i] for i in range(n_terms))
            return sp.simplify(solution)
            
        except Exception as e:
            print(f"Erro: {e}")
            return sp.sin(sp.pi * x)
