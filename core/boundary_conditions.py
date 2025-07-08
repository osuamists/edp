import numpy as np
import sympy as sp

class BoundaryConditionManager:
    def __init__(self):
        self.supported_types = ["dirichlet", "neumann", "initial", "robin", "periodic"]
        self.problem_type = None
        
    def set_problem_type(self, problem_type):
        """Define o tipo de problema para validações específicas"""
        self.problem_type = problem_type
    
    def validate(self, conditions, problem_type=None):
        """Valida condições de contorno baseado no tipo de problema"""
        if problem_type:
            self.problem_type = problem_type
            
        if self.problem_type == "poisson":
            return self._validate_poisson(conditions)
        elif self.problem_type == "onda_1d":
            return self._validate_wave_1d(conditions)
        elif self.problem_type == "calor":
            return self._validate_heat_1d(conditions)
        elif self.problem_type == "helmholtz":
            return self._validate_helmholtz_2d(conditions)
        else:
            return self._validate_generic(conditions)
    
    def _validate_generic(self, conditions):
        """Validação genérica para qualquer tipo de condição"""
        points = {}
        for cond_type, point, value in conditions:
            if cond_type not in self.supported_types:
                raise ValueError(f"Tipo de condição '{cond_type}' não suportado.")
            if (cond_type != "initial") and (point in points):
                raise ValueError(f"Conflito de condições no ponto {point}")
            points[point] = cond_type
        return True
    
    def _validate_poisson(self, conditions):
        """Validação específica para equação de Poisson"""
        boundary_points = []
        
        for cond_type, point, value in conditions:
            if cond_type not in ["dirichlet", "neumann", "robin"]:
                raise ValueError(f"Equação de Poisson não aceita condições do tipo '{cond_type}'")
            boundary_points.append(point)
        
        # Verificar se há condições suficientes nas fronteiras
        if len(set(boundary_points)) < 2:
            raise ValueError("Equação de Poisson requer condições em pelo menos 2 pontos de fronteira")
        
        return True
    
    def _validate_wave_1d(self, conditions):
        """Validação específica para equação da onda 1D"""
        has_boundary = False
        has_initial_u = False
        has_initial_ut = False
        
        for cond_type, point, value in conditions:
            if cond_type in ["dirichlet", "neumann"]:
                has_boundary = True
            elif cond_type == "initial":
                if point == "u":
                    has_initial_u = True
                elif point == "ut":
                    has_initial_ut = True
        
        if not has_boundary:
            raise ValueError("Equação da onda requer condições de fronteira espaciais")
        if not has_initial_u:
            raise ValueError("Equação da onda requer condição inicial para u(x,0)")
        if not has_initial_ut:
            raise ValueError("Equação da onda requer condição inicial para ∂u/∂t(x,0)")
        
        return True
    
    def _validate_heat_1d(self, conditions):
        """Validação específica para equação do calor 1D"""
        has_boundary = False
        has_initial = False
        
        for cond_type, point, value in conditions:
            if cond_type in ["dirichlet", "neumann"]:
                has_boundary = True
            elif cond_type == "initial" and point == "u":
                has_initial = True
        
        if not has_boundary:
            raise ValueError("Equação do calor requer condições de fronteira espaciais")
        if not has_initial:
            raise ValueError("Equação do calor requer condição inicial para u(x,0)")
        
        return True
    
    def _validate_helmholtz_2d(self, conditions):
        """Validação específica para equação de Helmholtz 2D"""
        for cond_type, point, value in conditions:
            if cond_type not in ["dirichlet", "neumann", "robin"]:
                raise ValueError(f"Equação de Helmholtz 2D não aceita condições do tipo '{cond_type}'")
        
        # Para 2D, precisamos de condições em todo o contorno
        if len(conditions) < 2:
            raise ValueError("Equação de Helmholtz 2D requer condições de fronteira adequadas")
        
        return True
    
    def apply_dirichlet(self, matrix, rhs, boundary_points, boundary_values):
        """Aplica condições de Dirichlet ao sistema linear"""
        for i, point in enumerate(boundary_points):
            if isinstance(point, (int, float)):
                # Para 1D
                matrix[point, :] = 0
                matrix[point, point] = 1
                rhs[point] = boundary_values[i]
        return matrix, rhs
    
    def apply_neumann(self, matrix, rhs, boundary_points, boundary_values, dx):
        """Aplica condições de Neumann ao sistema linear"""
        for i, point in enumerate(boundary_points):
            if point == 0:  # Fronteira esquerda
                matrix[point, point] = -1/dx
                matrix[point, point+1] = 1/dx
                rhs[point] = boundary_values[i]
            elif point == matrix.shape[0]-1:  # Fronteira direita
                matrix[point, point-1] = -1/dx
                matrix[point, point] = 1/dx
                rhs[point] = boundary_values[i]
        return matrix, rhs
    
    def get_initial_conditions(self, conditions, x_grid):
        """Extrai e avalia condições iniciais"""
        initial_u = None
        initial_ut = None
        
        for cond_type, point, value in conditions:
            if cond_type == "initial":
                if point == "u":
                    if callable(value):
                        initial_u = np.array([value(x) for x in x_grid])
                    else:
                        initial_u = np.full_like(x_grid, value)
                elif point == "ut":
                    if callable(value):
                        initial_ut = np.array([value(x) for x in x_grid])
                    else:
                        initial_ut = np.full_like(x_grid, value)
        
        return initial_u, initial_ut
    
    def summary(self, conditions):
        """Retorna um resumo das condições de contorno"""
        summary = {
            "dirichlet": [],
            "neumann": [],
            "initial": [],
            "robin": [],
            "periodic": []
        }
        
        for cond_type, point, value in conditions:
            summary[cond_type].append((point, value))
        
        return summary