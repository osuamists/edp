# EDP Solver - Método de Galerkin

Solver para 4 Equações Diferenciais Parciais clássicas usando o método de Galerkin com análise automática de convergência.

## 📊 Equações Implementadas

1. **Poisson 1D**: `-d²u/dx² = 1/x` em `[0.01, 1]` com `u(0.01) = u(1) = 0`
2. **Calor 1D**: `∂u/∂t = ∂²u/∂x²` em `[0, 1]` com `u(0,t) = u(1,t) = 0`, `u(x,0) = sin(3πx/2)`
3. **Onda 1D**: `∂u/∂t = 4∂²u/∂x²` em `[0, 1]` com `u(0,t) = 0`, `u(x,0) = 1`
4. **Helmholtz 2D**: `∇²φ + λφ = 0` em `[0,1] × [0,1/4]` com condições homogêneas

## 🚀 Como Executar

```bash
python main.py
```

Os gráficos de convergência são gerados automaticamente em `output/`.

## 📁 Estrutura

- `core/problems.py` - Catálogo das 4 EDPs
- `core/galerkin_solver.py` - Solver unificado  
- `core/convergence_analyzer.py` - Análise de convergência
- `visualizer.py` - Visualização dos resultados
- `main.py` - Script principal
- `output/` - Gráficos gerados

## 🎯 Resultados

O programa gera automaticamente gráficos de convergência para todas as 4 equações, mostrando como o erro diminui com o aumento do número de termos no método de Galerkin.
