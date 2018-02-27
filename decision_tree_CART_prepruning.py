import pandas as pd
import operator
from math import log

def classCount(data):
    labelCount={}
    classList=data['label']
    for one in classList:
        if one not in labelCount.keys():
            labelCount[one]=0
        labelCount[one]+=1
    return labelCount

def calcShannonEnt(data):
    labelCount=classCount(data)
    shannonEnt=0.0
    for one in labelCount:
        prob=float(labelCount[one])/len(data)
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def createTree(data):
    baseEntropy=calcShannonEnt(data)
    

if __name__ == '__main__':
    # load dataset
    path='/home/tyler/machine_learning/data/'
    data=pd.read_csv(path+'iris.csv')
    createTree(data)