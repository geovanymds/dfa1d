import numpy as numpy
import codecs

def readInput(inputPath):
    with codecs.open(inputPath, encoding='utf-8-sig') as f:
        x = numpy.loadtxt(f, delimiter='/n')
    return x

def saveOutput(outputPath,vetoutput):
    with open(outputPath, 'ab') as f:
        numpy.savetxt(f, numpy.log10(vetoutput), fmt='%0.4f', delimiter='\t')