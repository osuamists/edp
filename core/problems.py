import sympy as sp
import numpy as np

class EDPCatalog:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y') 
        self.t = sp.Symbol('t')
        self.u = sp.Function('u')
        
        self.problems = {
            "poisson_1d": {
                "nome": "Equação de Poisson 1D",
                "domain": (0, 1),
                "boundary_conditions": [("dirichlet", 0, 0), ("dirichlet", 1, 0)],
                "analytical": lambda x: x * (1 - x),  # Solução não trivial
                "source": lambda x: 2,  # Função fonte constante
                "tipo": "eliptica_1d"
            },
            
            "heat_1d": {
                "nome": "Equação do Calor 1D", 
                "domain": (0, 1),
                "time_domain": (0, 0.1),
                "boundary_conditions": [
                    ("dirichlet", 0, 0), 
                    ("dirichlet", 1, 0),
                    ("initial", "u", lambda x: x * (1 - x))  # Condição inicial não trivial
                ],
                "analytical": lambda x, t: x * (1 - x) * np.exp(-np.pi**2 * t),  # Aproximação
                "tipo": "parabolica_1d"
            },
            
            "wave_1d": {
                "nome": "Equação da Onda 1D",
                "domain": (0, 1),
                "time_domain": (0, 1),
                "boundary_conditions": [
                    ("dirichlet", 0, 0),
                    ("dirichlet", 1, 0), 
                    ("initial", "u", lambda x: np.sin(np.pi*x)),
                    ("initial", "ut", lambda x: 0)
                ],
                "analytical": lambda x, t: np.sin(np.pi*x)*np.cos(2*np.pi*t),
                "tipo": "hiperbolica_1d"
            },
            
            "helmholtz_2d": {
                "nome": "Equação de Helmholtz 2D",
                "domain": ((0, 1), (0, 1)),
                "boundary_conditions": [
                    ("dirichlet", "x0", 0), ("dirichlet", "x1", 0),
                    ("dirichlet", "y0", 0), ("dirichlet", "y1", lambda x: np.sin(np.pi*x))
                ],
                "analytical": lambda x, y: np.sin(np.pi*x)*np.sinh(np.sqrt(np.pi**2 + 4)*y)/np.sinh(np.sqrt(np.pi**2 + 4)),
                "tipo": "eliptica_2d"
            }
        }
    
    def get_problem(self, name):
        return self.problems[name]
    
    def get_all_problems(self):
        return self.problems
