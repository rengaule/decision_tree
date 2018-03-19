from math import log
import operator
from decision_tree.treePloter import createPlot

def createDataSet():
    dataSet = [['长', '粗', '男'],
               ['短', '粗', '男'],
               ['短', '粗', '男'],
               ['长', '细', '女'],
               ['短', '细', '女'],
               ['短', '粗', '女'],
               ['长', '粗', '女'],
               ['长', '粗', '女']]
    labels = ['头发', '声音']  # 两个特征
    return dataSet, labels

def majorityClass(classList):
    list={}
    for one in classList:
        if one not in list.keys():
            list[one]=1
        else:
            list[one]+=1
    sortedClass=sorted(list.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClass[0][0]

def calcShannonEnt(dataSet):
    numberData=len(dataSet)
    classCount={}
    shannonEnt=0
    for one in dataSet:
        currentLabel=one[-1]
        if currentLabel not in classCount.keys():
            classCount[currentLabel]=1
        else:
            classCount[currentLabel]+=1
    for key in classCount:
        prob=float(classCount[key])/numberData
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for examle in dataSet:
        if(examle[axis]==value):
            reducedDataSet=examle[:axis]
            reducedDataSet.extend(examle[axis+1:])
            retDataSet.append(reducedDataSet)
    return retDataSet

def chooseBestFeat(dataSet):
    numberFeats=len(dataSet[0])-1
    baseEntropy=calcShannonEnt(dataSet)
    baseInfoGain=0
    bestFeat=-1
    for i in range(numberFeats):
        newEntropy = 0
        featList=[example[i] for example in dataSet]
        uniqueVals=set(featList)
        for one in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,one)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy-=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if(infoGain>baseInfoGain):
            bestFeat=i
            baseInfoGain=infoGain
    return bestFeat

def generateTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    if(classList.count(classList[0])==len(classList)):
        return classList[0]
    if(len(dataSet[0])==1):
        return majorityClass(classList)
    bestFeat=chooseBestFeat(dataSet)
    bestLabel=labels[bestFeat]
    Tree={bestLabel:{}}
    del(labels[bestFeat])
    featVals=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featVals)
    for value in uniqueVals:
        subLabels=labels[:]
        Tree[bestLabel][value]=generateTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return Tree

if __name__ == '__main__':
    dataSet,labels=createDataSet()
    myTree = generateTree(dataSet, labels)
    print(myTree)
    createPlot(myTree)