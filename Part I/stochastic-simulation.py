# Disciplina: Simulação Estocástica
# Nome: Gustavo Silva Malvestiti
# Simulador - Parte I

# Pacote necessário: plotly
# Comando de instalação no terminal: pip install plotly

# Importações
from operator import iadd
from re import A

import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import time

# Varíavel para o cálculo do tempo de processamento
start_time = time.time()

# Plotagem de pontos
def plot(v):
    valores = np.array_split(v, 2)

    if len(valores[0]) > len(valores[1]):
        valores[0].pop(0)

    if len(valores[1]) > len(valores[0]):
        valores[1].pop(0)
    
    plt.plot(valores[0], valores[1], 'ro')
    plt.axis([0, 1, 0, 1])
    plt.show()

# Gerador de números pseudo-aleatórios
class Generator():
    
    # Variáveis padrão do gerador
    # Offset para os 2 primeiros números gerados
    DEFAULT_OFFSET = 2
    # Quantidade padrão de números gerados
    DEFAULT_NUMBER_QUANTITY = 100000
    # Semente padrão do gerador caso uma semente não seja especificada
    DEFAULT_GENERATOR_SEED = 255
    
    # Inicialização do gerador
    def __init__(self, a, c, m, quantity = DEFAULT_NUMBER_QUANTITY, seed = DEFAULT_GENERATOR_SEED):
        self.a = a
        self.c = c
        self.m = m
        self.quantity = quantity
        self.seed = seed
        self.head = []
        self.values = []
    
    # Geração dos números pseudo-aleatórios
    def generate(self):
        x1 = self.seed
        x2 = 0
        
        for x in range(0, self.quantity):
            x2 = x1 / self.m
            self.head.append(x1)
            self.values.append(x2)
            x1 = ((self.a * x1) + self.c) % self.m
    
    # Cálculo da média dos números gerados
    def media(self):
        return np.mean(self.values)

    # Cálculo do desvio padrão dos números gerados
    def desvioPadrao(self):
        return np.std(self.values)

    # Cálculo da covariância dos números gerados
    def covariancia(self):
        return np.cov(self.values)

    # Cálculo do qui-quadrado dos números gerados
    def quiQuadrado(self):
        somas = []
        for i in range(0, 10):
            somas.append(0)
            
        n = len(self.values) - self.DEFAULT_OFFSET
        
        for i in range(self.DEFAULT_OFFSET, n):
            value = self.values[i]
            
            if ((value == 0) or (value <= 0.1)):
                somas[0] += 1
            elif (value <= 0.2):
                somas[1] += 1
            elif (value <= 0.3):
                somas[2] += 1
            elif (value <= 0.4):
                somas[3] += 1
            elif (value <= 0.5):
                somas[4] += 1    
            elif (value <= 0.6):
                somas[5] += 1
            elif (value <= 0.7):
                somas[6] += 1
            elif (value <= 0.8):
                somas[7] += 1
            elif (value <= 0.9):
                somas[8] += 1
            else:
                somas[9] += 1
        
        qq = 0
        for i in range(0, 10):
            qq += math.pow((somas[i] - (n / 10)), 2) / (n / 10)

        return qq

    # Getters e Setters
    def setValues(self, new_value):
        self.values = new_value
    
    def getValues(self):
        return_values = self.values
        
        # Remoção dos n primeiros números gerados
        for i in range(self.DEFAULT_OFFSET):
            return_values.pop(0)
        
        return return_values
    
    def setA(self, new_a):
        self.a = new_a
    
    def getA(self):
        return self.a
    
    def setC(self, new_c):
        self.c = new_c
    
    def getC(self):
        return self.c
    
    def setM(self, new_m):
        self.m = new_m
    
    def getM(self):
        return self.m

# Simulador
class Simulador():
    
    # Variáveis padrão do simulador
    # Offset padrão da quantidade de veículos
    DEFAULT_RANGE_OFFSET = 1
    # Tempo padrão de simulação
    DEFAULT_SIMULATION_TIME = 3600
    # A padrão para o cálculo dos tempos de serviço
    DEFAULT_TS_A = 15
    # B padrão para o cálculo dos tempos de serviço
    DEFAULT_TS_B = 35
    # Flag para arredondar os resultados
    ROUND_NUMBER = False
    # Quantidade padrão de decimais
    DEFAULT_ROUND_DIGITS = 2
    
    # Inicialização do simulador
    def __init__(self, random, max_time = DEFAULT_SIMULATION_TIME, a = DEFAULT_TS_A, b = DEFAULT_TS_B):
        self.random_numbers = random
        self.max_time = max_time
        self.a = a
        self.b = b
        # Colunas de cada tabela do simulador
        self.array_tec = []
        self.array_ts = []
        self.clock_time = []
        self.start_time = []
        self.end_time = []
        self.queue_time = []
        self.system_time = []
        self.free_time = []

    # Retorna o número de veículos gerados
    def getRows(self):
        return len(self.array_tec)
    
    # Retorna um array ordenado de 1 até o número de veículos gerados
    # Coluna "Cliente" da tabela
    def getNumberArray(self):
        return np.arange(1, self.getRows() + self.DEFAULT_RANGE_OFFSET)

    # Converte valores de um array de números em uma string do número com duas casas decimais
    def twoDigits(self, values):
        for i in range(self.getRows()):
            values[i] = "{:.2f}".format(values[i])
        return values

    # Geração e visualização da tabela dos resultados do simulador
    def table(self):
        # Textos das colunas da tabela
        string_clock = 'Tempo do Relógio'
        string_start = 'Tempo de Início de Serviço'
        string_end = 'Tempo de Fim do Serviço'
        string_queue = 'Tempo na Fila'
        string_system = 'Tempo no Sistema'
        string_free = 'Tempo Livre'
        # Geração da tabela
        fig = go.Figure(data=[go.Table(header=dict(values=['Cliente', 'TEC', 'TS', string_clock, string_start, string_end, string_queue, string_system, string_free]), 
                        cells=dict(values=[self.getNumberArray(), self.twoDigits(self.array_tec), self.twoDigits(self.array_ts), self.twoDigits(self.clock_time), 
                        self.twoDigits(self.start_time), self.twoDigits(self.end_time), self.twoDigits(self.queue_time), self.twoDigits(self.system_time), 
                        self.twoDigits(self.free_time)]))])
        fig.show()

    # Retorno do tempo médio de chegada no sistema
    def getMediaTec(self):
        media_tec = 0
        for i in range(self.getRows()):
            media_tec += self.array_tec[i]
        return media_tec / self.getRows()

    # Retorno do tempo médio de espera na fila
    def getMediaQueue(self):
        return np.mean(self.queue_time)
    
    # Retorno do tempo médio de serviço
    def getMediaService(self):
        return np.mean(self.array_ts)
    
    # Retorno do tempo médio despendido no sistema
    def getMediaSystem(self):
        return np.mean(self.system_time)
    
    # Retorno da probabilidade de cancela livre
    def getProbFree(self):
        probabilidade_free = 0
        for i in range(self.getRows()):
            probabilidade_free += self.free_time[i]
        return probabilidade_free / self.max_time
    
    # Visualização dos tempos médios e probabilidade de cancela livre da simulação
    def print(self):
        STRING_SEGUNDOS = " segundos"
        print("\n" + "Tempo médio de espera na fila = " + str(self.getMediaQueue()) + STRING_SEGUNDOS)
        print("Tempo médio de serviço = " + str(self.getMediaService()) + STRING_SEGUNDOS)
        print("Tempo médio despendido no sistema = " + str(self.getMediaSystem()) + STRING_SEGUNDOS)
        print("Probabilidade de encontrar a cancela livre = " + str(self.getProbFree()) + "\n")

    # Realiza a simulação
    def simulate(self):
        # Limpeza dos arrays/colunas da tabela
        self.clearArrays()
        # Cálculo dos tempos de chegada
        self.calcTec()

        # Cálculo iterativo de cada coluna da simulação
        # Condição de parada da simulação
        cond = True
        # Índice atual dos arrays/linha da tabela de resultados
        index = 0
        # Início da simulação
        while (cond):
            # Cálculos
            # Tempo de serviço
            self.calcTs()
            # Tempo de chegada no relógio
            self.calcClock(index)
            # Tempo de início de serviço
            self.calcStart(index)
            # Tempo de final de serviço
            self.calcEnd(index)
            # Tempo na fila
            self.calcQueue(index)
            # Tempo no sistema
            self.calcSystem(index)
            # Tempo de cancela livre
            self.calcFree(index)
            
            # Verificação da condição de parada
            if (self.end_time[index] > self.max_time):
                cond = False
                self.trimmer(index)
            # Próximo índice/veículo
            index += 1
    
    # Limpeza dos arrays/colunas da tabela
    def clearArrays(self):
        self.array_tec.clear()
        self.array_ts.clear()
        self.clock_time.clear()
        self.start_time.clear()
        self.end_time.clear()
        self.queue_time.clear()
        self.system_time.clear()
        self.free_time.clear()
    
    # Retorno de um número pseudo-aleatório da array de números pseudo-aleatórios da simulação
    def getRandomNumber(self):
        return random.choice(self.random_numbers)

    # Retorna o número arrendodado para 2 casas decimais
    def roundNumber(self, number):
        if self.ROUND_NUMBER == True:
            return round(number)
        else:
            return round(number, self.DEFAULT_ROUND_DIGITS)
    
    # Cálculo dos tempos de chegada no sistema
    def calcTec(self):
        count = 0
        while (count < self.max_time):
            random_number = self.getRandomNumber()

            new_time = (-20) * math.log(float(random_number), math.e)
                
            self.array_tec.append(self.roundNumber(new_time))
            count += new_time
    
    # Cálculo dos tempos de serviço
    def calcTs(self):
        random_number = self.getRandomNumber()
        
        new_time = ((self.b - self.a) * float(random_number)) + self.a
        
        self.array_ts.append(self.roundNumber(new_time))

    # Retorno da contagem dos tempos de chegada até o determinado índice
    def getCountIndex(self, index):
        if (index == 0):
            return self.array_tec[index]
        
        count = 0
        for i in range(index + self.DEFAULT_RANGE_OFFSET):
            count += self.array_tec[i]
        return count
    
    # Cálculo dos tempos de chegada no relógio
    def calcClock(self, index):
        count = self.getCountIndex(index)
        
        self.clock_time.append(self.roundNumber(count))
    
    # Cálculo dos tempos de início de serviço
    def calcStart(self, index):
        if (index == 0):
            self.start_time.append(self.roundNumber(self.clock_time[index]))
        else:
            present_clock_time = self.clock_time[index]
            former_end_time = self.end_time[index - self.DEFAULT_RANGE_OFFSET]
            
            new_start_time = 0
            if (present_clock_time > former_end_time):
                new_start_time = present_clock_time
            else:
                new_start_time = former_end_time
            
            self.start_time.append(self.roundNumber(new_start_time))
    
    # Cálculo dos tempos de final de serviço
    def calcEnd(self, index):
        new_end_time = self.start_time[index] + self.array_ts[index]
        self.end_time.append(self.roundNumber(new_end_time))

    # Cálculo dos tempos na fila
    def calcQueue(self, index):
        self.queue_time.append(self.roundNumber(self.start_time[index] - self.clock_time[index]))
    
    # Cálculo dos tempos no sistema
    def calcSystem(self, index):
        self.system_time.append(self.roundNumber(self.queue_time[index] + self.array_ts[index]))

    # Cálculo dos tempos de cancela livre
    def calcFree(self, index):
        if (index == 0):
            self.free_time.append(self.roundNumber(self.start_time[index]))
        else:
            self.free_time.append(self.roundNumber(self.start_time[index] - self.end_time[index - self.DEFAULT_RANGE_OFFSET]))
    
    # Remove resultados da simulação caso tenham passado do tempo de simulação
    def trimmer(self, index):
        rows = self.getRows() - (index + self.DEFAULT_RANGE_OFFSET)
        for i in range(rows):
            self.array_tec.pop()

# Simulação
# Quantidad de sementes/simuladores
SEEDS_QTD = 130
# Semente base para a geração de novas sementes (mesma do Java)
BASE_MULTIPLIER = 25214903917
# Flag para mostrar os gráficos de um dos geradores
SHOW_PLOT = False
# Flag para mostrar as médias das propriedades estatísticas dos números pseudo-aleatórios gerados
SHOW_PROPERTIES_GENERATORS = True
# Tempo de simulação para todos os simuladores
SIMULATION_TIME = 3600
# Flag para mostrar tabela de resultados da simulação
SHOW_TABLE = True

# Geração das n sementes
seeds = []
for i in range(SEEDS_QTD):
    seeds.append(BASE_MULTIPLIER * random.random())

# Criação dos n geradores e geração de n arrays de números pseudo-aleatórios
generators = []
for i in range(SEEDS_QTD):
    generator = Generator(BASE_MULTIPLIER, 11, math.pow(2, 48), seed=seeds[i])
    generator.generate()
    generators.append(generator)

# Plotagem do gráfico dos números gerados no i-ésimo gerador e valo
if SHOW_PLOT == True:
    plot(generators[i].getValues())

# Exibição das médias das propriedades estatísticas dos números pseudo-aleatórios gerados
if SHOW_PROPERTIES_GENERATORS == True:
    propriedades_estatisticas = [0, 0, 0, 0]
    for i in range(SEEDS_QTD):
        propriedades_estatisticas[0] += generators[i].media()
        propriedades_estatisticas[1] += generators[i].desvioPadrao()
        propriedades_estatisticas[2] += generators[i].covariancia()
        propriedades_estatisticas[3] += generators[i].quiQuadrado()
    print("\n Propriedades estatísticas dos números pseudo-aleatórios gerados:" + "\n Média = " + str(propriedades_estatisticas[0]/SEEDS_QTD)
            + "\n Desvio padrão = " + str(propriedades_estatisticas[1]/SEEDS_QTD) + "\n Covariância = " + str(propriedades_estatisticas[2]/SEEDS_QTD)
            + "\n Qui-Quadrado = " + str(propriedades_estatisticas[3]/SEEDS_QTD))

# Criação dos n simuladores e realização de cada simulação
simulators = []
for i in range(SEEDS_QTD):
    values = generators[i].getValues()
    
    simulator = Simulador(values, SIMULATION_TIME)
    simulator.simulate()
    simulators.append(simulator)

# Criação dos arrays das médias dos tempos na fila, tempos no sistema e tempos de serviço de cada simulação
medias_fila = []
medias_sistema = []
medias_servico = []
medias_tec = []
for i in range(SEEDS_QTD):
    medias_fila.append(simulators[i].getMediaQueue())
    medias_sistema.append(simulators[i].getMediaSystem())
    medias_servico.append(simulators[i].getMediaService())
    medias_tec.append(simulators[i].getMediaTec())

# Cálculo das média das médias dos tempos na fila, tempos no sistema e tempos de serviço de cada simulação
media_das_medias_fila = np.mean(medias_fila)
media_das_medias_sistema = np.mean(medias_sistema)
media_das_medias_servico = np.mean(medias_servico)
media_das_medias_tec = np.mean(medias_tec)

# Desvios padrões das médias de dos tempos na fila, tempos no sistema e tempos de serviço de cada simulação
desvio_padrao_fila = np.std(medias_fila)
desvio_padrao_sistema = np.std(medias_sistema)
desvio_padrao_servico = np.std(medias_servico)
desvio_padrao_tec = np.std(medias_tec)

# Exibição da tabela de resultados da N-ésima simulação
if SHOW_TABLE == True:
    N = 0
    simulators[N].table()

# Cálculo dos intervalos de confiança
T_STUDENT = 1.96
intervalos_confianca = []
intervalos_confianca.append(media_das_medias_fila + (T_STUDENT * (desvio_padrao_fila / math.sqrt(SEEDS_QTD))))
intervalos_confianca.append(media_das_medias_fila - (T_STUDENT * (desvio_padrao_fila / math.sqrt(SEEDS_QTD))))
intervalos_confianca.append(media_das_medias_sistema + (T_STUDENT * (desvio_padrao_sistema / math.sqrt(SEEDS_QTD))))
intervalos_confianca.append(media_das_medias_sistema - (T_STUDENT * (desvio_padrao_sistema / math.sqrt(SEEDS_QTD))))
intervalos_confianca.append(media_das_medias_servico + (T_STUDENT * (desvio_padrao_servico / math.sqrt(SEEDS_QTD))))
intervalos_confianca.append(media_das_medias_servico - (T_STUDENT * (desvio_padrao_servico / math.sqrt(SEEDS_QTD))))

for i in range(len(intervalos_confianca)):
    intervalos_confianca[i] = round(intervalos_confianca[i], 2)
    intervalos_confianca[i] = "{:.2f}".format(intervalos_confianca[i])

# Exibição dos resultados
print("\n Quantidade de simuladores e sementes = " + str(SEEDS_QTD) + "\n Tempo de simulação = " + str(SIMULATION_TIME) + " segundos" +
      "\n Média dos tempos de chegada = " + str(media_das_medias_tec) + " segundos" + "\n" +
      "\n Intervalo de confiança do tempo de espera na fila:" +
      "\n + = " + str(intervalos_confianca[0]) + " segundos" + "\n - = " + str(intervalos_confianca[1]) + " segundos" + "\n" +
      "\n Intervalo de confiança do tempo despendido no sistema:" +
      "\n + = " + str(intervalos_confianca[2]) + " segundos" + "\n - = " + str(intervalos_confianca[3]) + " segundos" + "\n" +
      "\n Intervalo de confiança do tempo de serviço:" +
      "\n + = " + str(intervalos_confianca[4]) + " segundos" + "\n - = " + str(intervalos_confianca[5]) + " segundos" + "\n" +
      "\n Tempo de execução: " + str(time.time() - start_time) + " segundos" + "\n")