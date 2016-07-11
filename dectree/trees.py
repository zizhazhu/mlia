from math import log
import treePlotter

def calcEnt(dataset):
    n = float(len(dataset))
    labels = {}
    for featvec in dataset:
        current = featvec[-1]
        if current in labels:
            labels[current] += 1
        else:
            labels[current] = 1
    entropy = 0.0
    for key in labels:
        prob = labels[key] / n
        entropy -= prob * log(prob, 2)
    return entropy

def split(dataset, axis, value):
    result = []
    for vec in dataset:
        if vec[axis] == value:
            temp = vec[:axis]
            temp.extend(vec[axis + 1:])
            result.append(temp)
    return result

# TODO: merge split into featchoose
def featchoose(dataset):
    k = len(dataset[0]) - 1
    n = float(len(dataset))
    orientropy = calcEnt(dataset)
    choosen = -1
    Max = 0.0
    for i in range(k):
        featlist = [example[i] for example in dataset]
        uniquefeat = set(featlist)
        entropy = 0.0
        for value in uniquefeat:
            subdataset =  split(dataset, i, value)
            prob = len(subdataset) / n
            entropy += prob * calcEnt(subdataset)
        gain = orientropy - entropy
        if gain > Max:
            Max = gain
            choosen = i
    return choosen

def majoritycnt(classlist):
    classcnt = {}
    for vote in classlist:
        if vote in classcnt:
            classcnt[vote] += 1
        else:
            classcnt[vote] = 1
    Max = 0
    label = classlist[0]
    for key in classcnt:
        if classcnt[key] > Max:
            Max = classcnt[key]
            label = key
    return label

def createTree(dataSet, labels):
    classList = [line[-1] for line in dataSet]
    uniqueClass = set(classList)
    if len(uniqueClass) == 1:
        return classList[0]
    if len(dataSet[0]) == 1:
        return majoritycnt(classList)
    bestFeat = featchoose(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel : {} }
    del(labels[bestFeat])
    featValues = [line[bestFeat] for line in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(split(dataSet, bestFeat, value), subLabels)
    return myTree

def createdataset():
    dataset = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataset, labels

def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    # find the index of feat from the label
    featIndex = featLabels.index(firstStr)
    for (key, value) in secondDict.items():
        if testVec[featIndex] == key:
            if type(value).__name__ == 'dict':
                classLabel = classify(value, featLabels, testVec)
            else:
                classLabel = value
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fp = open(filename, 'w')
    pickle.dump(inputTree, fp)
    fp.close()

def readTree(filename):
    import pickle
    fp = open(filename, 'r')
    return pickle.load(fp)

fp = open("lenses.txt")
lenses = [inst.strip().split('\t') for inst in fp.readlines()]
labels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = createTree(lenses, labels)
print lensesTree
treePlotter.createPlot(lensesTree)