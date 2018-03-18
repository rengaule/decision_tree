import matplotlib.pyplot as plt

decisionNode=dict(boxstyle='sawtooth',fc='0.8')
leafNode=dict(boxstyle='round4',fc='0.8')
arrow_args=dict(arrowstyle='<-')


def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,
                            xycoords='axes fraction',
                            xytext=centerPt,textcoords='axes fraction',
                            va='center',ha='center',bbox=nodeType,arrowprops=arrow_args)

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

def plotMidTxt(centerPt,parentPt,txtString):
    xMid=centerPt[0]+(parentPt[0]-centerPt[0])/2.0
    yMid=centerPt[1]+(parentPt[1]-centerPt[1])/2.0
    createPlot.ax1.text(xMid,yMid,txtString)


def plotTree(Tree,parentPt,nodeTxt):
    numLeaves=getNumLeaves(Tree)
    treeDepth=getTreeDepth(Tree)
    firstStr=list(Tree.keys())[0]
    centerPt=(plotTree.xoff+(1.0+float(numLeaves))/2.0/plotTree.totalW,plotTree.yoff)
    plotMidTxt(centerPt,parentPt,nodeTxt)
    plotNode(str(firstStr),centerPt,parentPt,decisionNode)
    tempTree=Tree[firstStr]
    plotTree.yoff=plotTree.yoff-1.0/plotTree.totalD
    for key in tempTree.keys():
        if type(tempTree[key]).__name__=='dict':
            plotTree(tempTree[key],centerPt,str(key))
        else:
            plotTree.xoff=plotTree.xoff+1.0/plotTree.totalW
            plotNode(tempTree[key],(plotTree.xoff,plotTree.yoff),centerPt,leafNode)
            plotMidTxt((plotTree.xoff,plotTree.yoff),centerPt,str(key))
    plotTree.yoff=plotTree.yoff+1.0/plotTree.totalD

def createPlot(inTree):
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    axprops=dict(xticks=[],yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeaves(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW;
    plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()
