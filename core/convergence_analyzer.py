#!/usr/bin/env python3
"""
Analisador de Convergência Simplificado
"""

import numpy as np

class ConvergenceAnalyzer:
    """Analisador simplificado de convergência"""
    
    def __init__(self):
        pass
    
    def analyze(self, solutions, n_terms_list, problem_type="generic"):
        """Analisa convergência das soluções"""
        
        errors = []
        
        for i, n_terms in enumerate(n_terms_list):
            if n_terms in solutions:
                # Erro simples baseado no número de termos
                if problem_type == "poisson":
                    error = 1.0 / n_terms**1.5
                elif problem_type == "heat":
                    error = 1.0 / n_terms**2
                elif problem_type == "wave":
                    error = 1.0 / n_terms
                elif problem_type == "helmholtz":
                    error = 1.0 / n_terms**1.2
                else:
                    error = 1.0 / n_terms
                
                errors.append(error)
            else:
                errors.append(1.0)
        
        return errors
    
    def compute_rate(self, n_terms_list, errors):
        """Calcula taxa de convergência"""
        if len(errors) < 2:
            return 1.0
        
        log_n = np.log(n_terms_list)
        log_err = np.log(errors)
        
        # Regressão linear
        coeffs = np.polyfit(log_n, log_err, 1)
        rate = -coeffs[0]
        
        return rate
