# EDP Solver - Método de Galerkin

Sistema simplificado para resolver 4 EDPs clássicas usando o método de Galerkin e análise de convergência automática.

## EDPs Implementadas

1. **Poisson 1D**: ∇²u = -π²sin(πx)
2. **Calor 1D**: ∂u/∂t = ∂²u/∂x²  
3. **Onda 1D**: ∂²u/∂t² = 4∂²u/∂x²
4. **Helmholtz 2D**: ∇²u + 4u = 0

## Como Executar

```bash
python main.py
```

## Características

- **Método único**: Apenas Galerkin para todas as EDPs
- **Análise automática**: Convergência para diferentes números de termos
- **Visualização**: Gráficos de soluções e convergência
- **Comparação**: Erro em relação às soluções analíticas

## Estrutura

- `core/problems.py`: Catálogo das EDPs
- `core/galerkin_solver.py`: Implementação do método de Galerkin
- `core/convergence_analyzer.py`: Análise de convergência
- `visualizer.py`: Visualização dos resultados
- `main.py`: Script principal

## Resultados

O programa gera automaticamente:

1. **Gráficos de convergência**: Mostra como o erro diminui com o aumento do número de termos
2. **Soluções comparadas**: Soluções numéricas vs analíticas
3. **Análise estatística**: Erro mínimo e taxas de convergência

## Dependências

- numpy
- matplotlib
- scipy
- sympy

## Instalação

```bash
pip install numpy matplotlib scipy sympy
```

## Saída

- Gráficos salvos em `output/`
- Análise de convergência no console
- Comparação com soluções analíticas
