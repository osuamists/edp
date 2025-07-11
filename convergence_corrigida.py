#!/usr/bin/env python3
"""
ANÁLISE DE CONVERGÊNCIA CORRIGIDA
Script corrigido para análise de convergência dos métodos implementados
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def convergencia_poisson_corrigida():
    """
    Análise de convergência corrigida para a equação de Poisson.
    """
    print("="*60)
    print("ANÁLISE DE CONVERGÊNCIA CORRIGIDA: Equação de Poisson")
    print("∂²Ω/∂x² = Q(x), Q(x) = -1")
    print("="*60)
    
    from core.methods.galerkin_method import GalerkinMethod
    
    # Variação do número de termos
    n_terms_list = range(2, 11)
    errors_galerkin = []
    
    # Solução analítica: x(1-x)/2
    x_test = np.linspace(0.1, 0.9, 20)
    analytical_values = x_test * (1 - x_test) / 2
    
    for n_terms in n_terms_list:
        try:
            # Usar método diretamente
            method = GalerkinMethod(
                equation=sp.Integer(1),  # -u'' = 1
                domain=(0, 1),
                boundary_conditions=[(0, 0), (1, 0)]
            )
            
            solution = method.solve(n_terms=n_terms)
            
            if solution is not None:
                # Avaliar numericamente
                x_sym = sp.Symbol('x')
                numerical_values = []
                for x_val in x_test:
                    try:
                        val = float(solution.subs(x_sym, x_val))
                        numerical_values.append(val)
                    except:
                        numerical_values.append(0)
                
                # Calcular erro máximo
                error = np.max(np.abs(np.array(numerical_values) - analytical_values))
                errors_galerkin.append(error)
                print(f"n={n_terms}: Erro Galerkin={error:.2e}")
            else:
                errors_galerkin.append(np.nan)
                print(f"n={n_terms}: Erro - método retornou None")
            
        except Exception as e:
            print(f"Erro com {n_terms} termos: {e}")
            errors_galerkin.append(np.nan)
    
    # Plot da convergência
    plt.figure(figsize=(10, 6))
    valid_indices = ~np.isnan(errors_galerkin)
    if np.any(valid_indices):
        plt.semilogy(np.array(n_terms_list)[valid_indices], 
                     np.array(errors_galerkin)[valid_indices], 
                     'b-o', linewidth=2, label='Galerkin')
        plt.xlabel('Número de Termos')
        plt.ylabel('Erro Máximo')
        plt.title('Convergência - Equação de Poisson (Corrigida)')
        plt.grid(True)
        plt.legend()
        plt.savefig('output/convergence_poisson_corrigida.png', dpi=300, bbox_inches='tight')
        print("Gráfico salvo: output/convergence_poisson_corrigida.png")
    else:
        print("❌ Não foi possível gerar gráfico - todos os valores são NaN")

def convergencia_calor_corrigida():
    """
    Análise de convergência para a equação do calor.
    """
    print("\n" + "="*60)
    print("ANÁLISE DE CONVERGÊNCIA: Equação do Calor")
    print("∂u/∂t = ∂²u/∂x²")
    print("="*60)
    
    from core.methods.heat_method import HeatGalerkinMethod
    
    n_terms_list = range(3, 11)
    decay_rates = []
    
    for n_terms in n_terms_list:
        try:
            method = HeatGalerkinMethod(
                domain=(0, 1),
                boundary_conditions=[("dirichlet", 0, 0), ("dirichlet", 1, 0)]
            )
            
            # Obter taxas de decaimento
            rates = method.get_decay_rate(n_terms=n_terms)
            first_rate = rates[0] if rates else 0
            decay_rates.append(first_rate)
            
            print(f"n={n_terms}: Taxa_decaimento_1={first_rate:.4f}")
            
        except Exception as e:
            print(f"Erro com {n_terms} termos: {e}")
            decay_rates.append(np.nan)
    
    # Plot
    plt.figure(figsize=(10, 6))
    valid_indices = ~np.isnan(decay_rates)
    if np.any(valid_indices):
        plt.plot(np.array(n_terms_list)[valid_indices], 
                 np.array(decay_rates)[valid_indices], 
                 'r-s', linewidth=2, label='Taxa de Decaimento (1º Modo)')
        plt.xlabel('Número de Termos')
        plt.ylabel('Taxa de Decaimento')
        plt.title('Convergência - Equação do Calor')
        plt.grid(True)
        plt.legend()
        plt.savefig('output/convergence_heat_corrigida.png', dpi=300, bbox_inches='tight')
        print("Gráfico salvo: output/convergence_heat_corrigida.png")

def convergencia_helmholtz_corrigida():
    """
    Análise de convergência para Helmholtz 2D.
    """
    print("\n" + "="*60)
    print("ANÁLISE DE CONVERGÊNCIA: Helmholtz 2D")
    print("∂²φ/∂x² + ∂²φ/∂y² + λφ = 0")
    print("="*60)
    
    from core.methods.helmholtz_2d_method import Helmholtz2DMethod
    
    n_terms_list = range(2, 6)
    first_eigenvalues = []
    
    for n_terms in n_terms_list:
        try:
            method = Helmholtz2DMethod(
                domain=((0, 1), (0, 1)),
                boundary_conditions=[]
            )
            
            eigenvalues = method.calculate_eigenvalues(n_terms_x=n_terms, n_terms_y=n_terms)
            
            # Primeiro autovalor (menor)
            eigenvalue_list = list(eigenvalues.values())
            if eigenvalue_list:
                first_eigenval = float(min(eigenvalue_list))
                first_eigenvalues.append(first_eigenval)
                print(f"n={n_terms}x{n_terms}: 1º_eigenvalue={first_eigenval:.4f}")
            else:
                first_eigenvalues.append(np.nan)
                
        except Exception as e:
            print(f"Erro com {n_terms}x{n_terms} termos: {e}")
            first_eigenvalues.append(np.nan)
    
    # Plot
    plt.figure(figsize=(10, 6))
    valid_indices = ~np.isnan(first_eigenvalues)
    if np.any(valid_indices):
        plt.plot(np.array(n_terms_list)[valid_indices], 
                 np.array(first_eigenvalues)[valid_indices], 
                 'g-^', linewidth=2, label='1º Autovalor')
        plt.xlabel('Número de Termos (nxn)')
        plt.ylabel('1º Autovalor')
        plt.title('Convergência - Helmholtz 2D')
        plt.grid(True)
        plt.legend()
        plt.savefig('output/convergence_helmholtz_corrigida.png', dpi=300, bbox_inches='tight')
        print("Gráfico salvo: output/convergence_helmholtz_corrigida.png")

def main():
    print("ANÁLISE DE CONVERGÊNCIA CORRIGIDA - MÉTODOS EDP")
    print("="*70)
    
    # Criar pasta output se não existir
    import os
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Executar análises corrigidas
    convergencia_poisson_corrigida()
    convergencia_calor_corrigida()
    convergencia_helmholtz_corrigida()
    
    print("\n" + "="*70)
    print("✅ ANÁLISE DE CONVERGÊNCIA CORRIGIDA CONCLUÍDA")
    print("Arquivos gerados em output/:")
    print("- convergence_poisson_corrigida.png")
    print("- convergence_heat_corrigida.png") 
    print("- convergence_helmholtz_corrigida.png")
    print("="*70)

if __name__ == "__main__":
    main()
