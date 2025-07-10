from .numerical_method import NumericalMethod
from .galerkin_method import GalerkinMethod
from .rayleigh_ritz_method import RayleighRitzMethod
# Métodos especializados para o trabalho final
from .wave_method import WaveGalerkinMethod
from .heat_method import HeatGalerkinMethod
from .helmholtz_2d_method import Helmholtz2DMethod

__all__ = [
    'NumericalMethod',
    'GalerkinMethod', 
    'RayleighRitzMethod',
    'WaveGalerkinMethod',
    'HeatGalerkinMethod',
    'Helmholtz2DMethod'
]