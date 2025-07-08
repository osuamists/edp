import numpy as np
import sympy as sp

class EDPCatalog:
     def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.t = sp.Symbol('t')
        self.u = sp.Function('u')
        Q = sp.Function('Q')
        L = sp.Symbol('L', positive=True)
        self.problems = {
            "poisson": {
                "nome": "Poisson",
                "equation": sp.diff(self.u(self.x), self.x, 2) + Q(self.x),
                "domain": (0, 1),
                "boundary_conditions": [("dirichlet", 0, 0), ("dirichlet", 1, 0)],
                "analytical": lambda x: None # se conhecida
            },
            "onda_1d": {
                "nome": "Onda 1D",
                "equation": sp.diff(self.u(self.x, self.t), self.t, 2) - 4*sp.diff(self.u(self.x, self.t), self.x, 2),
                "domain": (0, 1),
                "boundary_conditions": [
                    ("dirichlet", 0, 0), ("dirichlet", 1, 0),
                    ("initial", "u", lambda x: 0), # condição inicial para u(x,0)
                    ("initial", "ut", lambda x: 0) # condição inicial para ∂u/∂t(x,0)
                ],
                "analytical": lambda x, t: None # se conhecida
            },
            "calor": {
                "nome": "Calor 1D",
                "equation": sp.diff(self.u(self.x, self.t), self.t) - sp.diff(self.u(self.x, self.t), self.x, 2),
                "domain": (0, L),
                "boundary_conditions": [
                    ("dirichlet", 0, 0), ("dirichlet", L, 0),
                    ("initial", "u", lambda x: 3*sp.sin(2*sp.pi*x/L)) # exemplo
                ],
                "analytical": lambda x, t: None # se conhecida
            },
            "helmholtz": {
                "nome": "Helmholtz 2D",
                "equation": sp.diff(self.u(self.x, self.y), self.x, 2) + sp.diff(self.u(self.x, self.y), self.y, 2) + 4*self.u(self.x, self.y),
                "domain": ((0, 1), (0, 1)),
                "boundary_conditions": [
                    ("dirichlet", 0, 0), ("dirichlet", 1, 0)
                ],
                "analytical": lambda x, y: None # se conhecida
            }
        }

