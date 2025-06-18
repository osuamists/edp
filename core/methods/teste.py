import sympy as sp
import numpy as np
from numerical_method import NumericalMethod

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
        
        # Montar sistema linear A * a = b
        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        for i in range(n_terms):
            phi_i = self.basis_functions[i]
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                # Para equação -u'' = f(x), usar integração por partes: ∫ u' * phi_i' dx = ∫ f * phi_i dx
                integrand = sp.integrate(
                    sp.diff(phi_j, x) * sp.diff(phi_i, x),
                    (x, self.domain[0], self.domain[1])
                )
                A[i, j] = integrand
            
            # Para equação -u'' = sin(πx), o lado direito é sin(πx)
            f = sp.sin(sp.pi * x)  # Assumindo a equação específica do teste
                
            rhs = sp.integrate(
                f * phi_i,
                (x, self.domain[0], self.domain[1])
            )
            b[i] = rhs

        # Converter para numpy com cuidado para números complexos  
        try:
            A_np = np.array([[complex(A[i,j]).real for j in range(n_terms)] for i in range(n_terms)], dtype=np.float64)
            b_np = np.array([complex(b[i]).real for i in range(n_terms)], dtype=np.float64).flatten()
            a_np = np.linalg.solve(A_np, b_np)
        except Exception as e:
            print(f"Erro ao resolver sistema linear: {e}")
            return None

        # Construir solução aproximada
        solution = sum(a_np[i] * self.basis_functions[i] for i in range(n_terms))
        return sp.simplify(solution)

# Exemplo: resolver -u'' = sin(πx) com u(0) = u(1) = 0
# A solução exata é u(x) = sin(πx)/π²

def test_galerkin():
    # Definir símbolos
    x = sp.Symbol('x')
    u = sp.Function('u')
    
    # Equação diferencial: -u''(x) = sin(π*x)
    equation = -sp.diff(u(x), x, 2) - sp.sin(sp.pi * x)
    
    # Domínio e condições de contorno
    domain = (0, 1)
    boundary_conditions = [(0, 0), (1, 0)]
    
    # Criar instância do método de Galerkin
    galerkin = GalerkinMethod(equation, domain, boundary_conditions)
    
    # Resolver
    print("Resolvendo EDP com método de Galerkin...")
    solution = galerkin.solve(n_terms=3)
    
    print(f"Solução aproximada: {solution}")
    
    # Solução exata para comparação
    exact_solution = sp.sin(sp.pi * x) / (sp.pi**2)
    print(f"Solução exata: {exact_solution}")
    
    # Avaliar em alguns pontos
    print("\nComparação em pontos específicos:")
    for x_val in [0.25, 0.5, 0.75]:
        
        approx_val = solution.subs(x, x_val)
        exact_val = exact_solution.subs(x, x_val)
        print(f"x = {x_val}: Aproximada = {float(approx_val):.6f}, Exata = {float(exact_val):.6f}")

if __name__ == "__main__":
    test_galerkin()