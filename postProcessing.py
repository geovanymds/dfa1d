import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np


def plotTimeSeries(timeSerie, title):
    fig = plt.figure()
    plt.plot(timeSerie)
    plt.title(title)
    plt.show(block=False)
    return


# Calcula o valor do alfa, como a inclinação do ajuste no gráfico log-log entre a escala e a função de flutuação
def plotLogLog(vetS, vetFs, slope, intercept):
    predict_y = intercept + slope * vetS
    x0 = np.mean(vetS)
    y0 = slope * x0 + intercept
    if slope > 1:
        model = 'fBm'
        h = slope - 1
    else:
        model = 'fGn'
        h = slope
    fig = plt.figure()
    plt.plot(vetS, vetFs, 'ro')
    plt.plot(vetS, predict_y, 'k-')
    if intercept > 0:
        t = 'y = ' + str(round(slope, 2)) + 'x + ' + str(round(intercept, 2))
    else:
        t = 'y = ' + str(round(slope, 2)) + 'x ' + str(round(intercept, 2))
    plt.annotate(t,
                 xy=(x0, y0),
                 xytext=(x0, y0),
                 # xytext=(x0 - .4 * x0, y0 + .4 * y0),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.5')
                 )
    plt.ylabel('Log(F(s))')
    plt.xlabel('Log(s)')
    plt.xlim(np.min(vetS), np.max(vetS) + 1)
    plt.ylim(np.min(vetFs), np.max(vetFs) + 1)
    plt.title('DFA-Unidimensional  ' + model + ': H = ' + str(round(h, 1)))
    red_line = mlines.Line2D([], [], color='red', marker='o', label='Dados')
    bla_line = mlines.Line2D([], [], color='black', label='Fit')
    plt.legend(handles=[red_line, bla_line], loc='lower right')
    plt.show(block=True)
    return


def plotHq(vet):
    fig = plt.figure()
    plt.plot(vet[:, 0], vet[:, 1], 'ro')
    plt.xlim((-7, 7))
    plt.ylim((0, 3))
    plt.xlabel('q')
    plt.ylabel('h(q)')
    plt.show(block=False)
