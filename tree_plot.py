import matplotlib.pyplot as plt

decisionNode=dict(boxstyle='sawtooth',fc='0.8')
leafNode=dict(boxstyle='round4',fc='0.8')
arrow_args=dict(arrowstyle='<-')


def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,
                            xycoords='axes fraction',
                            xytext=centerPt,textcoords='axes fraction',
                            va='center',ha='center',bbox=nodeType,arrowprops=arrow_args)

def createPlot():
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    createPlot.ax1=plt.subplot(111,frameon=False)
    plotNode('a decision node',(0.5,0.1),(0.1,0.5),decisionNode)
    plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()

def getNumLeaves(Tree):
    leafCounts=0
    firstStr=list(Tree.keys())[0]
    tempTree=Tree[firstStr]
    for key in tempTree.keys():
        subTree=tempTree[key]
        if type(subTree).__name__=='dict':
            leafCounts+=getNumLeaves(subTree)
        else:
            leafCounts+=1
    return leafCounts

def getTreeDepth(Tree):
    treeDepth=0
    firstStr=list(Tree.keys())[0]
    tempTree=Tree[firstStr]
    for key in tempTree.keys():
        subTree=tempTree[key]
        if type(subTree).__name__=='dict':
            thisDepth=1+getTreeDepth(subTree)
        else:
            thisDepth=1
        if thisDepth>treeDepth:
            treeDepth=thisDepth
    return treeDepth

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
    return listOfTrees[i]