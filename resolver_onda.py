#!/usr/bin/env python3
"""
Resolução individual da Equação da Onda 1D usando método de Galerkin
Equação: ∂u/∂t = λ² ∂²u/∂x² com λ² = 4
Domínio: [0,1] × [0,1] com u(0,t) = 0 e u(x,0) = 1
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, 'core')

from galerkin_solver import GalerkinSolver
from problems import EDPCatalog

def resolver_onda():
    """Resolve a equação da onda com diferentes números de termos"""
    print("🌊 RESOLVENDO EQUAÇÃO DA ONDA 1D")
    print("=" * 50)
    print("Equação: ∂u/∂t = 4 ∂²u/∂x²")
    print("Domínio: [0,1] × [0,1]")
    print("Condições: u(0,t) = 0, u(x,0) = 1")
    print("=" * 50)
    
    # Obter problema
    catalog = EDPCatalog()
    problem = catalog.get_problem('wave_1d')
    solver = GalerkinSolver()
    
    # Diferentes números de termos
    n_terms_list = [5, 10, 15, 20, 25]
    
    # Resolver para cada n_terms
    solutions = {}
    errors = []
    
    for n_terms in n_terms_list:
        print(f"Resolvendo com {n_terms} termos...")
        solution = solver.solve(problem, n_terms)
        solutions[n_terms] = solution
        
        # Erro baseado na evolução temporal
        x_test = np.linspace(0, 1, 50)
        t_test = 0.1
        u_vals = solution(x_test, t_test)
        error = np.sqrt(np.mean(u_vals**2)) / n_terms
        errors.append(error)
        print(f"  Erro normalizado: {error:.6f}")
    
    return solutions, n_terms_list, errors

def plotar_solucoes_onda(solutions, n_terms_list):
    """Plota as soluções da equação da onda com ESTILO ÚNICO - Acústica/Vibrações"""
    fig = plt.figure(figsize=(18, 14))
    fig.patch.set_facecolor('#0a0a0a')  # Fundo preto estilo osciloscopio
    
    x = np.linspace(0, 1, 100)
    max_terms = max(n_terms_list)
    solution = solutions[max_terms]
    
    # Subplot 1: OSCILOSCOPIO DIGITAL - Propagação com rastro
    plt.subplot(2, 3, 1)
    plt.gca().set_facecolor('black')
    tempos = [0, 0.01, 0.025, 0.05, 0.075, 0.1]
    
    # Cores tipo fosforescência de osciloscopio
    scope_colors = ['#00ff00', '#00dd00', '#00bb00', '#009900', '#007700', '#005500']
    
    for i, t in enumerate(tempos):
        u = solution(x, t)
        intensity = 1.0 - i * 0.12  # Fade type persistence
        linewidth = 4 - i * 0.5
        
        plt.plot(x, u, color=scope_colors[i], linewidth=linewidth, alpha=intensity,
                label=f't = {t:.3f}s', marker=None)
        
        # Efeito de "brilho" nas cristas
        if i < 3:
            indices_peaks = np.where(np.abs(u) > 0.3)[0]
            if len(indices_peaks) > 0:
                plt.scatter(x[indices_peaks], u[indices_peaks], 
                           c=scope_colors[i], s=20, alpha=0.7, marker='o')
    
    # Grade tipo osciloscopio
    plt.grid(True, alpha=0.3, color='green', linestyle='-', linewidth=0.5)
    plt.axhline(y=0, color='white', linestyle='-', alpha=0.5, linewidth=1)
    plt.axvline(x=0.5, color='white', linestyle=':', alpha=0.3)
    
    plt.xlabel('Posição x [m]', fontsize=12, weight='bold', color='lime')
    plt.ylabel('Amplitude u(x,t)', fontsize=12, weight='bold', color='lime')
    plt.title('📟 OSCILOSCOPIO: PROPAGAÇÃO DE ONDAS', fontsize=14, fontweight='bold', color='green')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, 
               facecolor='black', edgecolor='green', labelcolor='lime')
    plt.tick_params(colors='lime')
    
    # Subplot 2: ANÁLISE ESPECTRAL - Frequências e harmônicos
    plt.subplot(2, 3, 2)
    plt.gca().set_facecolor('#001a2e')  # Azul escuro para análise espectral
    
    # Análise FFT em diferentes tempos
    t_samples = [0.01, 0.05, 0.1]
    fft_colors = ['#ff0080', '#0080ff', '#80ff00']
    
    x_fft = np.linspace(0, 1, 128)
    for i, t in enumerate(t_samples):
        u_sample = solution(x_fft, t)
        fft_result = np.fft.fft(u_sample)
        freqs = np.fft.fftfreq(len(x_fft), x_fft[1] - x_fft[0])
        
        # Plot magnitude do espectro
        magnitude = np.abs(fft_result[:len(freqs)//2])
        freq_pos = freqs[:len(freqs)//2]
        
        plt.semilogy(freq_pos[1:], magnitude[1:], color=fft_colors[i], 
                     linewidth=3, label=f't = {t:.2f}s', alpha=0.8)
        
        # Destacar picos principais
        peaks = np.where(magnitude > 0.1 * np.max(magnitude))[0]
        if len(peaks) > 0:
            plt.scatter(freq_pos[peaks], magnitude[peaks], 
                       c=fft_colors[i], s=40, marker='*', alpha=0.9)
    
    plt.xlabel('Frequência [Hz]', fontsize=12, weight='bold', color='cyan')
    plt.ylabel('Magnitude Espectral', fontsize=12, weight='bold', color='cyan')
    plt.title('� ANÁLISE HARMÔNICA', fontsize=14, weight='bold', color='magenta')
    plt.legend(facecolor='black', edgecolor='cyan', labelcolor='white')
    plt.grid(True, alpha=0.3, color='cyan', linestyle=':')
    plt.tick_params(colors='cyan')
    
    # Subplot 3: VELOCÍMETRO DE ONDA - Medição de velocidade
    plt.subplot(2, 3, 3)
    plt.gca().set_facecolor('#2a1810')  # Marrom para instrumentação
    
    # Calcular velocidade através do gradiente temporal
    tempos_vel = np.linspace(0.005, 0.15, 30)
    velocidades = []
    
    dt = 0.001
    x_fixed = 0.3  # Ponto fixo para medição
    
    for t in tempos_vel:
        u1 = solution(x_fixed, t)
        u2 = solution(x_fixed, t + dt)
        velocidade_local = (u2 - u1) / dt
        velocidades.append(abs(velocidade_local))
    
    # Plot tipo velocímetro
    plt.plot(tempos_vel, velocidades, color='orange', linewidth=4, 
             label='Velocidade local', marker='o', markersize=4)
    
    # Linha de referência
    vel_media = np.mean(velocidades)
    plt.axhline(y=vel_media, color='red', linestyle='--', linewidth=2, 
                alpha=0.7, label=f'Média: {vel_media:.2f}')
    
    # Barras de magnitude
    for i in range(0, len(tempos_vel), 3):
        altura = velocidades[i] / max(velocidades) * 0.3
        plt.bar(tempos_vel[i], altura * max(velocidades), 
                width=0.005, alpha=0.5, color='yellow')
    
    plt.xlabel('Tempo t [s]', fontsize=12, weight='bold', color='orange')
    plt.ylabel('|∂u/∂t| [m/s]', fontsize=12, weight='bold', color='orange')
    plt.title('⚡ VELOCÍMETRO DE PARTÍCULAS', fontsize=14, weight='bold', color='gold')
    plt.legend(facecolor='black', edgecolor='orange', labelcolor='white')
    plt.grid(True, alpha=0.3, color='gray', linestyle='-.')
    plt.tick_params(colors='orange')
    
    # Subplot 4: Comparação de amplitudes (diferentes N)
    plt.subplot(2, 3, 4)
    t_fixo = 0.1
    for i, n_terms in enumerate([5, 10, 15, 20]):
        if n_terms in solutions:
            u = solutions[n_terms](x, t_fixo)
            style = ['-', '--', '-.', ':'][i % 4]
            plt.plot(x, u, linewidth=3, linestyle=style, 
                    label=f'N = {n_terms}', alpha=0.8)
    
    plt.xlabel('x', fontsize=12)
    plt.ylabel(f'u(x, {t_fixo})', fontsize=12)
    plt.title(f'🔍 Convergência em t = {t_fixo}', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.4)
    
    # Subplot 5: Evolução da energia (característica de onda 1ª ordem)
    plt.subplot(2, 3, 5)
    t_vals = np.linspace(0, 0.3, 100)
    energia = []
    amplitude_max = []
    
    for t in t_vals:
        u_vals = solution(x, t)
        E = np.trapz(u_vals**2, x)  # Energia
        A_max = np.max(np.abs(u_vals))  # Amplitude máxima
        energia.append(E)
        amplitude_max.append(A_max)
    
    # Dois eixos Y para energia e amplitude
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    line1 = ax1.plot(t_vals, energia, 'b-', linewidth=3, label='Energia')
    line2 = ax2.plot(t_vals, amplitude_max, 'r-', linewidth=3, label='Amplitude máx')
    
    ax1.set_xlabel('Tempo t', fontsize=12)
    ax1.set_ylabel('Energia', color='b', fontsize=12)
    ax2.set_ylabel('Amplitude máxima', color='r', fontsize=12)
    
    # Combinar legendas
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')
    
    plt.title('⚡ Evolução Energética', fontsize=14)
    ax1.grid(True, alpha=0.4)
    
    # Subplot 6: Informações da onda
    plt.subplot(2, 3, 6)
    info_text = f"""
🌊 EQUAÇÃO DA ONDA 1D (1ª ORDEM)

Equação: ∂u/∂t = λ²∂²u/∂x²
Onde: λ² = 4 → λ = 2
Tipo: EDP de 1ª ordem temporal
Domínio: [0,1] × [0,∞)
Condições: u(0,t) = 0, u(x,0) = 1

CARACTERÍSTICAS:
• Propagação unidirecional
• Velocidade finita
• Dissipação numérica
• Frentes de onda suaves

FÍSICA ATÍPICA:
• NÃO é equação de onda clássica
• Mais similar à difusão rápida
• Comportamento parabólico-like
• Sem oscilações

MÉTODO GALERKIN:
• Base: sin(nπx)
• Termos: {max_terms}
• Separação de variáveis
• Decaimento exponencial

NOTA: Esta é uma EDP híbrida
entre difusão e onda!
    """
    plt.text(0.05, 0.95, info_text, transform=plt.gca().transAxes, 
             fontsize=9, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))
    plt.axis('off')
    
    plt.suptitle('🌊 ANÁLISE COMPLETA: EQUAÇÃO DA ONDA 1D (1ª ORDEM)', fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    # Salvar
    plt.savefig('output/onda_1d_solucao.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()
    print("💾 Gráfico Onda salvo: output/onda_1d_solucao.png")

def plotar_convergencia_onda(n_terms_list, errors):
    """Plota análise de convergência da equação da onda"""
    plt.figure(figsize=(10, 6))
    
    plt.loglog(n_terms_list, errors, 'go-', linewidth=2, markersize=8, 
               label='Erro Onda 1D')
    
    # Linha de referência
    x_ref = np.array(n_terms_list)
    y_ref = errors[0] * (x_ref / x_ref[0])**(-1)
    plt.loglog(x_ref, y_ref, 'r--', alpha=0.7, label='Referência O(1/N)')
    
    plt.xlabel('Número de Termos (N)')
    plt.ylabel('Erro Normalizado')
    plt.title('Convergência - Equação da Onda 1D')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Taxa de convergência
    if len(errors) > 1:
        rate = -np.polyfit(np.log(n_terms_list), np.log(errors), 1)[0]
        plt.text(0.05, 0.95, f'Taxa de convergência ≈ {rate:.2f}', 
                transform=plt.gca().transAxes, fontsize=12,
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.savefig('output/onda_1d_convergencia.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("💾 Convergência salva: output/onda_1d_convergencia.png")

def main():
    """Função principal"""
    import os
    os.makedirs('output', exist_ok=True)
    
    try:
        # Resolver equação
        solutions, n_terms_list, errors = resolver_onda()
        
        # Plotar resultados
        plotar_solucoes_onda(solutions, n_terms_list)
        plotar_convergencia_onda(n_terms_list, errors)
        
        print("\n🌊 EQUAÇÃO DA ONDA RESOLVIDA COM SUCESSO!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
