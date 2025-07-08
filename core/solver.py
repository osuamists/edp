import numpy as np
import sympy as sp
from .problems import EDPCatalog
from .boundary_conditions import BoundaryConditionManager
from .config import METHOD_COMPATIBILITY, DEFAULT_PARAMETERS, PROBLEM_VALIDATIONS

# Importações condicionais dos métodos
try:
    from .methods.galerkin_method import GalerkinMethod
except ImportError:
    GalerkinMethod = None

try:
    from .methods.colocacao_method import CollocationMethod as ColocacaoMethod
except ImportError:
    ColocacaoMethod = None

try:
    from .methods.least_squares_method import LeastSquaresMethod
except ImportError:
    LeastSquaresMethod = None

try:
    from .methods.rayleigh_ritz_method import RayleighRitzMethod
except ImportError:
    RayleighRitzMethod = None

try:
    from .methods.moments_method import MomentsMethod
except ImportError:
    MomentsMethod = None

try:
    from .methods.SubregionsMethod import SubregionsMethod
except ImportError:
    SubregionsMethod = None

class EDPSolver:
    """
    Classe principal que integra o catálogo de EDPs com os métodos numéricos
    """
    
    def __init__(self):
        self.catalog = EDPCatalog()
        self.bc_manager = BoundaryConditionManager()
        
        # Registrar apenas métodos disponíveis
        self.available_methods = {}
        
        if GalerkinMethod:
            self.available_methods["galerkin"] = GalerkinMethod
        if ColocacaoMethod:
            self.available_methods["colocacao"] = ColocacaoMethod
        if LeastSquaresMethod:
            self.available_methods["least_squares"] = LeastSquaresMethod
        if RayleighRitzMethod:
            self.available_methods["rayleigh_ritz"] = RayleighRitzMethod
        if MomentsMethod:
            self.available_methods["moments"] = MomentsMethod
        if SubregionsMethod:
            self.available_methods["subregions"] = SubregionsMethod
            
        self.current_problem = None
        self.current_method = None
        
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
    
    def list_problems(self):
        """Lista todos os problemas disponíveis"""
        return {key: value["nome"] for key, value in self.catalog.problems.items()}
    
    def list_methods(self):
        """Lista todos os métodos numéricos disponíveis"""
        return list(self.available_methods.keys())
    
    def solve(self, problem_name, method_name, **kwargs):
        """
        Resolve uma EDP específica usando um método numérico escolhido
        
        Args:
            problem_name: Nome do problema no catálogo
            method_name: Nome do método numérico
            **kwargs: Argumentos específicos do método (n_terms, precision, etc.)
        """
        # Define o problema
        problem = self.set_problem(problem_name)
        
        # Verifica se o método está disponível
        if method_name not in self.available_methods:
            raise ValueError(f"Método '{method_name}' não disponível. Métodos: {list(self.available_methods.keys())}")
        
        # Adapta o problema para o método escolhido
        adapted_problem = self._adapt_problem_for_method(problem, method_name)
        
        # Cria instância do método
        method_class = self.available_methods[method_name]
        method_instance = method_class(
            equation=adapted_problem["equation"],
            domain=adapted_problem["domain"],
            boundary_conditions=adapted_problem["boundary_conditions"]
        )
        
        # Resolve o problema
        solution = method_instance.solve(**kwargs)
        
        return {
            "problem": problem_name,
            "method": method_name,
            "solution": solution,
            "domain": problem["domain"],
            "boundary_conditions": problem["boundary_conditions"]
        }
    
    def _adapt_problem_for_method(self, problem, method_name):
        """
        Adapta a formulação do problema para o método específico
        """
        adapted = problem.copy()
        
        if method_name in ["galerkin", "least_squares", "rayleigh_ritz"]:
            # Estes métodos tipicamente trabalham com a forma -u'' = f(x)
            adapted["equation"] = self._extract_source_term(problem["equation"])
        
        elif method_name == "colocacao":
            # Método de colocação trabalha com a equação completa
            adapted["equation"] = problem["equation"]
        
        elif method_name == "moments":
            # Método dos momentos pode precisar de adaptação específica
            adapted["equation"] = problem["equation"]
        
        elif method_name == "subregions":
            # Método de sub-regiões pode dividir o domínio
            adapted["equation"] = problem["equation"]
        
        return adapted
    
    def _extract_source_term(self, equation):
        """
        Extrai o termo fonte de uma equação diferencial
        Para equações como -u'' + f(x) = 0, retorna f(x)
        """
        x = sp.Symbol('x')
        u = sp.Function('u')
        
        # Para Poisson: d²u/dx² + Q(x) = 0 -> retorna Q(x)
        # Isso é uma simplificação, pode precisar de lógica mais sofisticada
        
        if hasattr(equation, 'args'):
            # Se a equação tem argumentos, tenta extrair termos não derivativos
            for term in equation.args:
                if not term.has(sp.Derivative):
                    return term
        
        # Fallback: retorna a equação original
        return equation
    
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
                results[method] = {"error": str(e)}
        
        return results
    
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
        # Usando a compatibilidade definida nas configurações
        compatible_methods = METHOD_COMPATIBILITY.get(problem_name, [])
        
        # Filtra métodos disponíveis com base na compatibilidade e nos métodos disponíveis
        recommended = [method for method in compatible_methods if method in self.available_methods]
        
        return recommended or ["galerkin"]  # Retorna galerkin como padrão se não houver recomendação
