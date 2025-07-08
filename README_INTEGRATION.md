# Sistema Integrado de Resolução de EDPs

## 🎯 Visão Geral

Este sistema integra um **catálogo de EDPs** com **métodos numéricos** para resolver equações diferenciais parciais de forma unificada e intuitiva.

## 📁 Estrutura do Projeto

```
edp/
├── core/
│   ├── problems.py              # Catálogo de EDPs
│   ├── boundary_conditions.py  # Gerenciador de condições de contorno
│   ├── solver.py               # Solver principal (integração)
│   ├── config.py               # Configurações de compatibilidade
│   └── methods/                # Métodos numéricos
│       ├── galerkin_method.py
│       ├── colocacao_method.py
│       ├── least_squares_method.py
│       ├── rayleigh_ritz_method.py
│       ├── moments_method.py
│       └── SubregionsMethod.py
├── examples/
│   ├── integrated_example.py   # Exemplo de uso
│   └── plot_solution.py
├── tests/
│   └── test_integration.py     # Testes de integração
└── interface/
    └── gui.py                  # Interface gráfica
```

## 🚀 Como Usar

### 1. Uso Básico

```python
from core.solver import EDPSolver

# Criar solver
solver = EDPSolver()

# Listar problemas disponíveis
problems = solver.list_problems()
print(problems)
# Output: {'poisson': 'Poisson', 'onda_1d': 'Onda 1D', ...}

# Listar métodos disponíveis
methods = solver.list_methods()
print(methods)
# Output: ['galerkin', 'colocacao', 'least_squares', ...]

# Resolver problema
result = solver.solve("poisson", "galerkin", n_terms=5)
```

### 2. Obter Recomendações

```python
# Recomendações simples
recommended = solver.recommend_method("poisson")
print(recommended)
# Output: ['galerkin', 'rayleigh_ritz', 'least_squares']

# Recomendações detalhadas
detailed = solver.recommend_method("poisson", detailed=True)
for method, info in detailed.items():
    print(f"{method}: {info['description']}")
```

### 3. Comparar Métodos

```python
# Comparar múltiplos métodos para o mesmo problema
comparison = solver.compare_methods(
    "poisson", 
    ["galerkin", "rayleigh_ritz"], 
    n_terms=4
)

for method, result in comparison.items():
    if "error" in result:
        print(f"{method}: ERRO")
    else:
        print(f"{method}: Sucesso")
```

### 4. Informações Detalhadas

```python
# Obter informações sobre um problema
info = solver.get_problem_info("onda_1d")
print(f"Nome: {info['nome']}")
print(f"Equação: {info['equation']}")
print(f"Domínio: {info['domain']}")
```

## 📊 Problemas Disponíveis

| Problema | Tipo | Equação | Aplicação |
|----------|------|---------|-----------|
| **Poisson** | Elíptica | ∇²u + Q(x) = 0 | Temperatura, potencial |
| **Onda 1D** | Hiperbólica | ∂²u/∂t² - c²∂²u/∂x² = 0 | Vibração, ondas |
| **Calor 1D** | Parabólica | ∂u/∂t - α∂²u/∂x² = 0 | Difusão de calor |
| **Helmholtz 2D** | Elíptica | ∇²u + k²u = 0 | Acústica, eletromagnetismo |

## 🔧 Métodos Numéricos

| Método | Tipo | Melhor Para | Prioridade |
|--------|------|-------------|------------|
| **Galerkin** | Resíduo Ponderado | Geral, robusto | ⭐⭐⭐ |
| **Rayleigh-Ritz** | Variacional | Problemas elípticos | ⭐⭐⭐ |
| **Mínimos Quadrados** | Resíduo Ponderado | Estabilidade numérica | ⭐⭐ |
| **Colocação** | Resíduo Ponderado | Implementação simples | ⭐⭐ |
| **Momentos** | Resíduo Ponderado | Problemas específicos | ⭐ |
| **Sub-regiões** | Divisão de Domínio | Geometrias complexas | ⭐⭐ |

## ⚙️ Configuração Avançada

### Parâmetros Padrão por Método

```python
# Obter parâmetros padrão
params = solver.get_default_parameters("galerkin")
print(params)
# Output: {'n_terms': 5, 'precision': 1e-6, 'basis_type': 'polynomial'}

# Usar parâmetros customizados
result = solver.solve("poisson", "galerkin", 
                     n_terms=8, 
                     precision=1e-8)
```

### Validação de Requisitos

```python
# Validar se problema atende requisitos
try:
    solver.validate_problem_requirements("onda_1d")
    print("✓ Problema válido")
except ValueError as e:
    print(f"✗ Erro: {e}")
```

## 🧪 Testando o Sistema

```bash
# Executar testes de integração
python tests/test_integration.py

# Executar exemplo completo
python examples/integrated_example.py
```

## 🎨 Visualização

```python
# Plotar resultado (em desenvolvimento)
from examples.plot_solution import plot_1d_solution

result = solver.solve("poisson", "galerkin")
plot_1d_solution(result)
```

## 🔄 Fluxo de Trabalho

1. **Escolher Problema**: Selecionar EDP do catálogo
2. **Obter Recomendações**: Ver métodos mais adequados
3. **Resolver**: Aplicar método escolhido
4. **Comparar**: Testar diferentes métodos
5. **Visualizar**: Plotar resultados

## 🚧 Próximos Desenvolvimentos

- [ ] Implementação completa de todos os métodos
- [ ] Interface gráfica interativa
- [ ] Visualização 2D e animações
- [ ] Mais problemas no catálogo
- [ ] Exportação de resultados
- [ ] Análise de convergência

## 📝 Notas Técnicas

- **Condições de Contorno**: Gerenciadas automaticamente
- **Validação**: Verificação automática de compatibilidade
- **Flexibilidade**: Fácil adição de novos problemas/métodos
- **Configurabilidade**: Parâmetros ajustáveis por método

---

**💡 Dica**: Use `solver.recommend_method(problema, detailed=True)` para obter explicações detalhadas sobre qual método usar!
