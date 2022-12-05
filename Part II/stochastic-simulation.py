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
        for _ in range(self.DEFAULT_OFFSET):
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

# Veículos do simulador
class Vehicle():
    
    # Variáveis padrão dos veículos
    # Tempo de chegada padrão do veículo
    DEFAULT_VEHICLE_TEC = 1
    # Tempo de serviço padrão do veículo
    DEFAULT_VEHICLE_TS = 1
    
    # Inicialização do veículo
    def __init__(self, tec = DEFAULT_VEHICLE_TEC, ts = DEFAULT_VEHICLE_TS):
        self.tec = tec
        self.ts = ts
    
    # Getters e Setters
    def getTec(self):
        return self.tec
    
    def setTec(self, new_tec):
        self.tec = new_tec
    
    def getTs(self):
        return self.ts
    
    def setTs(self, new_ts):
        self.ts = new_ts

# Cancelas do simulador
class Cancela():
    
    # Variáveis padrão das cancelas
    # Tempo de serviço atual inicial
    DEFAULT_INIT_PRESENT_SERVICE_TIME = 0
    # Tempo de serviço remanescente inicial
    DEFAULT_INIT_REMAINING_SERVICE_TIME = 0
    
    # Inicialização da cancela
    def __init__(self, present_service_time = DEFAULT_INIT_PRESENT_SERVICE_TIME, remaining_service_time = DEFAULT_INIT_REMAINING_SERVICE_TIME):
        self.queue = []
        self.count = 0
        self.present_service_time = present_service_time
        self.remaining_service_time = remaining_service_time
    
    # Quantidade de veículos da fila da cancela
    def quantity(self):
        return len(self.queue)

    # Adição de um novo veículo na fila da cancela
    def newVehicle(self, vehicle):
        self.count = self.count + 1
        if(self.quantity() == 0):
            self.present_service_time = vehicle.getTs()
        self.queue.append(vehicle)
        self.remaining_service_time = self.remaining_service_time + vehicle.getTs()

    # Cálculo da passagem de tempo do simulador para essa cancela
    def calculate(self, time):
        self.present_service_time = self.present_service_time - time
        self.remaining_service_time = self.remaining_service_time - time
        
        if self.present_service_time <= 0:
            if self.quantity() != 0:
                self.queue.pop(0)
            if self.quantity() == 0:
                self.present_service_time = self.DEFAULT_INIT_PRESENT_SERVICE_TIME
                self.remaining_service_time = self.DEFAULT_INIT_REMAINING_SERVICE_TIME
            else:
                self.present_service_time = self.queue[0].getTs() + self.present_service_time
    
    # Getter do tempo de serviço remanescente
    def getRemainingServiceTime(self):
        if self.remaining_service_time < 0:
            return 0
        else:
            return self.remaining_service_time
    
    # Getter da contagem de veículo que passaram pela cancela desde o início
    def getCount(self):
        return self.count

# Simulador
class Simulator():
    
    # Variáveis padrão do simulador
    # Offset padrão da quantidade de veículos
    DEFAULT_RANGE_OFFSET = 1
    # Tempo padrão de simulação
    DEFAULT_SIMULATION_TIME = 3600
    # Quantidade padrão de cancelas
    DEFAULT_CANCELAS_QUANTITY = 3
    # Multiplicador padrão do tempo de chegada
    DEFAULT_TEC_MULTIPLIER = 0.5
    # A padrão para o cálculo dos tempos de serviço
    DEFAULT_TS_A = 15
    # B padrão para o cálculo dos tempos de serviço
    DEFAULT_TS_B = 35
    # Flag para arredondar os resultados
    ROUND_NUMBER = False
    # Quantidade padrão de decimais
    DEFAULT_ROUND_DIGITS = 2

    # Inicialização do simulador
    def __init__(self, random_numbers, max_time = DEFAULT_SIMULATION_TIME, quantity_cancelas = DEFAULT_CANCELAS_QUANTITY, a = DEFAULT_TS_A, b = DEFAULT_TS_B):
        self.random_numbers = random_numbers
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
        for i in range(len(values)):
            values[i] = "{:.2f}".format(values[i])
        return values
    
    # Converte valores de um array de números em uma string do número com duas casas decimais
    def twoDigitsCancelas(self, values):
        for i in range(len(values)):
            values[i] = int(values[i]) + 1
        return values
    
    # Geração e visualização da tabela dos resultados do simulador
    def table(self):
        # Textos das colunas da tabela
        titles = ['Cliente', 'TEC', 'TS', 'Tempo do Relógio', 'Cancela', 'Tempo de Início', 'Tempo de Fim', 'Tempo na Fila', 'Tempo no Sistema', 'Tempo Livre']
        # Geração da tabela
        fig = go.Figure(data=[go.Table(header=dict(values=[titles[0], titles[1], titles[2], titles[3], titles[4], titles[5], titles[6], titles[7], titles[8], titles[9]]), 
                        cells=dict(values=[self.getNumberArray(), self.twoDigits(self.array_tec), self.twoDigits(self.array_ts), 
                                           self.twoDigits(self.clock_time), self.twoDigitsCancelas(self.cancelas), self.twoDigits(self.start_time),
                                           self.twoDigits(self.end_time), self.twoDigits(self.queue_time), self.twoDigits(self.system_time),
                                           self.twoDigits(self.free_time)]))])
        fig.show()
    
    # Retorno do tempo médio de chegada no sistema
    def meanTec(self):
        media_tec = 0
        for i in range(self.getRows()):
            media_tec += self.array_tec[i]
        return media_tec / self.getRows()

    # Retorno do tempo médio de espera na fila
    def meanQueue(self):
        return np.mean(self.queue_time)
    
    # Retorno do tempo médio de serviço
    def meanService(self):
        return np.mean(self.array_ts)
    
    # Retorno do tempo médio despendido no sistema
    def meanSystem(self):
        return np.mean(self.system_time)
    
    # Retorno da probabilidade de cancela livre
    def probFree(self):
        probabilidade_free = 0
        for i in range(self.getRows()):
            probabilidade_free += self.free_time[i]
        return probabilidade_free / self.max_time
    
    # Realiza a simulação
    def simulate(self):
        # Limpeza dos arrays/colunas da tabela
        self.clearArrays()
        # Cálculo dos tempos de chegada
        self.calcTec()
        
        # Criação das cancelas do simulador
        simulation_cancelas = self.newCancelas()
        
        # Cálculo iterativo de cada coluna da simulação
        # Condição de parada da simulação
        cond = True
        # Índice atual dos arrays/linha da tabela de resultados
        index = 0
        # Início da simulação
        while (cond):
            # Criação do novo veículo
            vehicle = self.vehicle(index)
            self.array_ts.append(vehicle.getTs())
            
            # Cálculo da passagem de tempo nas cancelas
            self.calcCancelas(simulation_cancelas, vehicle.getTec())
            
            # Busca pela próxima cancela que receberá o veículo
            index_cancela = self.nextCancela(simulation_cancelas)
            self.cancelas.append(index_cancela)
            
            # Tempo de chegada no relógio
            self.calcClock(index)
            
            # Tempo de início de serviço
            self.calcStart(simulation_cancelas[index_cancela], index)
            
            # Adição do veículo na fila da cancela
            simulation_cancelas[index_cancela].newVehicle(vehicle)
            
            # Tempo de final de serviço
            self.calcEnd(index)
            # Tempo na fila
            self.calcQueue(index)
            # Tempo no sistema
            self.calcSystem(index)
            # Tempo de cancela livre
            self.calcFree(simulation_cancelas[index_cancela], index_cancela, index)
            
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
        self.cancelas.clear()
        self.start_time.clear()
        self.end_time.clear()
        self.queue_time.clear()
        self.system_time.clear()
        self.free_time.clear()
    
    # Retorno de um número pseudo-aleatório da array de números pseudo-aleatórios da simulação
    def randomNumber(self):
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
            random_number = self.randomNumber()

            new_time = (-20) * math.log(float(random_number), math.e)
            new_time = new_time * self.DEFAULT_TEC_MULTIPLIER
                
            self.array_tec.append(self.roundNumber(new_time))
            count += new_time
    
    # Criação das cancelas do simulador
    def newCancelas(self):
        array_cancelas = []
        for _ in range(self.quantity_cancelas):
            new_cancela = Cancela()
            array_cancelas.append(new_cancela)
        return array_cancelas

    # Cálculo dos tempos de serviço
    def calcTs(self):
        random_number = self.randomNumber()
        
        new_time = ((self.b - self.a) * float(random_number)) + self.a
        new_time = self.roundNumber(new_time)

        return new_time
    
    # Criacação de um novo veículo
    def vehicle(self, index):
        new_vehicle = Vehicle(tec=self.array_tec[index], ts=self.calcTs())
        return new_vehicle

    # Cálculo da passagem de tempo nas cancelas
    def calcCancelas(self, simulation_cancelas, time):
        for i in range(self.quantity_cancelas):
            simulation_cancelas[i].calculate(time)
    
    # Busca pela cancela que receberá o novo veículo
    def nextCancela(self, simulation_cancelas):
        if self.quantity_cancelas == 1:
            return 0
        else:
            index = 0
            for i in range(1, len(simulation_cancelas)):
                if simulation_cancelas[i].quantity() < simulation_cancelas[index].quantity():
                    index = i
            return index
    
    # Retorno da contagem dos tempos de chegada até o determinado índice
    def countTimeToIndex(self, index):
        if (index == 0):
            return self.array_tec[index]
        
        count = 0
        for i in range(index + self.DEFAULT_RANGE_OFFSET):
            count += self.array_tec[i]
        return count
    
     # Cálculo dos tempos de chegada no relógio
    def calcClock(self, index):
        count = self.countTimeToIndex(index)
    
        self.clock_time.append(self.roundNumber(count))
    
    # Cálculo dos tempos de início de serviço
    def calcStart(self, cancela, index):
        present_clock_time = self.clock_time[index]
        remaining_time = cancela.getRemainingServiceTime()
        
        new_start_time = present_clock_time + remaining_time
        
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
    
    # Busca pela última ocorrência da cancela na tabela da simulação
    def lastIndexCancela(self, index_cancela):
        last_index = 0
        for i in range(len(self.cancelas) - 1):
            if self.cancelas[i] == index_cancela:
                last_index = i
        return last_index
    
    # Cálculo dos tempos de cancela livre
    def calcFree(self, cancela, index_cancela, index):
        if (cancela.getCount() == 1):
            self.free_time.append(self.roundNumber(self.start_time[index]))
        else:
            last_index_cancela = self.lastIndexCancela(index_cancela)
            new_time = self.start_time[index] - self.end_time[last_index_cancela]

            if new_time < 0:
                new_time = 0

            self.free_time.append(self.roundNumber(new_time))
    
    # Remove resultados da simulação caso tenham passado do tempo de simulação
    def trimmer(self, index):
        rows = self.getRows() - (index + self.DEFAULT_RANGE_OFFSET)
        for _ in range(rows):
            self.array_tec.pop()
            
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

# Criação dos n simuladores e realização de cada simulação
simulators = []
for i in range(SEEDS_QTD):
    values = generators[i].getValues()
    
    simulator = Simulator(values, SIMULATION_TIME)
    simulator.simulate()
    simulators.append(simulator)

# Criação dos arrays das médias dos tempos na fila, tempos no sistema e tempos de serviço de cada simulação
medias_fila = []
medias_sistema = []
medias_servico = []
medias_tec = []
for i in range(SEEDS_QTD):
    medias_fila.append(simulators[i].meanQueue())
    medias_sistema.append(simulators[i].meanSystem())
    medias_servico.append(simulators[i].meanService())
    medias_tec.append(simulators[i].meanTec())

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