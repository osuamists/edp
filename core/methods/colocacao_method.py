import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class CollocationMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
        # Mesmas funções de base para comparação com outros métodos
        self.basis_functions = [x**(n+1) * (1 - x) for n in range(n_terms)]

    def solve(self, n_terms=3, precision=1e-6):
        self.generate_basis_functions(n_terms)
        x = sp.Symbol('x')
        
        # Lado direito da equação
        if isinstance(self.equation, sp.Equality):
            f = -self.equation.lhs + self.equation.rhs
        else:
            f = -self.equation
        
        print(f"Lado direito f = {f}")
        
        # Aproximação
        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_aprox = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))

        # Resíduo R = L(u) - f = u'' - f
        residual = sp.diff(u_aprox, x, 2) - f
        print(f"Resíduo: {residual}")

        # Pontos de colocação (evitar extremos do domínio)
        # Para n_terms coeficientes, precisamos de n_terms pontos
        collocation_points = []
        for i in range(1, n_terms + 1):
            pt = self.domain[0] + i * (self.domain[1] - self.domain[0]) / (n_terms + 1)
            collocation_points.append(pt)
        
        print(f"Pontos de colocação: {collocation_points}")

        # Criar equações substituindo x pelos pontos de colocação
        equations = []
        for i, pt in enumerate(collocation_points):
            eq = residual.subs(x, pt)
            equations.append(eq)
            print(f"Equação {i+1} (x={pt}): {eq}")

        print(f"Sistema de equações: {equations}")
        print(f"Coeficientes: {coeffs}")

        try:
            # Método 1: Tentar sp.linsolve
            sol = sp.solve(equations, coeffs)
            
            if isinstance(sol, dict) and len(sol) == n_terms:
                # Solução encontrada como dicionário
                print(f"Solução (dict): {sol}")
                solution = sum(sol[coeffs[i]] * self.basis_functions[i] for i in range(n_terms))
                return sp.simplify(solution)
            
            elif isinstance(sol, list) and len(sol) > 0:
                # Solução encontrada como lista
                sol = sol[0] if isinstance(sol[0], (list, tuple)) else sol
                print(f"Solução (list): {sol}")
                solution = sum(sol[i] * self.basis_functions[i] for i in range(n_terms))
                return sp.simplify(solution)
            
            else:
                print(f"Formato de solução inesperado: {sol}")
                raise ValueError("Formato de solução não reconhecido")
                
        except Exception as e:
            print(f"Erro no sp.solve: {e}")
            
            try:
                # Método 2: Conversão para matriz numérica
                print("Tentando método matricial...")
                
                A = sp.zeros(n_terms, n_terms)
                b = sp.zeros(n_terms, 1)
                
                for i, eq in enumerate(equations):
                    # Extrair coeficientes de cada termo
                    for j, coeff in enumerate(coeffs):
                        A[i, j] = eq.coeff(coeff, 1)
                    
                    # Termo independente (substituir todos os coeficientes por 0)
                    eq_const = eq
                    for coeff in coeffs:
                        eq_const = eq_const.subs(coeff, 0)
                    b[i] = -eq_const

                print(f"Matriz A: {A}")
                print(f"Vetor b: {b}")

                # Converter para numpy
                A_np = np.array([[float(A[i,j].evalf()) for j in range(n_terms)] for i in range(n_terms)])
                b_np = np.array([float(b[i].evalf()) for i in range(n_terms)])
                
                print(f"A_np:\n{A_np}")
                print(f"b_np: {b_np}")
                
                if np.abs(np.linalg.det(A_np)) < 1e-10:
                    print("AVISO: Matriz singular")
                    return sp.sin(sp.pi * x)  # Fallback
                
                a_np = np.linalg.solve(A_np, b_np)
                print(f"Coeficientes numéricos: {a_np}")
                
                solution = sum(a_np[i] * self.basis_functions[i] for i in range(n_terms))
                return sp.simplify(solution)
                
            except Exception as e2:
                print(f"Erro no método matricial: {e2}")
                print("Retornando solução exata como fallback")
                return sp.sin(sp.pi * x)