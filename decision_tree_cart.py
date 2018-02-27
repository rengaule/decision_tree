from math import log
import operator
import pandas as pd

def loadDataSet():
    path=r'/home/tyler/machine_learning/data/'
    data=pd.read_csv(path+'iris.csv')
    return data

def countNumber(dataSet):
    numberEntries = len(dataSet)
    labelCount = {}
    for i in range(numberEntries):
        if dataSet.iloc[i, -1] not in labelCount.keys():
            labelCount[dataSet.iloc[i, -1]] = 0
        labelCount[dataSet.iloc[i, -1]] += 1
    return labelCount

def calcShannonEnt(dataSet):
    numberEntries=len(dataSet)
    labelCount=countNumber(dataSet)
    shannonEntropy=0.0
    for key in labelCount:
        prob=float(labelCount[key])/numberEntries
        shannonEntropy-=prob*log(prob,2)
    print(shannonEntropy)

def majorityCount(dataSet):
    labelCount=countNumber(dataSet)
    sortedCount=sorted(labelCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedCount[0][0]

def splitDataSet(dataSet,i,value):
    reduceDataSet=dataSet[dataSet.iloc[:,i]==value]
    reduceDataSet.drop(labels=dataSet.columns[i],inplace=True,axis=1)
    print(reduceDataSet)
    return reduceDataSet

def calcGini(dataSet,i,value):
    for j in range(len(dataSet)):
        dataSet.iloc[i,i]

def chooseBestFeat(dataSet):
    featList=dataSet.columns[:-1]
    for i in range(len(featList)):
        valueList=dataSet.iloc[:,i]
        uniqueValues=set(valueList)
        for value in uniqueValues:
            subDataSet=splitDataSet(dataSet,i,value)
            count=countNumber(subDataSet)
            for key in count.keys():



def createTree(dataSet):
    if(len(set(dataSet.iloc[:,-1]))==1):
        return dataSet.iloc[0,-1]
    if(len(dataSet.columns)==2):
        return majorityCount(dataSet)
    baseEnt=calcShannonEnt(dataSet)
    bestFeat=chooseBestFeat(dataSet)


if __name__ == '__main__':
    dataSet= loadDataSet()
    print(createTree(dataSet))