import sympy as sp
import numpy as np

class EDPCatalog:
    def __init__(self):
        # Removendo inicialização de símbolos SymPy do construtor
        # para evitar problemas de importação
        
        self.problems = {
            "poisson_1d": {
                "nome": "Equação de Poisson 1D",
                "domain": (0.01, 1),  # Evitando x=0 por causa de 1/x
                "boundary_conditions": [("dirichlet", 0.01, 0), ("dirichlet", 1, 0)],
                "analytical": None,  # Solução não trivial para Q(x)=1/x
                "source": lambda x: 1/x,  # Q(x) = 1/x, x ≠ 0
                "tipo": "eliptica_1d"
            },
            
            "heat_1d": {
                "nome": "Equação do Calor 1D", 
                "domain": (0, 1),  # L = 1 para simplificar
                "time_domain": (0, 0.1),
                "boundary_conditions": [
                    ("dirichlet", 0, 0), 
                    ("dirichlet", 1, 0),
                    ("initial", "u", lambda x: np.sin(3*np.pi/2 * x))  # f(x) = sin(3π/2L x) com L=1
                ],
                "analytical": lambda x, t: np.sin(3*np.pi/2 * x) * np.exp(-(3*np.pi/2)**2 * t),
                "tipo": "parabolica_1d"
            },
            
            "wave_1d": {
                "nome": "Equação da Onda 1D (Primeira Ordem)",
                "domain": (0, 1),
                "time_domain": (0, 1),
                "boundary_conditions": [
                    ("dirichlet", 0, 0),  # u(0,t) = 0
                    ("initial", "u", lambda x: 1)  # u(x,0) = 1
                ],
                "lambda_param": 4,  # λ² = 4
                "analytical": None,  # Equação de primeira ordem em t
                "tipo": "onda_primeira_ordem"
            },
            
            "helmholtz_2d": {
                "nome": "Equação de Helmholtz 2D",
                "domain": ((0, 1), (0, 0.25)),  # [0,1] × [0,1/4]
                "boundary_conditions": [
                    ("dirichlet", "x0", 0),  # φ(0,y) = 0
                    ("dirichlet", "y0", 0),  # φ(x,0) = 0
                    ("dirichlet", "x1", 0),  # φ(1,y) = 0
                    ("dirichlet", "y1", 0)   # φ(x,1/4) = 0
                ],
                "lambda_param": 1,  # λ em ∇²φ + λφ = 0
                "analytical": lambda x, y: np.sin(np.pi * x) * np.sin(4 * np.pi * y),  # Solução de separação de variáveis
                "tipo": "eliptica_2d"
            }
        }
    
    def get_problem(self, name):
        return self.problems[name]
    
    def get_all_problems(self):
        return self.problems
