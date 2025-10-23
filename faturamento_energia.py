"""
Sistema de Faturamento de Energia Elétrica
Programação Funcional - Python

Desenvolvido por: Carlos H. A. Weege
GitHub: @CarlosWeg

Este sistema calcula o faturamento de energia elétrica aplicando:
- Tarifação progressiva por faixas de consumo
- Bandeiras tarifárias (verde, amarela, vermelha)
- Impostos (ICMS, PIS, COFINS)
- Princípios de Programação Funcional
"""

import tkinter as tk
from tkinter import ttk, messagebox
from functools import reduce
from typing import Dict, List, Tuple, Optional

# ============================================================================
# CONFIGURAÇÕES E CONSTANTES (Imutáveis)
# ============================================================================

# Faixas de tarifação progressiva (kWh, tarifa por kWh em R$)
TARIFAS_FAIXAS = (
    (0, 100, 0.50),  # Até 100 kWh: R$ 0,50/kWh
    (100, 200, 0.75),  # 101-200 kWh: R$ 0,75/kWh
    (200, 500, 1.00),  # 201-500 kWh: R$ 1,00/kWh
    (500, float('inf'), 1.35)  # Acima de 500 kWh: R$ 1,35/kWh
)

# Bandeiras tarifárias (adicional em R$ por kWh)
BANDEIRAS = {
    'verde': 0.0,
    'amarela': 0.05,
    'vermelha': 0.10
}

# Alíquotas de impostos (percentuais)
IMPOSTOS = {
    'ICMS': 0.18,  # 18%
    'PIS': 0.0165,  # 1.65%
    'COFINS': 0.0761  # 7.61%
}


# ============================================================================
# FUNÇÕES PURAS DE VALIDAÇÃO
# ============================================================================

def validar_numero_positivo(valor: str) -> Tuple[bool, Optional[float], str]:
    """
    Função pura para validar se um valor é numérico e positivo.

    Args:
        valor: String contendo o valor a ser validado

    Returns:
        Tupla (é_válido, valor_convertido, mensagem_erro)
    """
    try:
        num = float(valor.replace(',', '.'))
        if num < 0:
            return (False, None, "O valor deve ser positivo")
        return (True, num, "")
    except ValueError:
        return (False, None, "Valor inválido. Digite um número válido")


def validar_bandeira(bandeira: str) -> Tuple[bool, str]:
    """
    Função pura para validar a bandeira tarifária.

    Args:
        bandeira: Nome da bandeira

    Returns:
        Tupla (é_válida, mensagem_erro)
    """
    bandeira_lower = bandeira.lower()
    if bandeira_lower in BANDEIRAS:
        return (True, "")
    return (False, f"Bandeira inválida. Use: {', '.join(BANDEIRAS.keys())}")


def validar_entradas(consumo: str, bandeira: str) -> Tuple[bool, Optional[float], str, str]:
    """
    Função pura que valida todas as entradas do usuário.

    Args:
        consumo: Consumo em kWh (string)
        bandeira: Bandeira tarifária

    Returns:
        Tupla (sucesso, consumo_validado, bandeira_validada, mensagem_erro)
    """
    valido_consumo, consumo_val, msg_consumo = validar_numero_positivo(consumo)

    if not valido_consumo:
        return (False, None, "", msg_consumo)

    valido_bandeira, msg_bandeira = validar_bandeira(bandeira)

    if not valido_bandeira:
        return (False, None, "", msg_bandeira)

    return (True, consumo_val, bandeira.lower(), "")


# ============================================================================
# FUNÇÕES PURAS DE CÁLCULO
# ============================================================================

def calcular_faixa(consumo_restante: float, faixa: Tuple[float, float, float]) -> Tuple[float, float]:
    """
    Função pura para calcular o valor de uma faixa de consumo.

    Args:
        consumo_restante: kWh restantes para calcular
        faixa: Tupla (inicio, fim, tarifa)

    Returns:
        Tupla (kwh_consumido_nesta_faixa, valor_faixa)
    """
    inicio, fim, tarifa = faixa
    kwh_faixa = fim - inicio
    kwh_usado = min(consumo_restante, kwh_faixa)
    valor = kwh_usado * tarifa
    return (kwh_usado, valor)


def calcular_tarifacao_por_faixas(consumo: float) -> List[Dict[str, float]]:
    """
    Função pura que calcula a tarifação progressiva por faixas.
    Usa map para processar cada faixa.

    Args:
        consumo: Total de kWh consumido

    Returns:
        Lista de dicionários com breakdown por faixa
    """
    consumo_restante = consumo
    resultados = []

    for faixa in TARIFAS_FAIXAS:
        if consumo_restante <= 0:
            break

        kwh_usado, valor = calcular_faixa(consumo_restante, faixa)

        if kwh_usado > 0:
            resultados.append({
                'faixa': f"{int(faixa[0])}-{int(faixa[1]) if faixa[1] != float('inf') else '∞'} kWh",
                'kwh': kwh_usado,
                'tarifa': faixa[2],
                'valor': valor
            })

        consumo_restante -= kwh_usado

    return resultados


def calcular_adicional_bandeira(subtotal: float, bandeira: str) -> float:
    """
    Função pura para calcular o adicional da bandeira tarifária.

    Args:
        subtotal: Valor base do consumo
        bandeira: Nome da bandeira

    Returns:
        Valor adicional da bandeira
    """
    return subtotal * BANDEIRAS[bandeira]


def calcular_imposto(base_calculo: float, aliquota: float) -> float:
    """
    Função pura para calcular um imposto individual.

    Args:
        base_calculo: Valor base para cálculo
        aliquota: Percentual do imposto (ex: 0.18 para 18%)

    Returns:
        Valor do imposto
    """
    return base_calculo * aliquota


def calcular_impostos(base_calculo: float) -> Dict[str, float]:
    """
    Função pura que calcula todos os impostos.
    Usa map para aplicar o cálculo a cada imposto.

    Args:
        base_calculo: Valor base (consumo + bandeira)

    Returns:
        Dicionário com breakdown de impostos
    """
    # Usando map para calcular cada imposto
    impostos_calculados = dict(
        map(
            lambda item: (item[0], calcular_imposto(base_calculo, item[1])),
            IMPOSTOS.items()
        )
    )
    return impostos_calculados


def calcular_faturamento(consumo: float, bandeira: str) -> Dict:
    """
    Função pura principal que orquestra todo o cálculo do faturamento.

    Args:
        consumo: Consumo em kWh
        bandeira: Bandeira tarifária

    Returns:
        Dicionário completo com todos os detalhes do faturamento
    """
    # Calcula tarifação por faixas
    faixas_detalhadas = calcular_tarifacao_por_faixas(consumo)

    # Usa reduce para somar todos os valores das faixas
    subtotal_consumo = reduce(
        lambda acc, faixa: acc + faixa['valor'],
        faixas_detalhadas,
        0.0
    )

    # Calcula adicional da bandeira
    adicional_bandeira = calcular_adicional_bandeira(subtotal_consumo, bandeira)

    # Base de cálculo para impostos
    base_impostos = subtotal_consumo + adicional_bandeira

    # Calcula impostos
    impostos_detalhados = calcular_impostos(base_impostos)

    # Usa reduce para somar todos os impostos
    total_impostos = reduce(
        lambda acc, valor: acc + valor,
        impostos_detalhados.values(),
        0.0
    )

    # Total final
    total_final = base_impostos + total_impostos

    # Retorna estrutura imutável (dicionário novo)
    return {
        'consumo_kwh': consumo,
        'bandeira': bandeira,
        'faixas': faixas_detalhadas,
        'subtotal_consumo': subtotal_consumo,
        'adicional_bandeira': adicional_bandeira,
        'base_impostos': base_impostos,
        'impostos': impostos_detalhados,
        'total_impostos': total_impostos,
        'total_final': total_final
    }


def verificar_invariantes(resultado: Dict) -> bool:
    """
    Função pura para verificar os invariantes do sistema.
    - Total deve ser >= 0
    - Soma(faixas) + impostos == total

    Args:
        resultado: Dicionário com resultado do cálculo

    Returns:
        True se invariantes são respeitados
    """
    # Invariante 1: Total >= 0
    if resultado['total_final'] < 0:
        return False

    # Invariante 2: Soma deve bater
    soma_faixas = reduce(
        lambda acc, f: acc + f['valor'],
        resultado['faixas'],
        0.0
    )

    recalculo = soma_faixas + resultado['adicional_bandeira'] + resultado['total_impostos']
    diferenca = abs(recalculo - resultado['total_final'])

    # Permite diferença mínima por arredondamento
    return diferenca < 0.01


# ============================================================================
# INTERFACE GRÁFICA
# ============================================================================

class SistemaFaturamentoEnergia:
    """
    Classe para a interface gráfica do sistema.
    Mantém separação entre lógica (funções puras) e apresentação.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Faturamento de Energia Elétrica")
        self.root.geometry("800x700")
        self.root.resizable(False, False)

        self.criar_interface()

    def criar_interface(self):
        """Cria todos os elementos da interface."""

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        titulo = ttk.Label(main_frame, text="💡 Faturamento de Energia Elétrica",
                           font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Entrada: Consumo
        ttk.Label(main_frame, text="Consumo (kWh):", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.entry_consumo = ttk.Entry(main_frame, width=30)
        self.entry_consumo.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Entrada: Bandeira
        ttk.Label(main_frame, text="Bandeira Tarifária:", font=('Arial', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.combo_bandeira = ttk.Combobox(main_frame, width=28,
                                           values=list(BANDEIRAS.keys()),
                                           state='readonly')
        self.combo_bandeira.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.combo_bandeira.current(0)

        # Botão Calcular
        btn_calcular = ttk.Button(main_frame, text="Calcular Faturamento",
                                  command=self.calcular)
        btn_calcular.grid(row=3, column=0, columnspan=2, pady=20)

        # Área de resultado
        ttk.Label(main_frame, text="Resultado:", font=('Arial', 12, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        # Text widget com scrollbar
        frame_resultado = ttk.Frame(main_frame)
        frame_resultado.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(frame_resultado)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_resultado = tk.Text(frame_resultado, height=20, width=70,
                                      yscrollcommand=scrollbar.set,
                                      font=('Courier', 9))
        self.text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_resultado.yview)

        # Rodapé
        rodape = ttk.Label(main_frame,
                           text="Desenvolvido por: Carlos H. A. Weege | GitHub: @CarlosWeg",
                           font=('Arial', 8), foreground='gray')
        rodape.grid(row=6, column=0, columnspan=2, pady=(20, 0))

    def calcular(self):
        """Processa o cálculo quando o botão é clicado."""
        consumo_str = self.entry_consumo.get()
        bandeira = self.combo_bandeira.get()

        # Validação usando funções puras
        valido, consumo, bandeira_validada, erro = validar_entradas(consumo_str, bandeira)

        if not valido:
            messagebox.showerror("Erro de Validação", erro)
            return

        # Cálculo usando funções puras
        resultado = calcular_faturamento(consumo, bandeira_validada)

        # Verifica invariantes
        if not verificar_invariantes(resultado):
            messagebox.showerror("Erro", "Falha na verificação dos invariantes!")
            return

        # Exibe resultado
        self.exibir_resultado(resultado)

    def exibir_resultado(self, resultado: Dict):
        """Exibe o resultado formatado na interface."""
        self.text_resultado.delete(1.0, tk.END)

        output = []
        output.append("=" * 70)
        output.append("FATURA DE ENERGIA ELÉTRICA".center(70))
        output.append("=" * 70)
        output.append(f"\nConsumo Total: {resultado['consumo_kwh']:.2f} kWh")
        output.append(f"Bandeira Tarifária: {resultado['bandeira'].capitalize()}\n")

        output.append("-" * 70)
        output.append("DETALHAMENTO POR FAIXA DE CONSUMO")
        output.append("-" * 70)

        for faixa in resultado['faixas']:
            output.append(f"  {faixa['faixa']:<20} | "
                          f"{faixa['kwh']:>8.2f} kWh × R$ {faixa['tarifa']:.2f} = "
                          f"R$ {faixa['valor']:>10.2f}")

        output.append(f"\nSubtotal Consumo: {' ' * 37} R$ {resultado['subtotal_consumo']:>10.2f}")
        output.append(f"Adicional Bandeira {resultado['bandeira'].capitalize()}: "
                      f"{' ' * 25} R$ {resultado['adicional_bandeira']:>10.2f}")
        output.append(f"{'─' * 70}")
        output.append(f"Base de Cálculo (Impostos): {' ' * 28} R$ {resultado['base_impostos']:>10.2f}\n")

        output.append("-" * 70)
        output.append("IMPOSTOS")
        output.append("-" * 70)

        for nome, valor in resultado['impostos'].items():
            percentual = IMPOSTOS[nome] * 100
            output.append(f"  {nome:<10} ({percentual:>5.2f}%): {' ' * 30} R$ {valor:>10.2f}")

        output.append(f"\nTotal Impostos: {' ' * 42} R$ {resultado['total_impostos']:>10.2f}")

        output.append("\n" + "=" * 70)
        output.append(f"VALOR TOTAL DA FATURA: {' ' * 33} R$ {resultado['total_final']:>10.2f}")
        output.append("=" * 70)

        self.text_resultado.insert(1.0, "\n".join(output))


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaFaturamentoEnergia(root)
    root.mainloop()