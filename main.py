################
# LEITURA E ANÁLISE DO ARQUIVO DE ENTRADA
###############

import json

def ler_arquivo_de_entrada(nome_arquivo):
    try:
        # Abrir o arquivo JSON
        with open(nome_arquivo, 'r') as arquivo:
            # Carregar o conteúdo do arquivo JSON
            dados = json.load(arquivo)
            # Verificar se o arquivo contém a chave "tarefas"
            if 'tarefas' in dados:
                # Retornar a lista de tarefas
                return dados['tarefas']
            else:
                print("Erro: Arquivo de entrada não contém a chave 'tarefas'.")
                return None
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None

# Exemplo de uso da função
nome_arquivo = 'entrada.json'  # Substitua pelo nome do seu arquivo de entrada
tarefas = ler_arquivo_de_entrada(nome_arquivo)
if tarefas:
    print("Tarefas encontradas no arquivo de entrada:")
    for tarefa in tarefas:
        print(tarefa)


################
# CÁLCULO DOS TEMPOS DE CICLO PRIMÁRIO E SECUNDÁRIO
###############


from math import gcd

def calcular_mdc(lista_numeros):
    """
    Calcula o Máximo Divisor Comum (MDC) de uma lista de números.
    """
    mdc = lista_numeros[0]
    for numero in lista_numeros[1:]:
        mdc = gcd(mdc, numero)
    return mdc

def calcular_mmc(lista_numeros):
    """
    Calcula o Mínimo Múltiplo Comum (MMC) de uma lista de números.
    """
    mmc = lista_numeros[0]
    for numero in lista_numeros[1:]:
        mmc = mmc * numero // gcd(mmc, numero)
    return mmc

# Função para calcular os tempos de ciclo
def calcular_tempos_de_ciclo(tarefas):
    # Extrair os períodos das tarefas
    periodos = [tarefa['periodo'] for tarefa in tarefas]
    # Calcular o MDC e o MMC dos períodos
    mdc = calcular_mdc(periodos)
    mmc = calcular_mmc(periodos)
    return mdc, mmc

# Exemplo de uso da função
if tarefas:
    mdc, mmc = calcular_tempos_de_ciclo(tarefas)
    print("Tempos de ciclo calculados:")
    print("Tempo de Ciclo Primário:", mmc)
    print("Tempo de Ciclo Secundário:", mdc)



################
# APLICAÇÃO DA HEURÍSTICA DE ESCALONAMENTO
###############


# Função para aplicar a heurística SETF (Menor Tempo de Execução Primeiro)
def setf(tarefas):
    # Ordenar as tarefas pelo tempo de execução, em ordem crescente
    tarefas_ordenadas = sorted(tarefas, key=lambda x: x['tempo_execucao'])
    return tarefas_ordenadas

# Exemplo de uso da função
if tarefas:
    print("Escalonamento sugerido (Heurística: Menor Tempo de Execução Primeiro):")
    escalonamento = setf(tarefas)
    for ciclo, tarefa in enumerate(escalonamento, start=1):
        print(f"Ciclo {ciclo}:")
        print(f"  - Tarefa {tarefa['id']}: tempo de execução = {tarefa['tempo_execucao']}, período = {tarefa['periodo']}, prioridade = {tarefa['prioridade']}")




################
# APRESENTAÇÃO DOS RESULTADOS
###############


# Função para apresentar os resultados finais
def apresentar_resultados(mdc, mmc, escalonamento):
    # Calcular o número total de ciclos
    total_ciclos = mmc // mdc

    # Imprimir os tempos de ciclo calculados
    print("Cálculo de Ciclos para o Executivo Cíclico:")
    print("-------------------------------------------")
    print("Tempo de Ciclo Primário:", mmc, "unidades de tempo")
    print("Tempo de Ciclo Secundário:", mdc, "unidades de tempo")
    print()

    # Imprimir o escalonamento sugerido
    print("Escalonamento Sugerido (Heurística: Menor Tempo de Execução Primeiro):")
    print("----------------------------------------------------------------------")
    for ciclo in range(total_ciclos):
        print(f"Ciclo {ciclo + 1}:")
        for tarefa in escalonamento:
            print(
                f"  - Tarefa {tarefa['id']}: tempo de execução = {tarefa['tempo_execucao']}, período = {tarefa['periodo']}, prioridade = {tarefa['prioridade']}")
    print()

    # Imprimir o resumo
    print("Resumo:")
    print("-------")
    print("Total de Ciclos:", total_ciclos)
    print("Utilização da CPU:", "{:.0%}".format(len(escalonamento) / total_ciclos))
    print()


# Exemplo de uso da função
if tarefas:
    apresentar_resultados(mdc, mmc, escalonamento)

