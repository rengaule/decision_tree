from math import log,sqrt
import operator

def createDataSet():
    dataSet = [[1,'长', '粗', '男'],
               [2,'短', '粗', '男'],
               [3,'短', '粗', '男'],
               [4,'长', '细', '女'],
               [5,'短', '细', '女'],
               [6,'短', '粗', '女'],
               [7,'长', '粗', '女'],
               [8,'长', '粗', '女']]
    labels = ['序号','头发', '声音']  # 两个特征
    return dataSet, labels

def classCount(dataSet):
    labelCount={}
    for one in dataSet:
        if one[-1] not in labelCount.keys():
            labelCount[one[-1]]=0
        labelCount[one[-1]]+=1
    return labelCount

def calcShannonEntropy(dataSet):
    labelCount=classCount(dataSet)
    numEntries=len(dataSet)
    Entropy=0.0
    for i in labelCount:
        prob=float(labelCount[i])/numEntries
        Entropy-=prob*log(prob,2)
    return Entropy

def majorityClass(dataSet):
    labelCount=classCount(dataSet)
    sortedLabelCount=sorted(labelCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedLabelCount[0][0]

def splitDataSet(dataSet,i,value):
    subDataSet=[]
    for one in dataSet:
        if one[i]==value:
            reduceData=one[:i]
            reduceData.extend(one[i+1:])
            subDataSet.append(reduceData)
    return subDataSet

def splitContinuousDataSet(dataSet,i,value,direction):
    subDataSet=[]
    for one in dataSet:
        if direction==0:
            if one[i]>value:
                reduceData=one[:i]
                reduceData.extend(one[i+1:])
                subDataSet.append(reduceData)
        if direction==1:
            if one[i]<=value:
                reduceData=one[:i]
                reduceData.extend(one[i+1:])
                subDataSet.append(reduceData)
    return subDataSet

def chooseBestFeat(dataSet):
    baseEntropy=calcShannonEntropy(dataSet)
    bestFeat=-1
    baseInfoGain=0.0
    numFeats=len(dataSet[0])-1
    for i in range(numFeats):
        vals=[example[i] for example in dataSet]
        uniqueVals=set(vals)
        newEntropy=0.0
        newInfoGain=0.0
        splitInfo=0.0
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=float(len(subDataSet))/len(dataSet)
            splitInfo-=prob*log(prob,2)
            newEntropy-=prob*calcShannonEntropy(subDataSet)
        newInfoGain=(baseEntropy-newEntropy)/splitInfo
        if newInfoGain>baseInfoGain:
            bestFeat=i
            baseInfoGain=newInfoGain
    return bestFeat



def createTree(dataSet,labels):
    Entropy=calcShannonEntropy(dataSet)
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0])==len(dataSet):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityClass(dataSet)
    bestFeat=chooseBestFeat(dataSet)
    bestFeatLabel=labels[bestFeat]
    print('bestFeat:'+bestFeatLabel)
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featVals=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featVals)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree



if __name__ == '__main__':
    dataSet,labels=createDataSet()
    print(createTree(dataSet,labels))
