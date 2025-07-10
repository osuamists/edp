"""
Módulo principal para resolução de Equações Diferenciais Parciais (EDPs)
"""

__version__ = "1.0.0"
__author__ = "EDP Solver Team"

from .problems import EDPCatalog
from .comparator import EDPComparator

__all__ = ['EDPCatalog', 'EDPComparator']
