from math import log
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

def calcShannonEnt(dataSet):
    labelCount={}
    numberEntries=len(dataSet)
    for one in dataSet:
        currentLabel=one[-1]
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel]=0
        labelCount[currentLabel]+=1
    shannonEnt=0.0
    for i in labelCount:
        prob=float(labelCount[i])/numberEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def majorityClass(classList):
    classCount={}
    for one in classList:
        if one not in classCount.keys():
            classCount[one]=0
        classCount[one]+=1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def splitDataSet(dataSet,feat,value):
    subDataSet=[]
    for featVec in dataSet:
        if featVec[feat]==value:
            reducedData=featVec[:feat]
            reducedData.extend(featVec[feat+1:])
            subDataSet.append(reducedData)
    return subDataSet

def chooseBestFeat(dataSet,labels):
    bestFeat=-1
    baseEnt=calcShannonEnt(dataSet)
    baseInfoGain=0.0
    numberFeat=len(dataSet[0])-1
    for i in range(numberFeat):
        classVals=[example[i] for example in dataSet]
        uniqueVals=set(classVals)
        newEntropy=0.0
        newInfoGain=0.0
        splitInfo=0.0
        print(labels[i] + ':')
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)
            print(str(value)+':')
            print(subDataSet)
            prob=float(len(subDataSet))/len(dataSet)
            newEntropy-=prob*calcShannonEnt(subDataSet)
            splitInfo -=prob*log(prob,2)
        newInfoGain=(baseEnt-newEntropy)/splitInfo
        print('baseEnt='+str(baseEnt))
        print('Iv'+labels[i]+'='+str(splitInfo)+' (V='+str(len(uniqueVals))+')')
        print('newEntropy '+labels[i]+'='+str(newEntropy))
        print('Gain '+labels[i] +'='+str(newInfoGain))
        print('\t')
        if newInfoGain>baseInfoGain:
            baseInfoGain=newInfoGain
            bestFeat=i
    return bestFeat


def createTree(dataSet,labels):
    shannonEnt=calcShannonEnt(dataSet)
    classList=[example[-1] for example in dataSet]
    if(classList.count(classList[0])==len(dataSet)):
        return classList[0]
    if(len(dataSet[0])==1):
        return majorityClass(classList)
    bestFeat=chooseBestFeat(dataSet,labels)
    bestFeatLabel=labels[bestFeat]
    print('bestFeat:'+labels[bestFeat])
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featVals=[example[bestFeat] for example in dataSet]
    uniquFeatVals=set(featVals)
    for value in uniquFeatVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

if __name__ == '__main__':
    dataSet,labels=createDataSet()
    print(createTree(dataSet,labels))