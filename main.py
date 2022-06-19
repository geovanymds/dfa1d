import dfa1d as dfa1d
import numpy as np


if __name__ == '__main__':
    alfas = []
    hs = []
    for i in range(30):
        alfa, h = dfa1d.dfa1d(f'./Data/input/fGn/09/sample_09_{i+1}.txt',1,f'./Data/output/fGn/09/sample_09_output_{i+1}')
        alfas.append(alfa)
        hs.append(h)
    print('MÉDIA PARA ALFA : ',np.mean(alfas))
    print('MÉDIA PARA H : ', np.mean(hs))
    print('DESVIO PADRÃO PARA ALFA : ',np.std(alfas))
    print('DESVIO PADRÃO PARA H : ',np.std(hs))
