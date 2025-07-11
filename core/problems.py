import sympy as sp
import numpy as np

class EDPCatalog:
    def __init__(self):
        # Removendo inicialização de símbolos SymPy do construtor
        # para evitar problemas de importação
        
        self.problems = {
            "poisson_1d": {
                "nome": "Equação de Poisson 1D",
                "domain": (0, 1),  # Alterado conforme imagem
                "boundary_conditions": [("dirichlet", 0, 0), ("dirichlet", 1, 0)],
                "analytical": None,  
                "source": lambda x: 1/x if x > 1e-10 else 1e10,  # Q(x) = 1/x com tratamento para x=0
                "tipo": "eliptica_1d"
            },
            
            "heat_1d": {
                "nome": "Equação do Calor 1D", 
                "domain": (0, 1),  
                "time_domain": (0, 0.1),
                "boundary_conditions": [
                    ("dirichlet", 0, 0), 
                    ("dirichlet", 1, 0),
                    ("initial", "u", lambda x: np.sin(3*np.pi/2 * x))  # u(x,0) = sin(3πx/2L) com L=1
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
                    ("initial", "u", lambda x: 1)  # u(x,0) = 1 conforme imagem
                ],
                "lambda_param": 4,  # λ² = 4
                "analytical": None,
                "tipo": "onda_primeira_ordem"
            },
            
            "helmholtz_2d": {
                "nome": "Equação de Helmholtz 2D",
                "domain": ((0, 1), (0, 1)),  # Domínio alterado para y ∈ [0,1] conforme imagem
                "boundary_conditions": [
                    ("dirichlet", "x0", 0),  # φ(0,y) = 0
                    ("dirichlet", "y0", 0),  # φ(x,0) = 0
                    ("dirichlet", "x1", 0),  # φ(1,y) = 0
                    ("neumann", "y1", 0)     # ∂φ/∂y(x,2) = 0 conforme imagem
                ],
                "lambda_param": 1,  
                "analytical": lambda x, y: np.sin(np.pi * x) * np.sin(np.pi * y),
                "tipo": "eliptica_2d"
            }
        }
    
    def get_problem(self, name):
        return self.problems[name]
    
    def get_all_problems(self):
        return self.problems
