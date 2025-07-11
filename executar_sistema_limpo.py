#!/usr/bin/env python3
"""
SISTEMA EDP LIMPO - Execução Principal
Resolve 4 EDPs com gráficos únicos conforme especificações atualizadas
"""

import os
import subprocess
import sys
import time

def main():
    """Execução principal do sistema limpo"""
    
    print("🎯" * 25)
    print("🎯 SISTEMA EDP - VERSÃO FINAL LIMPA 🎯")
    print("🎯" * 25)
    print()
    print("📋 EQUAÇÕES IMPLEMENTADAS:")
    print("   🔧 Poisson 1D: Q(x) = 1/x, domínio [0,1]")
    print("   🔥 Calor 1D: u(x,0) = sin(3πx/2)")
    print("   🌊 Onda 1D: u(x,0) = 1")
    print("   ⚡ Helmholtz 2D: domínio [0,1]×[0,1]")
    print()
    
    # Garantir pasta output
    os.makedirs('output', exist_ok=True)
    
    # Scripts funcionais
    scripts = [
        "resolver_poisson.py",
        "resolver_calor.py", 
        "resolver_onda.py",
        "resolver_helmholtz.py"
    ]
    
    print("🚀 EXECUTANDO TODAS AS EDPs...")
    print("-" * 50)
    
    sucessos = 0
    for i, script in enumerate(scripts, 1):
        print(f"[{i}/4] Executando {script}...")
        
        try:
            result = subprocess.run([sys.executable, script], 
                                  capture_output=True, text=True, timeout=90)
            
            if result.returncode == 0:
                print(f"✅ {script} - SUCESSO!")
                sucessos += 1
            else:
                print(f"❌ {script} - ERRO!")
                print(f"STDERR: {result.stderr[:200]}")
                
        except Exception as e:
            print(f"💥 {script} - EXCEÇÃO: {e}")
    
    print()
    print("📊 RESULTADO FINAL:")
    print(f"   Scripts executados: {sucessos}/{len(scripts)}")
    
    if sucessos == len(scripts):
        print("🎉 TODAS AS EDPs EXECUTADAS COM SUCESSO!")
        print("📁 Verifique os gráficos em: output/")
        print("🎨 Cada EDP possui visualizações únicas e distintas")
    else:
        print("⚠️ Alguns problemas foram detectados.")
    
    print()
    print("📁 ESTRUTURA FINAL LIMPA:")
    print("   core/ - Módulos principais")
    print("   output/ - Gráficos gerados") 
    print("   resolver_*.py - Scripts individuais")
    print("   executar_edps_graficos_unicos.py - Script principal")

if __name__ == "__main__":
    main()
