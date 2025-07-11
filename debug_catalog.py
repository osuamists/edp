"""
Debug do catálogo
"""

from core import EDPCatalog

catalog = EDPCatalog()
print("Problemas disponíveis:")
print(list(catalog.problems.keys()))

try:
    problem = catalog.get_problem('poisson_1d')
    print("✓ poisson_1d encontrado")
except Exception as e:
    print(f"✗ Erro: {e}")

try:
    all_problems = catalog.get_all_problems()
    print(f"Total de problemas: {len(all_problems)}")
    for key in all_problems:
        print(f"  - {key}")
except Exception as e:
    print(f"✗ Erro ao listar: {e}")
