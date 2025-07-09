import numpy as np
import sympy as sp

class EDPCatalog:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.t = sp.Symbol('t')
        self.u = sp.Function('u')
        
        self.problems = {
            "poisson": {
                "nome": "Poisson",
                # CORREÇÃO: Trocar Q(x) por função específica
                "equation": sp.Eq(sp.diff(self.u(self.x), self.x, 2), -sp.pi**2 * sp.sin(sp.pi * self.x)),
                "domain": (0, 1),
                "boundary_conditions": [("dirichlet", 0, 0), ("dirichlet", 1, 0)],
                "analytical": lambda x: sp.sin(sp.pi * x)  # Solução analítica conhecida
            },
            "onda_1d": {
                "nome": "Onda 1D",
                "equation": sp.Eq(sp.diff(self.u(self.x, self.t), self.t, 2), 4*sp.diff(self.u(self.x, self.t), self.x, 2)),
                "domain": (0, 1),
                "boundary_conditions": [
                    ("dirichlet", 0, 0), ("dirichlet", 1, 0),
                    ("initial", "u", lambda x: 0),
                    ("initial", "ut", lambda x: 0)
                ],
                "analytical": lambda x, t: None
            },
            "calor": {
                "nome": "Calor 1D",
                "equation": sp.Eq(sp.diff(self.u(self.x, self.t), self.t), sp.diff(self.u(self.x, self.t), self.x, 2)),
                "domain": (0, 1.0),
                "boundary_conditions": [
                    ("dirichlet", 0, 0), ("dirichlet", 1.0, 0),
                    ("initial", "u", lambda x: 3*sp.sin(2*sp.pi*x))
                ],
                "analytical": lambda x, t: None
            },
            "helmholtz": {
                "nome": "Helmholtz 2D",
                "equation": sp.Eq(sp.diff(self.u(self.x, self.y), self.x, 2) + sp.diff(self.u(self.x, self.y), self.y, 2) + 4*self.u(self.x, self.y), 0),
                "domain": ((0, 1), (0, 1)),
                "boundary_conditions": [("dirichlet", 0, 0), ("dirichlet", 1, 0)],
                "analytical": lambda x, y: None
            },
            "test_problem": {
                "nome": "Problema Teste u'' + u = π²sin(πx)",
                "equation": sp.Eq(sp.diff(self.u(self.x), self.x, 2) + self.u(self.x), sp.pi**2 * sp.sin(sp.pi * self.x)),
                "domain": (0, 1),
                "boundary_conditions": [("dirichlet", 0, 0), ("dirichlet", 1, 0)],
                "analytical": lambda x: sp.sin(sp.pi * x)
            }
        }

    def get_problem(self, problem_name):
        """Retornar problema específico"""
        if problem_name in self.problems:
            return self.problems[problem_name]
        else:
            raise ValueError(f"Problema '{problem_name}' não encontrado. Disponíveis: {list(self.problems.keys())}")

    def list_problems(self):
        """Listar todos os problemas disponíveis"""
        for name, problem in self.problems.items():
            print(f"{name}: {problem['nome']}")
            print(f"  Equação: {problem['equation']}")
            print(f"  Domínio: {problem['domain']}")
            print()

