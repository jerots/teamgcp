import numpy as np
import pandas as pd

import glob
import re
import math

from train import getTrainRecords, extractDurations


def getTable(filename, txt, user):
    df_rows = []
    cols = ["duration"]

    input = pd.read_csv(filename)
    letters, duration, HDlist, UDDlist, DDDlist = extractDurations(input)

    userrow = {}
    userrow['duration'] = duration

    for i in range(len(letters)):
        if (letters[i] == 'return'):
            break
        userrow['hperc' + str(i) + '_' + letters[i]] = HDlist[i] * 100.0 / duration
        userrow['uperc' + str(i) + '_' + letters[i]] = UDDlist[i] * 100.0 / duration
        userrow['dperc' + str(i) + '_' + letters[i]] = DDDlist[i] * 100.0 / duration
    df_rows.append(userrow)

    for i in range(len(letters)):  # SOON TO CHANGE
        if (letters[i] == 'return'):
            break
    cols.append('hperc' + str(i) + '_' + letters[i])
    cols.append('uperc' + str(i) + '_' + letters[i])
    cols.append('dperc' + str(i) + '_' + letters[i])

    newdata = pd.DataFrame(df_rows, columns=cols)

    return newdata


def separateByClass(dataset, labels):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]  # vector = row of data
        label = labels[i]
        if (label not in separated):
            separated[label] = []
        separated[label].append(vector)
    return separated


def mean(numbers):
    return sum(numbers) / float(len(numbers))


def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)


def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
    return summaries


def summarizeByClass(dataset, labels):
    separated = separateByClass(dataset, labels)
    summaries = {}
    for classValue, instances in separated.iteritems():
        summaries[classValue] = summarize(instances)
    return summaries


def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent


def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.iteritems():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]

            prob = calculateProbability(x, mean, stdev)

            if (prob != 0):
                probabilities[classValue] *= math.log(prob)

            probabilities[classValue] = round(probabilities[classValue], 2)
    return probabilities


def getProbs(filename, user, txt):

    newdata = getTable(filename, txt, user)
    dataset, labels, shortlist= getTrainRecords(txt)
    test = newdata[shortlist].drop('user', axis=1).as_matrix(columns=None)

    summaries = summarizeByClass(dataset, labels)

    for i in range(len(test)):
        testcase = test[i]
        return calculateClassProbabilities(summaries, testcase)


def predict(probabilities):
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.iteritems():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel
