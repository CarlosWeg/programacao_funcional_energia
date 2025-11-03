# 💡 Sistema de Faturamento de Energia Elétrica

Sistema desenvolvido aplicando conceitos de **Programação Funcional** para cálculo de faturamento de energia elétrica com tarifação progressiva, bandeiras tarifárias e impostos.

---

## 📋 Sobre o Projeto

Este sistema calcula o valor da fatura de energia elétrica considerando:

- **Tarifação Progressiva por Faixas**: O custo do kWh aumenta conforme o consumo
- **Bandeiras Tarifárias**: Adicional conforme condições de geração (verde, amarela, vermelha)
- **Impostos**: ICMS, PIS e COFINS aplicados sobre o valor base
- **Princípios de Programação Funcional**: Funções puras, imutabilidade e funções de ordem superior

### Faixas de Tarifação

| Faixa de Consumo | Tarifa (R$/kWh) |
|------------------|-----------------|
| 0 - 100 kWh      | R$ 0,50         |
| 101 - 200 kWh    | R$ 0,75         |
| 201 - 500 kWh    | R$ 1,00         |
| Acima de 500 kWh | R$ 1,35         |

### Bandeiras Tarifárias

- **Verde**: Sem adicional
- **Amarela**: + R$ 0,05 por kWh consumido
- **Vermelha**: + R$ 0,10 por kWh consumido

### Impostos

- **ICMS**: 18%
- **PIS**: 1,65%
- **COFINS**: 7,61%

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.7 ou superior
- `tkinter` para a interface gráfica (geralmente já vem com Python)

⚠️ Atenção: Requisito para macOS

O `tkinter` (Tcl/Tk) geralmente já vem instalado com o Python. No entanto, 
em algumas instalações, como por exemplo do macOS, 
esse pacote gráfico não é incluído por padrão.

Se você receber o erro: `ModuleNotFoundError: No module named '_tkinter'`

Execute no terminal (substitua X.XX pela sua versão do Python):
```bash
brew install python-tk@X.XX
```

Ou tente o comando genérico:
```bash
brew install python-tk
```

### Passos para Execução

1. **Clone o repositório**:
```bash
git clone https://github.com/CarlosWeg/programacao_funcional_energia.git
cd programacao_funcional_energia
```

2. **Execute o programa**:
```bash
python faturamento_energia.py
```

3. **Use a interface**:
   - Digite o consumo em kWh
   - Selecione a bandeira tarifária
   - Clique em "Calcular Faturamento"
   - Visualize o resultado detalhado

---

## 💻 Conceitos de Programação Funcional Aplicados

### 1. **Funções Puras**

Todas as funções de cálculo e validação são puras:
- Não modificam estado externo
- Retornam sempre o mesmo resultado para as mesmas entradas
- Sem efeitos colaterais

Exemplos:
```python
def validar_numero_positivo(valor: str) -> Tuple[bool, Optional[float], str]:
    """Função pura - apenas valida e retorna resultado"""
    try:
        num = float(valor.replace(',', '.'))
        if num < 0:
            return (False, None, "O valor deve ser positivo")
        return (True, num, "")
    except ValueError:
        return (False, None, "Valor inválido")

def calcular_imposto(base_calculo: float, aliquota: float) -> float:
    """Função pura - apenas calcula, sem modificar estado"""
    return base_calculo * aliquota
```

### 2. **Imutabilidade**

Os valores originais nunca são modificados:
- Constantes em UPPERCASE (TARIFAS_FAIXAS, BANDEIRAS, IMPOSTOS)
- Funções retornam novos valores/estruturas
- Dados de entrada permanecem intactos

```python
# Constantes imutáveis
TARIFAS_FAIXAS = (
    (0, 100, 0.50),
    (100, 200, 0.75),
    # ...
)

# Retorna novo dicionário, não modifica entrada
def calcular_faturamento(consumo: float, bandeira: str) -> Dict:
    # ... cálculos ...
    return {  # Novo objeto
        'consumo_kwh': consumo,
        'total_final': total_final,
        # ...
    }
```

### 3. **Funções de Ordem Superior**

Uso de `map`, `filter` e `reduce`:

#### **Map** - Transforma coleções
```python
def calcular_impostos(base_calculo: float) -> Dict[str, float]:
    """Usa map para calcular cada imposto"""
    impostos_calculados = dict(
        map(
            lambda item: (item[0], calcular_imposto(base_calculo, item[1])),
            IMPOSTOS.items()
        )
    )
    return impostos_calculados
```

#### **Reduce** - Agrega valores
```python
# Soma valores das faixas
subtotal_consumo = reduce(
    lambda acc, faixa: acc + faixa['valor'],
    faixas_detalhadas,
    0.0
)

# Soma total de impostos
total_impostos = reduce(
    lambda acc, valor: acc + valor,
    impostos_detalhados.values(),
    0.0
)
```

### 4. **Composição de Funções**

Funções pequenas e reutilizáveis que se combinam:

```python
def calcular_faturamento(consumo: float, bandeira: str) -> Dict:
    """Função que compõe outras funções puras"""
    # 1. Calcula faixas
    faixas_detalhadas = calcular_tarifacao_por_faixas(consumo)
    
    # 2. Soma faixas (usando reduce)
    subtotal_consumo = reduce(lambda acc, f: acc + f['valor'], faixas_detalhadas, 0.0)
    
    # 3. Calcula bandeira
    adicional_bandeira = calcular_adicional_bandeira(subtotal_consumo, bandeira)
    
    # 4. Calcula impostos
    impostos_detalhados = calcular_impostos(base_impostos)
    
    # 5. Retorna resultado imutável
    return { ... }
```

### 5. **Validação com Funções Puras**

Sistema de validação modular e reutilizável:

```python
def validar_entradas(consumo: str, bandeira: str) -> Tuple:
    """Valida todas entradas sem efeitos colaterais"""
    valido_consumo, consumo_val, msg = validar_numero_positivo(consumo)
    if not valido_consumo:
        return (False, None, "", msg)
    
    valido_bandeira, msg = validar_bandeira(bandeira)
    if not valido_bandeira:
        return (False, None, "", msg)
    
    return (True, consumo_val, bandeira.lower(), "")
```

---

## 📊 Exemplos de Uso

### Exemplo 1: Consumo Baixo (Bandeira Verde)

**Entrada**:
- Consumo: 80 kWh
- Bandeira: Verde

**Saída**:
```
Consumo Total: 80.00 kWh
Bandeira Tarifária: Verde

DETALHAMENTO POR FAIXA:
  0-100 kWh          |    80.00 kWh × R$ 0.50 = R$      40.00

Subtotal Consumo:                                  R$      40.00
Adicional Bandeira Verde:                          R$       0.00
Base de Cálculo (Impostos):                        R$      40.00

IMPOSTOS:
  ICMS      (18.00%):                              R$       7.20
  PIS       ( 1.65%):                              R$       0.66
  COFINS    ( 7.61%):                              R$       3.04

Total Impostos:                                    R$      10.90

VALOR TOTAL DA FATURA:                             R$      50.90
```

### Exemplo 2: Consumo Médio (Bandeira Amarela)

**Entrada**:
- Consumo: 250 kWh
- Bandeira: Amarela

**Saída**:
```
Consumo Total: 250.00 kWh
Bandeira Tarifária: Amarela

DETALHAMENTO POR FAIXA:
  0-100 kWh          |   100.00 kWh × R$ 0.50 = R$      50.00
  100-200 kWh        |   100.00 kWh × R$ 0.75 = R$      75.00
  200-500 kWh        |    50.00 kWh × R$ 1.00 = R$      50.00

Subtotal Consumo:                                  R$     175.00
Adicional Bandeira Amarela:                        R$       8.75
Base de Cálculo (Impostos):                        R$     183.75

IMPOSTOS:
  ICMS      (18.00%):                              R$      33.08
  PIS       ( 1.65%):                              R$       3.03
  COFINS    ( 7.61%):                              R$      13.98

Total Impostos:                                    R$      50.09

VALOR TOTAL DA FATURA:                             R$     233.84
```
---

## ✅ Invariantes do Sistema

O sistema verifica automaticamente dois invariantes críticos:

1. **Total ≥ 0**: O valor total nunca pode ser negativo
2. **Soma correta**: `soma(faixas) + bandeira + impostos = total`

```python
def verificar_invariantes(resultado: Dict) -> bool:
    """Verifica integridade dos cálculos"""
    # Invariante 1: Total >= 0
    if resultado['total_final'] < 0:
        return False
    
    # Invariante 2: Soma deve bater
    soma_faixas = reduce(lambda acc, f: acc + f['valor'], resultado['faixas'], 0.0)
    recalculo = soma_faixas + resultado['adicional_bandeira'] + resultado['total_impostos']
    diferenca = abs(recalculo - resultado['total_final'])
    
    return diferenca < 0.01  # Permite margem por arredondamento
```

---

## 🏗️ Arquitetura do Sistema

### Estrutura do Código

```
faturamento_energia.py
│
├── CONFIGURAÇÕES E CONSTANTES
│   ├── TARIFAS_FAIXAS (tupla imutável)
│   ├── BANDEIRAS (dicionário imutável)
│   └── IMPOSTOS (dicionário imutável)
│
├── FUNÇÕES PURAS DE VALIDAÇÃO
│   ├── validar_numero_positivo()
│   ├── validar_bandeira()
│   └── validar_entradas()
│
├── FUNÇÕES PURAS DE CÁLCULO
│   ├── calcular_faixa()
│   ├── calcular_tarifacao_por_faixas()
│   ├── calcular_adicional_bandeira()
│   ├── calcular_imposto()
│   ├── calcular_impostos()
│   ├── calcular_faturamento()
│   └── verificar_invariantes()
│
└── INTERFACE GRÁFICA
    └── SistemaFaturamentoEnergia (classe)
        ├── criar_interface()
        ├── calcular()
        └── exibir_resultado()
```

## 🔍 Detalhes de Implementação

### Por que Funções Puras?

```python
# ❌ Função IMPURA (modifica estado global)
total_global = 0

def calcular_ruim(valor):
    global total_global
    total_global += valor  # Efeito colateral!
    return total_global

# ✅ Função PURA (sem efeitos colaterais)
def calcular_bom(valor, total_anterior):
    return total_anterior + valor  # Apenas retorna novo valor
```

### Por que Imutabilidade?

```python
# ❌ Modificando estrutura original
def processar_ruim(dados):
    dados['total'] = 100  # Modifica o original!
    return dados

# ✅ Criando nova estrutura
def processar_bom(dados):
    return {**dados, 'total': 100}  # Retorna cópia com modificação
```

### Vantagens da Abordagem Funcional

1. **Testabilidade**: Funções puras são fáceis de testar
2. **Previsibilidade**: Mesmo input sempre gera mesmo output
3. **Paralelização**: Funções puras podem ser executadas em paralelo
4. **Debugging**: Mais fácil rastrear bugs sem efeitos colaterais
5. **Manutenibilidade**: Código mais modular e reutilizável

---

## 🧪 Casos de Teste

### Teste 1: Validação de Entrada Inválida
```python
# Entrada: "abc"
# Esperado: (False, None, "Valor inválido. Digite um número válido")
```

### Teste 2: Consumo Zero
```python
# Entrada: 0 kWh, Verde
# Esperado: Total = 0.00
```

### Teste 3: Múltiplas Faixas
```python
# Entrada: 250 kWh, Verde
# Esperado: 
#   - Faixa 1: 100 kWh × 0.50 = 50.00
#   - Faixa 2: 100 kWh × 0.75 = 75.00
#   - Faixa 3: 50 kWh × 1.00 = 50.00
#   - Subtotal: 175.00
```

### Teste 4: Invariantes
```python
# Para qualquer entrada válida:
# assert total_final >= 0
# assert abs(soma_faixas + bandeira + impostos - total) < 0.01
```

---

## 📚 Conceitos Teóricos Aplicados

### 1. Transparência Referencial

Uma expressão é referencialmente transparente se pode ser substituída por seu valor sem mudar o comportamento do programa.

```python
# Esta função tem transparência referencial
valor1 = calcular_imposto(100, 0.18)
valor2 = calcular_imposto(100, 0.18)
# valor1 == valor2 sempre!
```

### 2. Composição de Funções

```python
# f(g(x)) - composição matemática
resultado = calcular_faturamento(
    validar_entradas(input_usuario)[1],  # g(x)
    "verde"
)  # f(g(x))
```

### 3. Higher-Order Functions

Funções que recebem ou retornam outras funções:

```python
# map é uma função de ordem superior
map(lambda x: x * 2, [1, 2, 3])  # [2, 4, 6]

# reduce também
reduce(lambda acc, x: acc + x, [1, 2, 3], 0)  # 6
```

### Sobre o Código

Este projeto foi desenvolvido com foco em **conceitos de programação funcional** para fins educacionais.
