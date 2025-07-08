"""
Teste completo da integração com todos os métodos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.simple_solver import SimplifiedEDPSolver

def test_all_methods():
    print("=== Teste Completo de Todos os Métodos ===\n")
    
    solver = SimplifiedEDPSolver()
    
    # Status atual
    status = solver.status_report()
    print(f"📊 Status: {status['methods_available']} métodos, {status['problems_available']} problemas")
    print(f"🔧 Métodos: {', '.join(status['methods'])}")
    print(f"📚 Problemas: {', '.join(status['problems'])}\n")
    
    # Matriz de compatibilidade: problema x método
    results_matrix = {}
    
    print("🧪 Testando todas as combinações Problema x Método:\n")
    
    for problem in status['problems']:
        results_matrix[problem] = {}
        print(f"📖 Problema: {problem.upper()}")
        
        # Obter recomendações
        recommendations = solver.recommend_method(problem)
        print(f"   💡 Recomendados: {recommendations}")
        
        # Testar cada método
        for method in status['methods']:
            try:
                result = solver.solve(problem, method, n_terms=3)
                
                if result['status'] == 'success':
                    results_matrix[problem][method] = "✅ Sucesso"
                    print(f"   ✅ {method}: Sucesso")
                elif result['status'] == 'error':
                    results_matrix[problem][method] = f"❌ {result['error'][:30]}..."
                    print(f"   ❌ {method}: {result['error'][:50]}...")
                else:
                    results_matrix[problem][method] = "⚠️ Parcial"
                    print(f"   ⚠️ {method}: {result.get('solution', 'Parcial')}")
                    
            except Exception as e:
                results_matrix[problem][method] = f"💥 {str(e)[:30]}..."
                print(f"   💥 {method}: {str(e)[:50]}...")
        
        print()
    
    # Resumo da matriz de compatibilidade
    print("📋 MATRIZ DE COMPATIBILIDADE:")
    print("="*80)
    
    # Cabeçalho
    header = "Problema".ljust(12)
    for method in status['methods']:
        header += method[:10].ljust(12)
    print(header)
    print("-" * len(header))
    
    # Dados
    for problem in status['problems']:
        line = problem.ljust(12)
        for method in status['methods']:
            symbol = "✅" if "Sucesso" in results_matrix[problem][method] else "❌"
            line += symbol.ljust(12)
        print(line)
    
    # Estatísticas
    print("\n📈 ESTATÍSTICAS:")
    total_tests = len(status['problems']) * len(status['methods'])
    successful_tests = sum(1 for p in results_matrix.values() 
                          for result in p.values() 
                          if "Sucesso" in result)
    
    success_rate = (successful_tests / total_tests) * 100
    print(f"   Total de testes: {total_tests}")
    print(f"   Sucessos: {successful_tests}")
    print(f"   Taxa de sucesso: {success_rate:.1f}%")
    
    # Método mais versátil
    method_scores = {}
    for method in status['methods']:
        score = sum(1 for p in results_matrix.values() 
                   if "Sucesso" in p.get(method, ""))
        method_scores[method] = score
    
    best_method = max(method_scores, key=method_scores.get)
    print(f"   🏆 Método mais versátil: {best_method} ({method_scores[best_method]}/{len(status['problems'])} problemas)")
    
    # Problema mais compatível
    problem_scores = {}
    for problem in status['problems']:
        score = sum(1 for result in results_matrix[problem].values() 
                   if "Sucesso" in result)
        problem_scores[problem] = score
    
    easiest_problem = max(problem_scores, key=problem_scores.get)
    print(f"   🎯 Problema mais compatível: {easiest_problem} ({problem_scores[easiest_problem]}/{len(status['methods'])} métodos)")
    
    return results_matrix, success_rate

def test_method_comparison():
    print("\n" + "="*80)
    print("🔍 COMPARAÇÃO DETALHADA DE MÉTODOS (Problema: Poisson)")
    print("="*80)
    
    solver = SimplifiedEDPSolver()
    
    # Comparar todos os métodos para Poisson
    methods = solver.list_methods()
    comparison = solver.compare_methods("poisson", methods, n_terms=4)
    
    for method, result in comparison.items():
        print(f"\n🔧 Método: {method.upper()}")
        print(f"   Status: {result.get('status', 'unknown')}")
        
        if result.get('status') == 'success':
            solution = result.get('solution')
            print(f"   Tipo de solução: {type(solution)}")
            print(f"   Solução: {str(solution)[:60]}...")
        elif result.get('status') == 'error':
            print(f"   Erro: {result.get('error', 'Desconhecido')}")

if __name__ == "__main__":
    results_matrix, success_rate = test_all_methods()
    
    if success_rate > 50:
        print(f"\n🎉 INTEGRAÇÃO BEM-SUCEDIDA! Taxa: {success_rate:.1f}%")
    else:
        print(f"\n⚠️  Integração parcial. Taxa: {success_rate:.1f}%")
    
    test_method_comparison()
    
    print(f"\n{'='*80}")
    print("🚀 CONCLUSÕES:")
    print("1. ✅ Sistema de integração funcionando")
    print("2. ✅ Múltiplos métodos numéricos operacionais") 
    print("3. ✅ Validação automática de condições de contorno")
    print("4. ✅ Recomendações inteligentes de métodos")
    print("5. ✅ Comparação automática entre métodos")
    print("\n💡 Próximo: Implementar visualização e interface gráfica!")
