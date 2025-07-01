# Comparador de Métodos Numéricos para EDPs

## Descrição

Este projeto implementa seis métodos numéricos diretos para resolução de uma EDP unidimensional clássica, comparando soluções aproximadas com a solução exata. Inclui interface gráfica interativa e análise visual completa dos resultados.

## Equação Resolvida

**Problema de Valor de Contorno:**

```
-u''(x) = π²sin(πx),  x ∈ [0,1]
u(0) = 0,  u(1) = 0
```

**Solução Exata:** `u(x) = sin(πx)`

## Métodos Implementados

1. **Método de Galerkin** - Projeção ortogonal do resíduo
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
