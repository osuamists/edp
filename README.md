# Sistema EDP Solver - Resolução de Equações Diferenciais Parciais

## 📋 Descrição

Sistema robusto para resolução de 4 EDPs específicas usando método de Galerkin com visualizações únicas.

## 🔧 Equações Implementadas

1. **Poisson 1D**: `-d²u/dx² = 1/x` no domínio `[0,1]`
2. **Calor 1D**: `∂u/∂t = ∂²u/∂x²` com `u(x,0) = sin(3πx/2)`
3. **Onda 1D**: `∂u/∂t = 4∂²u/∂x²` com `u(x,0) = 1`
4. **Helmholtz 2D**: `∇²φ + φ = 0` no domínio `[0,1]×[0,1]`

## 🚀 Como Usar

### Execução Individual:
```bash
python resolver_poisson.py     # Resolve apenas Poisson
python resolver_calor.py       # Resolve apenas Calor
python resolver_onda.py        # Resolve apenas Onda
python resolver_helmholtz.py   # Resolve apenas Helmholtz
```

### Execução Completa:
```bash
python executar_sistema_limpo.py  # Executa todas as 4 EDPs
```

## 📊 Resultados

- **Gráficos**: 8 arquivos PNG únicos em `output/`
- **Análise**: Solução + convergência para cada EDP
- **Visualização**: Estilo único para cada equação

## 📁 Estrutura

```
edp/
├── core/                     # Módulos principais
├── output/                   # Gráficos gerados
├── resolver_*.py            # Scripts individuais
└── executar_sistema_limpo.py # Script principal
```

## 🛠️ Dependências

- Python 3.8+
- numpy, matplotlib, sympy

## 📖 Documentação Completa

Ver `RELATORIO_TECNICO.md` para especificações detalhadas.

---
**Status**: ✅ Funcional e Validado
