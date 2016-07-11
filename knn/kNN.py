import numpy as np
import operator as op
import matplotlib
import matplotlib.pyplot as plt

def createDataSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

#TODO: a faster version
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis = 1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key = op.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    lines = fr.readlines()
    length = len(lines)
    returnMat = np.zeros((length, 3))
    classLabelVector = []
    fr = open(filename)
    index = 0
    for line in lines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    norm = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    norm = dataSet - np.tile(minVals, (m, 1))
    norm = norm / np.tile(maxVals - minVals, (m, 1))
    return norm, maxVals - minVals, minVals

def datingClassTest():
    horatio = 0.1
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    norm, ranges, minvals = autoNorm(datingDataMat)
    m = norm.shape[0]
    numTestVecs = int(m * horatio)
    errorcount = 0.0
    for i in range(numTestVecs):
        classifierresult = classify0(norm[i, :], norm[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print "The classifier came back with %d, the right answer is : %d." % (classifierresult, datingLabels[i])
        if classifierresult != datingLabels[i]:
            errorcount += 1
    print "The total error rate is %f" % (errorcount / float(numTestVecs))

def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    flymiles = float(raw_input("frequent flier miles earned per year?"))
    icecream = float(raw_input("liters of ice cream consumed per year?"))
    datingdata, datinglabels = file2matrix('datingTestSet.txt')
    norm, range, minval = autoNorm(datingdata)
    inputdata = np.array([flymiles, percentTats, icecream])
    result = classify0((inputdata - minval) / range, norm, datinglabels, 3)
    print "You will probably like this person: ", resultList[result - 1]

def graph():
    datingDataMat, datingLabels = file2matrix("datingTestSet.txt")
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2], 15.0 * np.array(datingLabels), 15.0 * np.array(datingLabels))
    plt.show()

group, labels = createDataSet()
#print classify0([0, 0], group, labels, 3)
datingClassTest()
classifyPerson()