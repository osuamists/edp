from abc import ABC, abstractmethod
import sympy as sp 

class NumericalMethod(ABC):
    
    def __init__(self, equation, domain, boundary_conditions):
        """
        Classe base para métodos numéricos de solução de EDPs.
        """
        self.equation = equation
        self.domain = domain
        self.boundary_conditions = boundary_conditions
        self.basis_functions = []  # Será preenchido depois

    @abstractmethod
    def solve(self, n_terms=3, precision=1e-6):
        """
        Método principal que deve ser implementado por cada técnica.
        Deve retornar a solução aproximada.
        """
        pass

    @abstractmethod
    def generate_basis_functions(self, n_terms):
        """
        Gera as funções base usadas na aproximação (ex: polinômios, senos, etc).
        """
        pass