import sympy as sp
import numpy as np
# Certifique-se de que a importação de NumericalMethod está correta
# Se NumericalMethod estiver em um arquivo chamado numerical_method.py na mesma pasta, use:
# from numerical_method import NumericalMethod 
# Se estiver na pasta pai, como antes:
from .numerical_method import NumericalMethod

class GalerkinMethod(NumericalMethod):
    """
    Implementa o método de Galerkin para resolver EDOs de segunda ordem
    na forma -u''(x) = f(x) com condições de contorno u(a)=0, u(b)=0.
    """
    
    def generate_basis_functions(self, n_terms):
        """
        Gera funções de base polinomiais que satisfazem u(a)=0 e u(b)=0.
        Exemplo para domínio (0, 1): x*(1-x), x^2*(1-x), ...
        """
        x = sp.Symbol('x')
        a, b = self.domain
        # Forma geral para um domínio (a, b)
        self.basis_functions = [(x - a)**n * (b - x) for n in range(1, n_terms + 1)]

    def solve(self, n_terms=3):
        """
        Monta e resolve o sistema linear A*c = b para os coeficientes da solução.
        """
        # Garante que as funções de base sejam geradas
        self.generate_basis_functions(n_terms)
        
        x = sp.Symbol('x')
        
        # O método espera que self.equation seja apenas o lado direito f(x)
        # Ex: f_x = sp.pi**2 * sp.sin(sp.pi * x)
        f_x = self.equation

        # Inicializa a matriz A e o vetor b com zeros
        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        # Monta a matriz A e o vetor b
        for i in range(n_terms):
            phi_i = self.basis_functions[i]
            
            # Calcula o elemento do vetor b
            # b_i = integral(f(x) * phi_i(x) dx)
            integrand_b = f_x * phi_i
            b[i] = sp.integrate(integrand_b, (x, self.domain[0], self.domain[1]))
            
            # Calcula a linha da matriz A
            # A_ij = integral(phi_j'(x) * phi_i'(x) dx)
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                integrand_A = sp.diff(phi_j, x) * sp.diff(phi_i, x)
                A[i, j] = sp.integrate(integrand_A, (x, self.domain[0], self.domain[1]))

        # Converte as matrizes simbólicas para NumPy para resolver o sistema
        # O método .tolist() e np.float64 garantem a conversão correta
        try:
            A_np = np.array(A.tolist()).astype(np.float64)
            b_np = np.array(b.tolist()).astype(np.float64).flatten() # .flatten() para garantir que b seja um vetor 1D
        except TypeError:
            print("ERRO: Não foi possível converter a matriz A ou o vetor b para valores numéricos.")
            print("Isso geralmente acontece se a integral não pôde ser resolvida simbolicamente.")
            print("Vetor b simbólico:", b)
            return None # Retorna None em caso de falha

        # Resolve o sistema linear A*c = b para encontrar os coeficientes c
        try:
            coeffs = np.linalg.solve(A_np, b_np)
        except np.linalg.LinAlgError:
            print("ERRO: A matriz A é singular e o sistema não pode ser resolvido.")
            return None

        # Constrói a solução aproximada final
        solution = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))
        
        return sp.simplify(solution)