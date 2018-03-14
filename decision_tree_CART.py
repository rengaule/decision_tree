import pandas as pd
import operator

def loadDataSet(name='iris.csv'):
    path='/home/tyler/machine_learning/data/'
    dataSet=pd.read_csv(path+name)
    return dataSet

def classCount(dataSet):
    counts={}
    labels=dataSet.iloc[:,-1]
    for one in labels:
        if one not in counts.keys():
            counts[one]=0
        counts[one]+=1
    return counts

def calcGini(dataSet):
    gini=1.00
    counts=classCount(dataSet)
    for one in counts.keys():
        prob=float(counts[one])/len(dataSet)
        gini-=(prob*prob)
    return gini

def majorityClass(dataSet):
    counts=classCount(dataSet)
    sortedCounts=sorted(counts.items(),key=operator.itemgetter(1),reverse=True)
    return sortedCounts[0][0]

def splitContinuousDataSet(dataSet,i,value,direction):
    if direction==0:
        subDataSet=dataSet[dataSet.iloc[:,i]>value]
    if direction==1:
        subDataSet=dataSet[dataSet.iloc[:,i]<=value]
    reduceDataSet=subDataSet.drop(subDataSet.columns[i],axis=1)
    return reduceDataSet

def splitDataSet(dataSet,i,value):
    subDataSet=dataSet[dataSet.iloc[:,i]==value]
    reduceDataSet=subDataSet.drop(subDataSet.columns[i],axis=1)
    return reduceDataSet


def chooseBestFeat(dataSet):
    labels=dataSet.iloc[:,-1]
    feats=dataSet.columns
    splitDic={}
    splitPoint=[]
    bestGiniIndex=10000.0
    bestFeat=0
    for i in range(len(dataSet.iloc[0,:])-1):
        if type(dataSet.iloc[0,i]).__name__=='float64':
            # set a list of value as split point to split
            valueList=set(dataSet.iloc[:,i])
            bestSplitGini=1000.0
            for value in valueList:
                newGiniIndex=0.0
                greaterDataSet=splitContinuousDataSet(dataSet,i,value,0)
                prob0=float(len(greaterDataSet))/len(dataSet)
                newGiniIndex+=prob0*calcGini(greaterDataSet)
                smallerDataSet=splitContinuousDataSet(dataSet,i,value,1)
                prob1=float(len(smallerDataSet))/len(dataSet)
                newGiniIndex+=prob1*calcGini(smallerDataSet)
                if newGiniIndex<bestSplitGini:
                    bestSplitGini=newGiniIndex
                    bestSplitValue=value
            splitDic[dataSet.columns[i]]=value
            GiniIndex=bestSplitGini
            print('tempBestFeat:' + str(dataSet.columns[i]) + ' ,GiniIndex:' + str(newGiniIndex))
        else:
            valueList=set(dataSet.iloc[:,i])
            newGiniIndex=0.0
            for value in valueList:
                subDataSet=splitDataSet(dataSet,i,value)
                prob=float(len(subDataSet))/len(dataSet)
                newGiniIndex+=prob*calcGini(subDataSet)
            GiniIndex=newGiniIndex
        if GiniIndex<bestGiniIndex:
            bestGiniIndex=GiniIndex
            bestFeat=i
    if type(dataSet.iloc[0,bestFeat]).__name__=='float64':
        bestFeatValue=splitDic[dataSet.columns[bestFeat]]
    if type(dataSet.iloc[0,bestFeat]).__name__=='str':
        bestFeatValue=dataSet.columns[bestFeat]
    return bestFeat,bestFeatValue





def createTree(dataSet):
    gini=calcGini(dataSet)
    if len(dataSet.columns)==2:
        return majorityClass(dataSet)
    if len(set(dataSet.iloc[:,-1]))==1:
        return dataSet.iloc[0,-1]
    bestFeat,bestFeatValue=chooseBestFeat(dataSet)
    bestFeatLabel=dataSet.columns[bestFeat]
    print('bestFeat:'+str(bestFeatLabel))
    print('bestFeatValue:'+str(bestFeatValue))
    myTree={bestFeatLabel:{}}
    # reduceDataSet=dataSet.drop(bestFeatLabel,axis=1)
    if type(dataSet.iloc[0,bestFeat]).__name__=='float64':
        greaterDataSet=splitContinuousDataSet(dataSet,bestFeat,bestFeatValue,0)
        myTree[bestFeatLabel]['>'+str(bestFeatValue)]=createTree(greaterDataSet)
        smallerDataSet=splitContinuousDataSet(dataSet,bestFeat,bestFeatValue,1)
        myTree[bestFeatLabel]['<='+str(bestFeatValue)]=createTree(smallerDataSet)
    if type(dataSet.iloc[0,bestFeat]).__name__=='str':
        bestFeatValues=dataSet.iloc[:,bestFeat]
        uniqBestFeatVals=set(bestFeatValues)
        for value in uniqBestFeatVals:
            myTree[bestFeatLabel][bestFeatValue]=createTree(splitDataSet(dataSet,bestFeat,value))

    return myTree

if __name__ == '__main__':
    dataSet=loadDataSet()
    dataSet._convert(float)
    labels=dataSet.columns
    print(createTree(dataSet))