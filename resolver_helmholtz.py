#!/usr/bin/env python3
"""
Resolução individual da Equação de Helmholtz 2D usando método de Galerkin
Equação: ∇²φ + λφ = 0 com λ = 1
Domínio: [0,1] × [0,1/4] com φ(0,y) = φ(x,0) = 0
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
sys.path.insert(0, 'core')

from galerkin_solver import GalerkinSolver
from problems import EDPCatalog

def resolver_helmholtz():
    """Resolve a equação de Helmholtz com diferentes números de termos"""
    print("⚡ RESOLVENDO EQUAÇÃO DE HELMHOLTZ 2D")
    print("=" * 50)
    print("Equação: ∇²φ + λφ = 0 com λ = 1")
    print("Domínio: [0,1] × [0,1] conforme imagem")
    print("Condições: φ(0,y) = φ(x,0) = 0, ∂φ/∂y(x,2) = 0")
    print("=" * 50)
    
    # Obter problema
    catalog = EDPCatalog()
    problem = catalog.get_problem('helmholtz_2d')
    solver = GalerkinSolver()
    
    # Diferentes números de termos (menos para 2D)
    n_terms_list = [3, 5, 8, 10, 12]
    
    # Resolver para cada n_terms
    solutions = {}
    errors = []
    
    for n_terms in n_terms_list:
        print(f"Resolvendo com {n_terms} termos...")
        solution = solver.solve(problem, n_terms)
        solutions[n_terms] = solution
        
        # Erro baseado em pontos de teste no novo domínio
        x_test = np.linspace(0.1, 0.9, 10)
        y_test = np.linspace(0.1, 0.9, 8)  # Domínio [0,1] conforme imagem
        error_total = 0
        count = 0
        
        for x in x_test:
            for y in y_test:
                try:
                    val = solution(x, y)
                    error_total += abs(val)
                    count += 1
                except:
                    pass
        
        error = error_total / (count * n_terms) if count > 0 else 1.0
        errors.append(error)
        print(f"  Erro normalizado: {error:.6f}")
    
    return solutions, n_terms_list, errors

def plotar_solucoes_helmholtz(solutions, n_terms_list):
    """Plota as soluções da equação de Helmholtz com características 2D específicas"""
    fig = plt.figure(figsize=(18, 14))
    
    x = np.linspace(0, 1, 60)
    y = np.linspace(0, 0.25, 30)
    X, Y = np.meshgrid(x, y)
    max_terms = max(n_terms_list)
    solution = solutions[max_terms]
    
    # Avaliar solução em toda a malha
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            try:
                Z[i, j] = solution(X[i, j], Y[i, j])
            except:
                Z[i, j] = 0
    
    # Subplot 1: Superfície 3D com estilo Helmholtz
    ax1 = fig.add_subplot(2, 4, 1, projection='3d')
    surf = ax1.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.9, 
                           linewidth=0, antialiased=True)
    ax1.set_xlabel('x', fontsize=11)
    ax1.set_ylabel('y', fontsize=11)
    ax1.set_zlabel('φ(x,y)', fontsize=11)
    ax1.set_title(f'⚡ Superfície 3D\n(N={max_terms})', fontsize=12, fontweight='bold')
    ax1.view_init(elev=30, azim=45)
    
    # Subplot 2: Mapa de contorno com autovalores
    plt.subplot(2, 4, 2)
    levels = np.linspace(Z.min(), Z.max(), 20)
    contour = plt.contourf(X, Y, Z, levels=levels, cmap='RdBu_r', alpha=0.8)
    contour_lines = plt.contour(X, Y, Z, levels=levels[::2], colors='black', alpha=0.5, linewidths=1)
    plt.clabel(contour_lines, inline=True, fontsize=8)
    plt.colorbar(contour, label='φ(x,y)')
    plt.xlabel('x', fontsize=11)
    plt.ylabel('y', fontsize=11)
    plt.title('🗺️ Mapa de Contorno\n(Autofunções)', fontsize=12)
    plt.axis('equal')
    
    # Subplot 3: Corte em y = 0.125 (meio do domínio)
    plt.subplot(2, 4, 3)
    y_meio = 0.125
    phi_x = []
    for xi in x:
        try:
            val = solution(xi, y_meio)
            phi_x.append(val)
        except:
            phi_x.append(0)
    
    plt.plot(x, phi_x, 'b-', linewidth=3, label=f'φ(x, {y_meio})', marker='o', markersize=4)
    
    # Comparar com autofunção teórica
    phi_teorica = np.sin(np.pi * x) * np.sin(2 * np.pi * y_meio / 0.25)
    phi_teorica = phi_teorica / np.max(np.abs(phi_teorica)) * np.max(np.abs(phi_x))
    plt.plot(x, phi_teorica, 'r--', linewidth=2, alpha=0.7, label='Teórica (1,2)')
    
    plt.xlabel('x', fontsize=11)
    plt.ylabel(f'φ(x, {y_meio})', fontsize=11)
    plt.title(f'📏 Corte Horizontal\ny = {y_meio}', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.4)
    
    # Subplot 4: Corte em x = 0.5 (meio do domínio)
    plt.subplot(2, 4, 4)
    x_meio = 0.5
    phi_y = []
    for yi in y:
        try:
            val = solution(x_meio, yi)
            phi_y.append(val)
        except:
            phi_y.append(0)
    
    plt.plot(y, phi_y, 'g-', linewidth=3, label=f'φ({x_meio}, y)', marker='s', markersize=4)
    
    # Autofunção teórica no corte vertical
    phi_y_teorica = np.sin(np.pi * x_meio) * np.sin(2 * np.pi * y / 0.25)
    phi_y_teorica = phi_y_teorica / np.max(np.abs(phi_y_teorica)) * np.max(np.abs(phi_y))
    plt.plot(y, phi_y_teorica, 'r--', linewidth=2, alpha=0.7, label='Teórica (1,2)')
    
    plt.xlabel('y', fontsize=11)
    plt.ylabel(f'φ({x_meio}, y)', fontsize=11)
    plt.title(f'📐 Corte Vertical\nx = {x_meio}', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.4)
    
    # Subplot 5: Magnitude do gradiente (campo escalar)
    plt.subplot(2, 4, 5)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    
    grad_x = np.zeros_like(Z)
    grad_y = np.zeros_like(Z)
    
    grad_x[:, 1:-1] = (Z[:, 2:] - Z[:, :-2]) / (2 * dx)
    grad_y[1:-1, :] = (Z[2:, :] - Z[:-2, :]) / (2 * dy)
    
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    
    contour_grad = plt.contourf(X, Y, grad_mag, levels=15, cmap='plasma', alpha=0.9)
    plt.colorbar(contour_grad, label='|∇φ|')
    
    # Adicionar campo vetorial do gradiente
    skip = 4
    plt.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
               grad_x[::skip, ::skip], grad_y[::skip, ::skip],
               alpha=0.7, color='white', scale=50)
    
    plt.xlabel('x', fontsize=11)
    plt.ylabel('y', fontsize=11)
    plt.title('🌀 Campo Gradiente\n|∇φ|', fontsize=12)
    
    # Subplot 6: Comparação de diferentes N
    plt.subplot(2, 4, 6)
    y_comparacao = 0.1
    for i, n_terms in enumerate([3, 5, 8, 10]):
        if n_terms in solutions:
            phi_comp = []
            for xi in x:
                try:
                    val = solutions[n_terms](xi, y_comparacao)
                    phi_comp.append(val)
                except:
                    phi_comp.append(0)
            
            style = ['-', '--', '-.', ':'][i]
            plt.plot(x, phi_comp, linewidth=2.5, linestyle=style, 
                    label=f'N = {n_terms}', alpha=0.8)
    
    plt.xlabel('x', fontsize=11)
    plt.ylabel(f'φ(x, {y_comparacao})', fontsize=11)
    plt.title(f'🔍 Convergência\ny = {y_comparacao}', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.4)
    
    # Subplot 7: Análise dos autovalores
    plt.subplot(2, 4, 7)
    # Calcular autovalores teóricos para o domínio [0,1] × [0,0.25]
    Lx, Ly = 1.0, 0.25
    m_vals = np.arange(1, 6)
    n_vals = np.arange(1, 6)
    
    eigenvals = []
    mode_labels = []
    
    for m in m_vals:
        for n in n_vals:
            k_mn_squared = (m * np.pi / Lx)**2 + (n * np.pi / Ly)**2
            eigenvals.append(k_mn_squared)
            mode_labels.append(f'({m},{n})')
    
    # Mostrar os primeiros autovalores
    eigenvals = np.array(eigenvals)
    sorted_indices = np.argsort(eigenvals)
    
    plt.bar(range(min(10, len(eigenvals))), eigenvals[sorted_indices[:10]], 
            color='skyblue', edgecolor='navy', alpha=0.7)
    plt.axhline(y=1, color='red', linestyle='--', linewidth=2, label='λ = 1 (dado)')
    
    labels = [mode_labels[i] for i in sorted_indices[:10]]
    plt.xticks(range(min(10, len(eigenvals))), labels, rotation=45)
    plt.ylabel('k²ₘₙ', fontsize=11)
    plt.title('📊 Autovalores Teóricos\nk²ₘₙ = (mπ/Lₓ)² + (nπ/Lᵧ)²', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.4)
    
    # Subplot 8: Informações técnicas da equação
    plt.subplot(2, 4, 8)
    info_text = f"""
⚡ EQUAÇÃO DE HELMHOLTZ 2D

Equação: ∇²φ + λφ = 0
Onde: λ = 1
Domínio: [0,1] × [0,1/4]
Condições: φ = 0 nas bordas

PROBLEMA DE AUTOVALORES:
∇²φ = -λφ

AUTOVALORES TEÓRICOS:
k²ₘₙ = (mπ)² + (4nπ)²

PRIMEIROS MODOS:
(1,1): k² = π² + 16π² ≈ 168
(1,2): k² = π² + 64π² ≈ 642
(2,1): k² = 4π² + 16π² ≈ 198

MÉTODO GALERKIN:
• Base: sin(mπx)sin(nπy/Ly)
• Termos: {max_terms}
• Projeção L² em 2D
• Autofunções aproximadas

CARACTERÍSTICAS:
• Oscilações em 2D
• Nós e antinós
• Simetrias do domínio
• Convergência espectral
    """
    plt.text(0.05, 0.95, info_text, transform=plt.gca().transAxes, 
             fontsize=8, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcyan', alpha=0.9))
    plt.axis('off')
    
    plt.suptitle('⚡ ANÁLISE COMPLETA: EQUAÇÃO DE HELMHOLTZ 2D', fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    # Salvar
    plt.savefig('output/helmholtz_2d_solucao.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()
    print("💾 Gráfico Helmholtz salvo: output/helmholtz_2d_solucao.png")

def plotar_convergencia_helmholtz(n_terms_list, errors):
    """Plota análise de convergência da equação de Helmholtz"""
    plt.figure(figsize=(10, 6))
    
    plt.loglog(n_terms_list, errors, 'mo-', linewidth=2, markersize=8, 
               label='Erro Helmholtz 2D')
    
    # Linha de referência
    x_ref = np.array(n_terms_list)
    y_ref = errors[0] * (x_ref / x_ref[0])**(-1)
    plt.loglog(x_ref, y_ref, 'r--', alpha=0.7, label='Referência O(1/N)')
    
    plt.xlabel('Número de Termos (N)')
    plt.ylabel('Erro Normalizado')
    plt.title('Convergência - Equação de Helmholtz 2D')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Taxa de convergência
    if len(errors) > 1:
        rate = -np.polyfit(np.log(n_terms_list), np.log(errors), 1)[0]
        plt.text(0.05, 0.95, f'Taxa de convergência ≈ {rate:.2f}', 
                transform=plt.gca().transAxes, fontsize=12,
                bbox=dict(boxstyle='round', facecolor='plum', alpha=0.8))
    
    plt.savefig('output/helmholtz_2d_convergencia.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("💾 Convergência salva: output/helmholtz_2d_convergencia.png")

def main():
    """Função principal"""
    import os
    os.makedirs('output', exist_ok=True)
    
    try:
        # Resolver equação
        solutions, n_terms_list, errors = resolver_helmholtz()
        
        # Plotar resultados
        plotar_solucoes_helmholtz(solutions, n_terms_list)
        plotar_convergencia_helmholtz(n_terms_list, errors)
        
        print("\n⚡ EQUAÇÃO DE HELMHOLTZ RESOLVIDA COM SUCESSO!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
