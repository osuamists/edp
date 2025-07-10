import numpy as np
import sympy as sp

class EDPCatalog:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.t = sp.Symbol('t')
        self.u = sp.Function('u')
        
        self.problems = {
            # Problema 1: Equação de Poisson
            "poisson_trabalho": {
                "nome": "1. Equação de Poisson",
                "equation": sp.Integer(-1),  # Q(x) = -1
                "full_equation": sp.Eq(sp.diff(self.u(self.x), self.x, 2), -1),
                "domain": (0, 1),
                "boundary_conditions": [("dirichlet", 0, 0), ("dirichlet", 1, 0)],
                "analytical": self.x * (1 - self.x) / 2,  # Solução: x(1-x)/2
                "description": "∂²Ω/∂x² = Q(x), Q(x) = -1",
                "tipo": "eliptica"
            },
            
            # Problema 2: Equação da Onda 1D
            "onda_trabalho": {
                "nome": "2. Equação da Onda unidimensional", 
                "equation": sp.Eq(sp.diff(self.u(self.x, self.t), self.t), 4*sp.diff(self.u(self.x, self.t), self.x, 2)),
                "full_equation": sp.Eq(sp.diff(self.u(self.x, self.t), self.t), 4*sp.diff(self.u(self.x, self.t), self.x, 2)),
                "domain": (0, 1),
                "boundary_conditions": [
                    ("dirichlet", 0, 0),  # u(0,t) = 0
                    ("initial", "u", 1)   # u(x,0) = 1
                ],
                "analytical": None,  # Solução depende do tempo
                "description": "∂u/∂t = λ²∂²u/∂x², λ² = 4",
                "tipo": "hiperbolica",
                "lambda": 4
            },
            
            # Problema 3: Equação do Calor
            "calor_trabalho": {
                "nome": "3. Equação do Calor",
                "equation": sp.Eq(sp.diff(self.u(self.x, self.t), self.t), sp.diff(self.u(self.x, self.t), self.x, 2)),
                "full_equation": sp.Eq(sp.diff(self.u(self.x, self.t), self.t), sp.diff(self.u(self.x, self.t), self.x, 2)),
                "domain": (0, 1),  # Assumindo L = 1
                "boundary_conditions": [
                    ("dirichlet", 0, 0),  # u(0,t) = 0
                    ("dirichlet", 1, 0),  # u(L,t) = 0 
                    ("initial", "u", sp.sin(3*sp.pi*self.x/2))  # u(x,0) = sin(3πx/2L)
                ],
                "analytical": None,  # Solução depende do tempo
                "description": "∂u/∂t = ∂²u/∂x², f(x) = sin(3πx/2L)",
                "tipo": "parabolica"
            },
            
            # Problema 4: Equação de Helmholtz 2D
            "helmholtz_trabalho": {
                "nome": "4. Equação de Helmholtz",
                "equation": sp.Eq(sp.diff(self.u(self.x, self.y), self.x, 2) + sp.diff(self.u(self.x, self.y), self.y, 2) + sp.Symbol('lambda')*self.u(self.x, self.y), 0),
                "full_equation": sp.Eq(sp.diff(self.u(self.x, self.y), self.x, 2) + sp.diff(self.u(self.x, self.y), self.y, 2) + sp.Symbol('lambda')*self.u(self.x, self.y), 0),
                "domain": ((0, 1), (0, sp.Symbol('gamma'))),  # [0,1] × [0,γ]
                "boundary_conditions": [
                    ("dirichlet", (0, "y"), 0),  # φ(0,y) = 0
                    ("dirichlet", ("x", 0), 0),  # φ(x,0) = 0
                    ("dirichlet", (1, "y"), 0),  # φ(1,y) = 0
                    ("dirichlet", ("x", "gamma/4"), 0)  # φ(x,γ/4) = 0
                ],
                "analytical": None,  # Solução complexa
                "description": "∂²φ/∂x² + ∂²φ/∂y² + λφ = 0",
                "tipo": "eliptica_2d"
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

