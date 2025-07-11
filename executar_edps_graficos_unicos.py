#!/usr/bin/env python3
"""
EXECUÇÃO PRINCIPAL: 4 EDPs Distintas com Gráficos Únicos
Sistema limpo que resolve cada equação separadamente com visualizações específicas
"""

import os
import subprocess
import sys

def main():
    """Executa todas as 4 EDPs com gráficos distintos e melhorados"""
    
    print("🎯" * 20)
    print("🎯 SISTEMA EDP - GRÁFICOS ÚNICOS E DISTINTOS 🎯")
    print("🎯" * 20)
    print()
    print("📊 Cada equação terá visualizações COMPLETAMENTE DIFERENTES:")
    print("   🔧 Poisson: Análise de curvatura e singularidade")
    print("   🔥 Calor: Difusão térmica e decaimento energético") 
    print("   🌊 Onda: Propagação e frentes de onda")
    print("   ⚡ Helmholtz: Autovalores e campos 2D")
    print()
    
    # Criar diretório limpo
    os.makedirs('output', exist_ok=True)
    
    # Scripts na ordem das equações da imagem
    scripts = [
        ("resolver_poisson.py", "🔧 EQUAÇÃO DE POISSON 1D"),
        ("resolver_onda.py", "🌊 EQUAÇÃO DA ONDA 1D"),
        ("resolver_calor.py", "🔥 EQUAÇÃO DO CALOR 1D"),
        ("resolver_helmholtz.py", "⚡ EQUAÇÃO DE HELMHOLTZ 2D")
    ]
    
    resultados = []
    
    for i, (script, titulo) in enumerate(scripts, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/4] {titulo}")
        print(f"{'='*60}")
        
        try:
            result = subprocess.run([sys.executable, script], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ {titulo} - RESOLVIDA COM SUCESSO!")
                if result.stdout:
                    # Mostrar apenas as últimas linhas relevantes
                    lines = result.stdout.strip().split('\n')
                    for line in lines[-3:]:
                        if line.strip():
                            print(f"   {line}")
                resultados.append((titulo, True))
            else:
                print(f"❌ ERRO em {titulo}:")
                if result.stderr:
                    print(f"   {result.stderr[-200:]}")  # Últimos 200 chars do erro
                resultados.append((titulo, False))
                
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT em {titulo} (>120s)")
            resultados.append((titulo, False))
        except Exception as e:
            print(f"❌ ERRO INESPERADO em {titulo}: {e}")
            resultados.append((titulo, False))
    
    # Resumo final
    print(f"\n{'🎊'*20}")
    print("🎊 RESULTADO FINAL 🎊")
    print(f"{'🎊'*20}")
    
    sucessos = sum(1 for _, sucesso in resultados if sucesso)
    
    for titulo, sucesso in resultados:
        status = "✅ SUCESSO" if sucesso else "❌ FALHOU"
        print(f"{status} - {titulo}")
    
    print(f"\n📊 ESTATÍSTICA: {sucessos}/4 equações resolvidas")
    
    if sucessos == 4:
        print("\n🏆 TODAS AS 4 EQUAÇÕES RESOLVIDAS COM GRÁFICOS ÚNICOS!")
        
        # Verificar gráficos gerados
        graficos_esperados = [
            "poisson_1d_solucao.png",
            "poisson_1d_convergencia.png",
            "onda_1d_solucao.png",
            "onda_1d_convergencia.png", 
            "calor_1d_solucao.png",
            "calor_1d_convergencia.png",
            "helmholtz_2d_solucao.png",
            "helmholtz_2d_convergencia.png"
        ]
        
        print(f"\n📈 GRÁFICOS GERADOS:")
        graficos_encontrados = 0
        
        for grafico in graficos_esperados:
            if os.path.exists(f"output/{grafico}"):
                tamanho = os.path.getsize(f"output/{grafico}")
                print(f"   ✅ {grafico} ({tamanho:,} bytes)")
                graficos_encontrados += 1
            else:
                print(f"   ❌ {grafico} (não encontrado)")
        
        print(f"\n📊 GRÁFICOS: {graficos_encontrados}/{len(graficos_esperados)}")
        
        if graficos_encontrados == len(graficos_esperados):
            print("\n🎨 TODOS OS GRÁFICOS ÚNICOS FORAM GERADOS!")
            print("\n📋 CARACTERÍSTICAS DISTINTAS:")
            print("   🔧 Poisson: Análise de singularidade e curvatura")
            print("   🔥 Calor: Mapas térmicos e decaimento exponencial")
            print("   🌊 Onda: Diagramas espaço-tempo e propagação")  
            print("   ⚡ Helmholtz: Superfícies 3D e autovalores")
            
        print(f"\n📁 Verifique os gráficos em: output/")
        
    else:
        print(f"\n⚠️ EXECUÇÃO PARCIAL: {sucessos}/4 equações")
    
    print(f"\n{'🎯'*20}")

if __name__ == "__main__":
    main()
