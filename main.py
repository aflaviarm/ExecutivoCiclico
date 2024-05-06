import json
import math

def calcular_mmc(periodos):
    """
    Calcula o Mínimo Múltiplo Comum (MMC) de uma lista de períodos.

    Parâmetros:
        periodos (list): Uma lista de períodos das tarefas.

    Retorna:
        int: O Mínimo Múltiplo Comum (MMC) dos períodos.
    """

    def gcd(a, b):
        """Calcula o Maior Divisor Comum (MDC) de dois números."""
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        """Calcula o Mínimo Múltiplo Comum (MMC) de dois números."""
        return a * b // gcd(a, b)

    mmc = 1
    for periodo in periodos:
        mmc = lcm(mmc, periodo)
    return mmc


def calcular_mdc(periodos):
    """
    Calcula o Maior Divisor Comum (MDC) de uma lista de períodos.

    Parâmetros:
        periodos (list): Uma lista de períodos das tarefas.

    Retorna:
        int: O Maior Divisor Comum (MDC) dos períodos.
    """
    mdc = periodos[0]
    for periodo in periodos[1:]:
        mdc = math.gcd(mdc, periodo)
    return mdc


def calcular_tempo_ciclo_primario_e_secundario(periodos, maiores_tempos_execucao):
    """
    Calcula o tempo de ciclo primário e secundário com base nos períodos das tarefas.

    Parâmetros:
        periodos (list): Uma lista de períodos das tarefas.
        maiores_tempos_execucao (list): Uma lista dos maiores tempos de execução das tarefas.

    Retorna:
        tuple: Uma tupla contendo o tempo de ciclo primário e o tempo de ciclo secundário.
    """
    mmc = calcular_mmc(periodos)
    mdc = calcular_mdc(periodos)

    # Requisito 1: O tamanho do frame deve ser maior ou igual ao maior tempo de execução de uma tarefa
    tamanho_frame = max(maiores_tempos_execucao)

    # Requisito 2: O tamanho de frames candidatos deve caber igualmente dentro de um ciclo maior
    tempo_ciclo_primario = mmc
    tempo_ciclo_secundario = mdc

    # Requisito 3: Deve existir um frame entre o release-time(t') e o deadline (t'+Di) de todos os jobs
    while (2 * tamanho_frame - tempo_ciclo_primario) > tempo_ciclo_secundario:
        tempo_ciclo_secundario += mdc

    return tempo_ciclo_primario, tempo_ciclo_secundario


def ultima_execucao(tarefa, ciclos, ciclo_atual, tempo_atual):
    ultima_exec = -1  # Inicializa com -1 para indicar que a tarefa ainda não foi executada
    if len(ciclos) == 0:
        return ultima_exec

    for task in ciclo_atual:
        if task['id'] == tarefa['id']:
            ultima_exec = -2
            return ultima_exec

    for num_ciclo, ciclo in reversed(list(enumerate(ciclos))):
        for posicao, t in enumerate(ciclo):
            if t['id'] == tarefa['id']:
                if len(ciclos) == 1 or num_ciclo == (len(ciclos)-1):
                    ultima_exec = (tempo_ciclo_secundario + tempo_atual) - sum(t['tempo_execucao'] for t in ciclo[:posicao])
                else:
                    ultima_exec = ((len(ciclos) - (num_ciclo+1)) * tempo_ciclo_secundario) + ((tempo_ciclo_secundario + tempo_atual) - sum(t['tempo_execucao'] for t in ciclo[:posicao]))

                return ultima_exec
    return ultima_exec


def ordenar_tarefas_por_setf(tarefas, tempo_ciclo_primario, tempo_ciclo_secundario):
    """
    Ordena as tarefas de acordo com a heurística SETF (Menor Tempo de Execução Primeiro) e distribui as tarefas em ciclos.

    Parâmetros:
        tarefas (list): Uma lista de dicionários representando as tarefas, cada dicionário contendo os seguintes campos:
                        - id: identificador único para cada tarefa.
                        - periodo: o período de cada tarefa.
                        - tempo_execucao: o tempo necessário para completar a tarefa.
                        - prioridade: um número que indica a prioridade da tarefa.
        tempo_ciclo_primario (int): O tempo de ciclo primário calculado.
        tempo_ciclo_secundario (int): O tempo de ciclo secundário calculado.

    Retorna:
        list: Uma lista de ciclos, cada ciclo contendo uma lista de tarefas a serem executadas dentro desse ciclo.
    """
    # Ordena as tarefas por prioridade (maior prioridade primeiro), por período (menor período primeiro) e, em seguida, por tempo de execução (menor tempo primeiro)
    tarefas_ordenadas = sorted(tarefas, key=lambda x: (-x['prioridade'], -x['periodo']))

    ciclos = []

    # Distribui as tarefas em múltiplos ciclos de acordo com os tempos de ciclo primário e secundário
    while tarefas_ordenadas:
        ciclo_atual = []
        tempo_atual = 0
        recomece_for = 1
        while recomece_for:

            if not tarefas_ordenadas:
                break

            for tarefa in tarefas_ordenadas[:]:

                if tempo_atual + tarefa['tempo_execucao'] <= tempo_ciclo_secundario:
                    execucao = ultima_execucao(tarefa, ciclos, ciclo_atual, tempo_atual)

                    if execucao == -2:

                        if len(tarefas_ordenadas) == 1:
                            recomece_for = 0
                        else:
                            continue

                    if (execucao >= tarefa['periodo']) or execucao == -1:
                        ciclo_atual.append(tarefa)
                        tempo_atual += tarefa['tempo_execucao']

                        if (len(ciclos)*tempo_ciclo_secundario + tarefa['periodo']) >= tempo_ciclo_primario:
                            tarefas_ordenadas.remove(tarefa)

                        if recomece_for == 0:
                            recomece_for = 1
                            break

                    else:
                        recomece_for = 0
                        continue

                else:
                    recomece_for = 0
                    break

        ciclos.append(ciclo_atual)

    return ciclos


def ler_dados_entrada(caminho_arquivo):
    """
    Lê os dados de entrada do arquivo JSON fornecido.

    Parâmetros:
        caminho_arquivo (str): O caminho do arquivo JSON de entrada.

    Retorna:
        list: Uma lista de dicionários representando as tarefas, cada dicionário contendo os seguintes campos:
              - id: identificador único para cada tarefa.
              - periodo: o período de cada tarefa.
              - tempo_execucao: o tempo necessário para completar a tarefa.
              - prioridade: um número que indica a prioridade da tarefa.
    """
    with open(caminho_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)
    return dados['tarefas']


def imprimir_resultados(tempo_ciclo_primario, tempo_ciclo_secundario, ciclos):
    """
    Imprime os resultados formatados na saída padrão.

    Parâmetros:
        tempo_ciclo_primario (int): O tempo de ciclo primário calculado.
        tempo_ciclo_secundario (int): O tempo de ciclo secundário calculado.
        ciclos (list): Uma lista de ciclos, cada ciclo contendo uma lista de tarefas a serem executadas dentro desse ciclo.
    """
    print("Cálculo de Ciclos para o Executivo Cíclico:")
    print("-------------------------------------------")
    print(f"Tempo de Ciclo Primário: {tempo_ciclo_primario} unidades de tempo")
    print(f"Tempo de Ciclo Secundário: {tempo_ciclo_secundario} unidades de tempo")
    print("\nEscalonamento Sugerido (Heurística: Menor Tempo de Execução Primeiro):")
    print("----------------------------------------------------------------------")
    for i, ciclo in enumerate(ciclos, start=1):
        print(f"\nCiclo {i}:")
        for tarefa in ciclo:
            print(
                f"  - {tarefa['id']}: tempo de execução = {tarefa['tempo_execucao']}, período = {tarefa['periodo']}, prioridade = {tarefa['prioridade']}")
    print("\nResumo:")
    print("-------")
    print(f"Total de Ciclos: {len(ciclos)}")
    print(f"Total de Intercâmbios de Tarefa por Ciclo: {sum(len(ciclo) for ciclo in ciclos)}")
    utilizacao_cpu = (sum(
        tarefa['tempo_execucao'] for ciclo in ciclos for tarefa in ciclo) / tempo_ciclo_primario) * 100
    print(f"Utilização da CPU: {utilizacao_cpu}%")




# Caminho do arquivo JSON de entrada
caminho_arquivo = "entrada.json"

# Ler os dados de entrada do arquivo JSON
tarefas = ler_dados_entrada(caminho_arquivo)

# Calcular os tempos de ciclo primário e secundário
tempo_ciclo_primario, tempo_ciclo_secundario = calcular_tempo_ciclo_primario_e_secundario(
    [tarefa['periodo'] for tarefa in tarefas], [tarefa['tempo_execucao'] for tarefa in tarefas])

# Ordenar as tarefas por SETF e dividir em ciclos
ciclos = ordenar_tarefas_por_setf(tarefas, tempo_ciclo_primario, tempo_ciclo_secundario)

# Imprimir os resultados formatados
imprimir_resultados(tempo_ciclo_primario, tempo_ciclo_secundario, ciclos)
