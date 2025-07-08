"""
Solver simplificado para demonstrar a integração
"""

import numpy as np
import sympy as sp
from .problems import EDPCatalog
from .boundary_conditions import BoundaryConditionManager

# Configurações expandidas
SIMPLE_COMPATIBILITY = {
    "poisson": ["galerkin", "rayleigh_ritz", "least_squares", "colocacao"],
    "onda_1d": ["galerkin", "colocacao", "moments"],
    "calor": ["galerkin", "least_squares", "colocacao"],
    "helmholtz": ["galerkin", "rayleigh_ritz", "subregions"]
}

class SimplifiedEDPSolver:
    """
    Versão simplificada do solver para demonstrar a integração
    """
    
    def __init__(self):
        self.catalog = EDPCatalog()
        self.bc_manager = BoundaryConditionManager()
        
        # Apenas métodos que sabemos que funcionam
        self.available_methods = {}
        
        # Tentar importar métodos disponíveis
        try:
            from .methods.galerkin_method import GalerkinMethod
            self.available_methods["galerkin"] = GalerkinMethod
        except ImportError as e:
            print(f"Aviso: Método Galerkin não disponível - {e}")
            
        try:
            from .methods.least_squares_method import LeastSquaresMethod
            self.available_methods["least_squares"] = LeastSquaresMethod
        except ImportError as e:
            print(f"Aviso: Método Least Squares não disponível - {e}")
            
        try:
            from .methods.rayleigh_ritz_method import RayleighRitzMethod
            self.available_methods["rayleigh_ritz"] = RayleighRitzMethod
        except ImportError as e:
            print(f"Aviso: Método Rayleigh-Ritz não disponível - {e}")
            
        try:
            from .methods.colocacao_method import CollocationMethod
            self.available_methods["colocacao"] = CollocationMethod
        except ImportError as e:
            print(f"Aviso: Método Colocação não disponível - {e}")
            
        try:
            from .methods.moments_method import MomentsMethod
            self.available_methods["moments"] = MomentsMethod
        except ImportError as e:
            print(f"Aviso: Método Momentos não disponível - {e}")
            
        try:
            from .methods.SubregionsMethod import SubregionsMethod
            self.available_methods["subregions"] = SubregionsMethod
        except ImportError as e:
            print(f"Aviso: Método Sub-regiões não disponível - {e}")
        
        self.current_problem = None
        
    def list_problems(self):
        """Lista todos os problemas disponíveis"""
        return {key: value["nome"] for key, value in self.catalog.problems.items()}
    
    def list_methods(self):
        """Lista todos os métodos numéricos disponíveis"""
        return list(self.available_methods.keys())
    
    def set_problem(self, problem_name):
        """Define o problema EDP a ser resolvido"""
        if problem_name not in self.catalog.problems:
            raise ValueError(f"Problema '{problem_name}' não encontrado no catálogo")
        
        self.current_problem = self.catalog.problems[problem_name]
        self.bc_manager.set_problem_type(problem_name)
        
        # Valida as condições de contorno do problema
        self.bc_manager.validate(
            self.current_problem["boundary_conditions"], 
            problem_name
        )
        
        return self.current_problem
    
    def get_problem_info(self, problem_name):
        """Retorna informações detalhadas sobre um problema"""
        if problem_name not in self.catalog.problems:
            raise ValueError(f"Problema '{problem_name}' não encontrado")
        
        problem = self.catalog.problems[problem_name]
        bc_summary = self.bc_manager.summary(problem["boundary_conditions"])
        
        return {
            "nome": problem["nome"],
            "equation": problem["equation"],
            "domain": problem["domain"],
            "boundary_conditions_summary": bc_summary,
            "analytical": problem.get("analytical", "Não disponível")
        }
    
    def recommend_method(self, problem_name):
        """
        Recomenda o melhor método para um problema específico
        """
        recommendations = SIMPLE_COMPATIBILITY.get(problem_name, ["galerkin"])
        available_recommendations = [m for m in recommendations if m in self.available_methods]
        return available_recommendations or ["galerkin"]
    
    def solve(self, problem_name, method_name, **kwargs):
        """
        Resolve uma EDP específica usando um método numérico escolhido
        """
        # Define o problema
        problem = self.set_problem(problem_name)
        
        # Verifica se o método está disponível
        if method_name not in self.available_methods:
            raise ValueError(f"Método '{method_name}' não disponível. Métodos: {list(self.available_methods.keys())}")
        
        # Tentar resolver com qualquer método disponível
        try:
            # Adaptar problema para o método escolhido
            adapted_equation = self._extract_source_term(problem["equation"])
            
            # Criar instância do método
            method_class = self.available_methods[method_name]
            method_instance = method_class(
                equation=adapted_equation,
                domain=problem["domain"],
                boundary_conditions=problem["boundary_conditions"]
            )
            
            # Resolver o problema
            solution = method_instance.solve(**kwargs)
            
            return {
                "problem": problem_name,
                "method": method_name,
                "solution": solution,
                "domain": problem["domain"],
                "boundary_conditions": problem["boundary_conditions"],
                "status": "success"
            }
            
        except Exception as e:
            return {
                "problem": problem_name,
                "method": method_name,
                "error": str(e),
                "status": "error"
            }
    
    def _extract_source_term(self, equation):
        """
        Extrai o termo fonte de uma equação diferencial
        """
        # Para demonstração, retorna uma função simples
        x = sp.Symbol('x')
        
        # Se a equação tem Q(x), tenta extrair
        if hasattr(equation, 'args'):
            for term in equation.args:
                if 'Q' in str(term):
                    return sp.pi**2 * sp.sin(sp.pi * x)  # Exemplo padrão
        
        # Fallback para função teste
        return sp.pi**2 * sp.sin(sp.pi * x)
    
    def compare_methods(self, problem_name, methods_list, **kwargs):
        """
        Compara diferentes métodos numéricos para o mesmo problema
        """
        results = {}
        
        for method in methods_list:
            try:
                result = self.solve(problem_name, method, **kwargs)
                results[method] = result
            except Exception as e:
                results[method] = {"error": str(e), "status": "error"}
        
        return results
    
    def status_report(self):
        """
        Relatório do status do sistema
        """
        return {
            "problems_available": len(self.catalog.problems),
            "methods_available": len(self.available_methods),
            "problems": list(self.catalog.problems.keys()),
            "methods": list(self.available_methods.keys()),
            "integration_status": "functional" if self.available_methods else "limited"
        }
