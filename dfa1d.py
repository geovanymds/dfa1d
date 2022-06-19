import numpy as numpy
import postProcessing as pp
from scipy import stats
from utils import readInput, saveOutput

# Integração para retorno da função perfil
def integration(serie):
    average = numpy.average(serie)
    result = numpy.cumsum(serie,dtype = float)
    return result

# Função para calcular o desvio na função perfil
def deviation(array,average):
    for index, sample in enumerate(array):
        array[index] = sample - (index+1)*average
    return array

def calculateAlpha(points_array):
    points_array = numpy.log10(points_array)
    x = points_array[:,0]
    y = points_array[:,1]
    slope, intercept, _, _, _ = stats.linregress(x, y)
    # pp.plotLogLog(x, y, slope, intercept)
    if slope > 1:
        model = 'fBm'
        h = slope - 1
    else:
        model = 'fGn'
        h = slope
    print('O valor de h para a série de entrada é : ', h)
    print('O valor de alfa para a série de entrada é : ', slope)
    print('A série é : ', model)
    return [slope, h]

def dfa1d(caminhoEntrada, grau,arqSaida):
    serie = readInput(caminhoEntrada)
    # 1.	A série temporal {Xk} com k = 1, ...,N é integrada na chamada função perfil Y(k)
    yk = integration(serie)
    # 2.A série (ou perfil) Y(k) é dividida em n intervalos não sobrepostos de tamanho s, onde ns=int(N/s).
    # O processo repetido várias vezes, para diferentes escalas
    serie_length = len(serie)
    points_array = numpy.zeros(shape=(1, 2))
    max_scale = numpy.ceil(serie_length / 4).astype(numpy.int32)
    boxratio = numpy.power(2.0, 1.0 / 8.0)
    s = 4
    while s <= max_scale:
        resized_serie = yk
        # Ajusta o tamanho da série caso não seja multiplo de s
        if numpy.mod(serie_length,s) !=0:
            new_serie_length = s * int(numpy.trunc(serie_length/s))
            resized_serie = yk[0:new_serie_length]
        # Vetor que parte de s até o valor mais próximo do tamanho
        # da série ajustada, sem ultrapassa-lo e com passos iguais a s.
        # s = a 4, por exemplo ... [4,8,12,16 ... x (x<=max(serie ajustada))]
        t = numpy.arange(s,len(resized_serie),s)
        # Série dividida em intervalos [[intervalo 1],[intervalo 2] ...]
        serie_intervals = numpy.array(numpy.array_split(resized_serie,t))
        # [1, 2, 3 ... s]
        x = numpy.arange(1, s + 1)
        # 3. Cálculo da variância para cada cada parte da série
        # Mínimos quadrados
        p = numpy.polynomial.polynomial.polyfit(x,serie_intervals.T, grau)
        # Cálculo do polinômio para cada resultado dos mínimos quadrados de cada subintervalo
        yfit = numpy.polynomial.polynomial.polyval(x,p)
        # Variancia da diferença entre os intervalos e o resultado dos polinômios
        difference = serie_intervals - yfit
        intervals_variance = numpy.var(difference)
        # 4. Calculo da funcao de flutuação DFA como a média das variâncias de cada intervalo:
        fs = numpy.sqrt(numpy.mean(intervals_variance))
        points_array = numpy.vstack((points_array,[s,fs]))
        # A escala (s) cresce numa série geométrica. Adaptado de physionet
        s = numpy.ceil(s * boxratio).astype(numpy.int)
        #s = s + 1
    # Parte da primeira partição da série e copia partição por partição no vetor de saída
    points_array = points_array[1::1, :]
    saveOutput(arqSaida,points_array)
    a = calculateAlpha(points_array)
    return a

