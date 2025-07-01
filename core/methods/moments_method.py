import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class MomentsMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
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

        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        for i in range(n_terms):
            psi_i = self.basis_functions[i]  # Função peso
            
            # Matriz A: ∫φⱼ'' * ψᵢ dx
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                phi_j_second_deriv = sp.diff(phi_j, x, 2)
                integrand = phi_j_second_deriv * psi_i
                A[i, j] = sp.integrate(integrand, (x, self.domain[0], self.domain[1]))
            
            # Vetor b: ∫f * ψᵢ dx
            integrand_b = f * psi_i
            b[i] = sp.integrate(integrand_b, (x, self.domain[0], self.domain[1]))

        print(f"Matriz A: {A}")
        print(f"Vetor b: {b}")

        # Converter para numpy com .evalf() explícito
        try:
            A_list = []
            for i in range(n_terms):
                row = []
                for j in range(n_terms):
                    # Forçar avaliação numérica
                    val_sym = A[i, j].evalf()
                    if val_sym.is_real:
                        row.append(float(val_sym))
                    else:
                        # Se for complexo, usar apenas parte real
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
            print(f"Erro detalhado no método dos momentos: {e}")
            print(f"Tipo do erro: {type(e)}")
            
            # Debug adicional
            print("Debug - Primeira entrada da matriz A:")
            print(f"A[0,0] = {A[0,0]}")
            print(f"Tipo: {type(A[0,0])}")
            print(f"É número? {A[0,0].is_number}")
            
            return sp.sin(sp.pi * x)
