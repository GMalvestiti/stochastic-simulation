# Disciplina: Simulação Estocástica
# Nome: Gustavo Silva Malvestiti
# Simulador - Parte II

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
    def __init__(self, multiplier, increment, modulus, quantity = DEFAULT_NUMBER_QUANTITY, seed = DEFAULT_GENERATOR_SEED):
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = modulus
        self.quantity = quantity
        self.seed = seed
        self.head = []
        self.values = []
    
    # Geração dos números pseudo-aleatórios
    def generate(self):
        x1 = self.seed
        x2 = 0
        
        for _ in range(0, self.quantity):
            x2 = x1 / self.modulus
            self.head.append(x1)
            self.values.append(x2)
            x1 = ((self.multiplier * x1) + self.increment) % self.modulus
    
    # Cálculo da média dos números gerados
    def mean(self):
        return np.mean(self.values)

    # Cálculo do desvio padrão dos números gerados
    def standardDeviation(self):
        return np.std(self.values)

    # Cálculo da covariância dos números gerados
    def covariance(self):
        return np.cov(self.values)

    # Cálculo do qui-quadrado dos números gerados
    def chiSquare(self):
        sums = []
        for i in range(0, 10):
            sums.append(0)
            
        n = len(self.values) - self.DEFAULT_OFFSET
        
        for i in range(self.DEFAULT_OFFSET, n):
            value = self.values[i]
            
            if ((value == 0) or (value <= 0.1)):
                sums[0] += 1
            elif (value <= 0.2):
                sums[1] += 1
            elif (value <= 0.3):
                sums[2] += 1
            elif (value <= 0.4):
                sums[3] += 1
            elif (value <= 0.5):
                sums[4] += 1    
            elif (value <= 0.6):
                sums[5] += 1
            elif (value <= 0.7):
                sums[6] += 1
            elif (value <= 0.8):
                sums[7] += 1
            elif (value <= 0.9):
                sums[8] += 1
            else:
                sums[9] += 1
        
        cs = 0
        for i in range(0, 10):
            cs += math.pow((sums[i] - (n / 10)), 2) / (n / 10)

        return cs

    # Getters e Setters
    def setValues(self, new_value):
        self.values = new_value
    
    # Remoção dos n primeiros números gerados
    def removeNumbers(self, values):
        for i in range(self.DEFAULT_OFFSET):
            values.pop(0)
        return values
    
    def getValues(self):
        return self.removeNumbers(self.values)
    
    def setMultiplier(self, multiplier):
        self.multiplier = multiplier
    
    def getMultiplier(self):
        return self.multiplier
    
    def setIncrement(self, increment):
        self.increment = increment
    
    def getIncrement(self):
        return self.increment
    
    def setModulus(self, modulus):
        self.modulus = modulus
    
    def getModulus(self):
        return self.modulus

class Vehicle():
    
    DEFAULT_VEHICLE_TEC = 1
    DEFAULT_VEHICLE_TS = 1
    
    def __init__(self, tec = DEFAULT_VEHICLE_TEC, ts = DEFAULT_VEHICLE_TS):
        self.tec = tec
        self.ts = ts
    
    def getTec(self):
        return self.tec
    
    def setTec(self, new_tec):
        self.tec = new_tec
    
    def getTs(self):
        return self.ts
    
    def setTs(self, new_ts):
        self.ts = new_ts

class Cancela():
    
    DEFAULT_INIT_QUEUE_QUANTITY = 0
    DEFAULT_INIT_REMAINING_SERVICE_TIME = 0
    
    def __init__(self, queue_quantity = DEFAULT_INIT_QUEUE_QUANTITY, remaining_service_time = DEFAULT_INIT_REMAINING_SERVICE_TIME):
        self.queue = []
        self.queue_quantity = queue_quantity
        self.remaining_service_time = remaining_service_time
    
class Simulator():
    
    # Variáveis padrão do simulador
    # Offset padrão da quantidade de veículos
    DEFAULT_RANGE_OFFSET = 1
    # Tempo padrão de simulação
    DEFAULT_SIMULATION_TIME = 3600
    # Quantidade padrão de cancelas
    DEFAULT_CANCELAS_QUANTITY = 3
    # A padrão para o cálculo dos tempos de serviço
    DEFAULT_TS_A = 15
    # B padrão para o cálculo dos tempos de serviço
    DEFAULT_TS_B = 35
    # Flag para arredondar os resultados
    ROUND_NUMBER = False
    # Quantidade padrão de decimais
    DEFAULT_ROUND_DIGITS = 2

    # Inicialização do simulador
    def __init__(self, random, max_time = DEFAULT_SIMULATION_TIME, quantity_cancelas = DEFAULT_CANCELAS_QUANTITY, a = DEFAULT_TS_A, b = DEFAULT_TS_B):
        self.random_numbers = random
        self.max_time = max_time
        self.quantity_cancelas = quantity_cancelas
        self.a = a
        self.b = b
        # Colunas de cada tabela do simulador
        self.array_tec = []
        self.array_ts = []
        self.cancelas = []
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
        titles = ['Cliente', 'TEC', 'TS', 'Tempo do Relógio', 'Cancela', 'Tempo de Início', 'Tempo de Fim', 'Tempo na Fila', 'Tempo no Sistema', 'Tempo Livre']
        # Geração da tabela
        fig = go.Figure(data=[go.Table(header=dict(values=[titles[0], titles[1], titles[2], titles[3], titles[4], titles[5], titles[6], titles[7], titles[8], titles[9]]), 
                        cells=dict(values=[self.getNumberArray(), self.twoDigits(self.array_tec), self.twoDigits(self.array_ts), self.twoDigits(self.cancelas),
                        self.twoDigits(self.clock_time), self.twoDigits(self.start_time), self.twoDigits(self.end_time), self.twoDigits(self.queue_time),
                        self.twoDigits(self.system_time), self.twoDigits(self.free_time)]))])
        fig.show()

# Simulação
# Quantidade de sementes/simuladores
SEEDS_QTD = 130
# Semente base para a geração de novas sementes (mesma do Java) e multiplicador padrão dos geradores
BASE_MULTIPLIER = 25214903917
# Incremento padrão dos geradores
BASE_INCREMENT = 11
# Módulo padrão dos geradores
BASE_MODULUS = math.pow(2, 48)
# Flag para mostrar os gráficos de um dos geradores
SHOW_PLOT = False
# Quantidade de pontos no gráfico de dispensão dos geradores
PLOT_POINTS_QUANTITY = 4000
# Flag para mostrar as médias das propriedades estatísticas dos números pseudo-aleatórios gerados
SHOW_PROPERTIES_GENERATORS = False
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
    generator = Generator(BASE_MULTIPLIER, BASE_INCREMENT, BASE_MODULUS, seed=seeds[i])
    generator.generate()
    generators.append(generator)

# Plotagem do gráfico dos números gerados no i-ésimo gerador e valo
if SHOW_PLOT == True:
    generator_plot = Generator(BASE_MULTIPLIER, BASE_INCREMENT, BASE_MODULUS, seed=seeds[i], quantity=PLOT_POINTS_QUANTITY)
    generator_plot.generate()
    plot(generator_plot.getValues())

# Exibição das médias das propriedades estatísticas dos números pseudo-aleatórios gerados
if SHOW_PROPERTIES_GENERATORS == True:
    statistic_properties = [0, 0, 0, 0]
    for i in range(SEEDS_QTD):
        statistic_properties[0] += generators[i].mean()
        statistic_properties[1] += generators[i].standardDeviation()
        statistic_properties[2] += generators[i].covariance()
        statistic_properties[3] += generators[i].chiSquare()
    print("\n Propriedades estatísticas dos números pseudo-aleatórios gerados:" + "\n Média = " + str(statistic_properties[0]/SEEDS_QTD)
            + "\n Desvio padrão = " + str(statistic_properties[1]/SEEDS_QTD) + "\n Covariância = " + str(statistic_properties[2]/SEEDS_QTD)
            + "\n Qui-Quadrado = " + str(statistic_properties[3]/SEEDS_QTD))

values = generators[0].getValues()
simulator = Simulator(values, SIMULATION_TIME)
#simulator.simulate()
simulator.table()