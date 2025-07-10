# Sistema Numérico para Equações Diferenciais Parciais - TRABALHO FINAL

## 🎯 Visão Geral

Este projeto implementa métodos numéricos para resolver **4 tipos fundamentais de Equações Diferenciais Parciais (EDPs)**, conforme especificado no trabalho acadêmico. O sistema suporta problemas elípticos, hiperbólicos, parabólicos e problemas 2D.

## 📋 Problemas Implementados

### 1. Equação de Poisson (Elíptica) ✅
- **Equação**: `∂²Ω/∂x² = Q(x)`, onde `Q(x) = -1`
- **Domínio**: `[0,1]` com condições `Ω(0) = Ω(1) = 0`
- **Métodos**: Galerkin e Rayleigh-Ritz
- **Solução analítica**: `Ω(x) = x(1-x)/2`
- **Status**: ✅ Implementado e validado (erro < 10⁻¹⁵)

### 2. Equação da Onda (Hiperbólica) ✅
- **Equação**: `∂u/∂t = λ²∂²u/∂x²`, onde `λ² = 4`
- **Domínio**: `[0,1] × [0,T]` com `u(0,t) = 0`, `u(x,0) = 1`
- **Método**: Wave-Galerkin com separação de variáveis
- **Características**: Solução temporal por superposição de modos
- **Status**: ✅ Implementado e testado

### 3. Equação do Calor (Parabólica) ✅
- **Equação**: `∂u/∂t = ∂²u/∂x²`
- **Condições**: `u(0,t) = u(1,t) = 0`, `u(x,0) = sin(3πx/2L)`
- **Método**: Heat-Galerkin com série de Fourier
- **Características**: Decaimento exponencial no tempo
- **Status**: ✅ Implementado e validado com solução analítica

### 4. Equação de Helmholtz 2D (Elíptica 2D) ✅
- **Equação**: `∂²φ/∂x² + ∂²φ/∂y² + λφ = 0`
- **Domínio**: `[0,1] × [0,γ]` com `φ = 0` nas bordas
- **Método**: Helmholtz-2D com análise de autovalores
- **Características**: Espectro discreto de autovalores
- **Status**: ✅ Implementado e testado

## 🏗️ Estrutura do Projeto
2. **Método de Rayleigh-Ritz** - Minimização funcional de energia
3. **Método dos Mínimos Quadrados** - Minimização da norma L² do resíduo
4. **Método dos Momentos** - Anulação de momentos do resíduo
5. **Método da Colocação** - Anulação pontual do resíduo
6. **Método das Sub-regiões** - Média do resíduo em subdomínios

## Estrutura do Projeto

```
edp/
├── core/
│   ├── methods/
│   │   ├── __init__.py
│   │   ├── numerical_method.py        # Classe base
│   │   ├── galerkin_method.py
│   │   ├── rayleigh_ritz_method.py
│   │   ├── least_squares_method.py
│   │   ├── moments_method.py
│   │   ├── colocacao_method.py
│   │   └── SubregionsMethod.py
│   └── __init__.py
├── examples/
│   ├── plot_solution.py              # Script de comparação
│   └── compare_methods.py
├── interface/
│   └── gui.py                        # Interface gráfica
├── tests/
│   └── test_methods.py
├── README.md
├── requirements.txt
└── main.py
```

## Requisitos

- **Python 3.8+**
- **Bibliotecas necessárias:**
  - `numpy` - Computação numérica
  - `sympy` - Computação simbólica
  - `matplotlib` - Visualização de dados
  - `tkinter` - Interface gráfica (incluído no Python)

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/osuamists/edp.git
cd edp
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar ambiente virtual

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

## Como Usar

### Interface Gráfica (Recomendado)

```bash
python interface/gui.py
```

**Funcionalidades da GUI:**

- ✅ Seleção múltipla de métodos (checkboxes)
- ✅ Ajuste do número de termos (1-10)
- ✅ Visualização gráfica em tempo real
- ✅ Tabela de erros comparativos
- ✅ Análise visual das soluções

### Script de Comparação

```bash
python examples/plot_solution.py
```

### Executar como módulo

```bash
python -m examples.plot_solution
```

## Resultados Esperados

| Método | Erro Típico | Comentário |
|--------|-------------|------------|
| **Galerkin** | ~9.1e-04 | Excelente para problemas variacionais |
| **Rayleigh-Ritz** | ~9.1e-04 | Equivalente ao Galerkin neste problema |
| **Mínimos Quadrados** | ~2.7e-03 | Erro global controlado |
| **Momentos** | ~9.1e-04 | Boa performance com base adequada |
| **Colocação** | ~7.9e-03 | Depende dos pontos escolhidos |
| **Sub-regiões** | ~6.6e-03 | Método mais simples |

## Funcionalidades

### ✅ **Core Features**

- Implementação robusta de 6 métodos numéricos
- Arquitetura orientada a objetos
- Tratamento de erros e casos especiais
- Cálculo automático de erros máximos

### ✅ **Interface Gráfica**

- Seleção interativa de métodos
- Controle do número de termos
- Visualização em tempo real
- Tabela de resultados comparativos

### ✅ **Análise e Visualização**

- Comparação visual com solução exata
- Cálculo de erros máximos
- Gráficos de alta qualidade
- Legenda informativa com erros

## Exemplos de Uso

### Testar um método específico

```python
from core.methods.galerkin_method import GalerkinMethod
import sympy as sp

# Definir problema
x = sp.Symbol('x')
f = sp.pi**2 * sp.sin(sp.pi * x)
domain = (0, 1)
boundary_conditions = [(0, 0), (1, 0)]

# Resolver
galerkin = GalerkinMethod(f, domain, boundary_conditions)
solution = galerkin.solve(n_terms=3)
print(f"Solução: {solution}")
```

### Comparar múltiplos métodos

```python
# Execute a interface gráfica e selecione os métodos desejados
python interface/gui.py
```

## Desenvolvimento

### Executar testes

```bash
python -m pytest tests/
```

### Estrutura das classes

- **NumericalMethod**: Classe base abstrata
- **Cada método**: Herda de NumericalMethod
- **Interface**: Integra todos os métodos

## Contribuições

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autor

Desenvolvido como projeto acadêmico para estudo de métodos numéricos aplicados a EDPs.

---

## Troubleshooting

### Erro de importação

```bash
# Execute a partir do diretório raiz do projeto
cd edp/
python interface/gui.py
```

### Problemas com matplotlib

```bash
pip install --upgrade matplotlib
```

### Interface não abre

- Verifique se o tkinter está instalado
- No Ubuntu: `sudo apt-get install python3-tk`

---

**🎯 Projeto completo e funcional para análise comparativa de métodos numéricos em EDPs!**
