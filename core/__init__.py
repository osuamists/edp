"""
Core module for EDP (Equações Diferenciais Parciais) solver.
Focused on solving 4 specific PDEs using Galerkin method with convergence analysis.
"""

__version__ = "2.0.0"
__author__ = "EDP Solver Team"

from .problems import EDPCatalog
from .galerkin_solver import GalerkinSolver
from .convergence_analyzer import ConvergenceAnalyzer

__all__ = ['EDPCatalog', 'GalerkinSolver', 'ConvergenceAnalyzer']
