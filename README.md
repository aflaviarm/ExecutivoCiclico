
# Escalonamento de Tarefas com Executivo Cíclico

## Visão Geral

Este projeto implementa um algoritmo de escalonamento de tarefas usando a heurística SETF (Menor Tempo de Execução Primeiro) e o Executivo Cíclico. O sistema é capaz de calcular os tempos de ciclo primário e secundário com base nos períodos das tarefas e sugerir um escalonamento adequado.

## Detalhamento do Design

O sistema é composto por várias funções em Python que realizam diferentes etapas do processo de escalonamento:

- `calcular_mmc(periodos)`: Calcula o Mínimo Múltiplo Comum (MMC) de uma lista de períodos.
- `calcular_mdc(periodos)`: Calcula o Maior Divisor Comum (MDC) de uma lista de períodos.
- `calcular_tempo_ciclo_primario_e_secundario(periodos, maiores_tempos_execucao)`: Calcula o tempo de ciclo primário e secundário com base nos períodos das tarefas.
- `ultima_execucao(tarefa, ciclos, ciclo_atual, tempo_atual)`: Determina o tempo da última execução de uma tarefa.
- `ordenar_tarefas_por_setf(tarefas, tempo_ciclo_primario, tempo_ciclo_secundario)`: Ordena as tarefas por SETF e distribui as tarefas em ciclos.
- `ler_dados_entrada(caminho_arquivo)`: Lê os dados de entrada de um arquivo JSON.
- `imprimir_resultados(tempo_ciclo_primario, tempo_ciclo_secundario, ciclos)`: Imprime os resultados formatados na saída padrão.

O sistema segue os seguintes passos principais:

1. Lê os dados de entrada de um arquivo JSON que contém as informações das tarefas.
2. Calcula os tempos de ciclo primário e secundário com base nos períodos das tarefas.
3. Ordena as tarefas por SETF e distribui as tarefas em ciclos.
4. Imprime os resultados formatados na saída padrão.

## Decisões de Implementação

- A heurística SETF (Menor Tempo de Execução Primeiro) foi escolhida para ordenar as tarefas, priorizando as tarefas com menor tempo de execução.
- O algoritmo do Executivo Cíclico é utilizado para dividir as tarefas em ciclos de execução, garantindo que os períodos das tarefas sejam respeitados.

## Instruções para Executar o Sistema

1. Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).

2. Clone este repositório para o seu ambiente local:

    ```bash
    git clone https://github.com/aflaviarm/ExecutivoCiclico.git
    ```

3. Navegue até o diretório do projeto:

    ```bash
    cd ExecutivoCiclico
    ```

4. Execute o script Python `main.py`:

    ```bash
    python main.py
    ```

5. O resultado do escalonamento será exibido no terminal.
