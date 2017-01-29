import random

def getPercentStr(value):
    return '%.2f' % round(value*100, 1) + "%"

def getMoneyStr(value):
    return '%.2f PLN' % value

def simulate(winProbability):
    return (random.random() <= winProbability)
