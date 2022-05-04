from typing import IO
import csv
import sys

from result.check import ajustTime
from work.DepthCalculation import Status
from work.util import most_frequent


class Compare:
    file: IO
    tp = 0
    fn = 0
    fp = 0
    tn = 0

    def initFile(self, filename: str):
        self.file = open(filename, "w+")

    def addPrediction(self, time: str, status: str):
        self.file.write(time + ';' + status + '\n')

    def writeComparaison(self, time, compareStatusList):
        if time == None:
            time = "00:00"
        else:
            time = ajustTime(time)

        statusToCompare = most_frequent(compareStatusList)
        sys.stdout.write('\r'+time)
        self.addPrediction(time, statusToCompare)
        return time
        # print(statusToCompare)

    def buildResult(self, actual, expected, pathResult):
        actualF = open(actual)
        actualReader = csv.reader(actualF, delimiter=';')
        expectedF = open(expected)
        expectedReader = csv.reader(expectedF, delimiter=';')
        resultFile = open(pathResult, "w+")
        listActualReader = list(actualReader)

        for index, expectedRow in enumerate(expectedReader, 0):
            self.__constructTableClassification(listActualReader[index], expectedRow)

        self.__insertEvaluationMetrics(resultFile)




    def __constructTableClassification(self, actualRow, expectedRow):
        if actualRow[0] == expectedRow[0]:
            if actualRow[1] == Status.OK.name:
                if expectedRow[1] == Status.OK.name:
                    self.tn = self.tn + 1
                else:
                    self.fn = self.fn + 1
            else:
                if expectedRow[1] != Status.OK.name:
                    self.tp = self.tp + 1
                else:
                    self.fp = self.fp + 1

    def __insertEvaluationMetrics(self, resultFile: IO):
        resultFile.write('TP : ' + str(self.tp) + '\n')
        resultFile.write('FP : ' + str(self.fp) + '\n')
        resultFile.write('TN : ' + str(self.tn) + '\n')
        resultFile.write('FN : ' + str(self.fn) + '\n')

        resultFile.write('\n')
        resultFile.write('---------------------\n')
        resultFile.write('\n')

        p = self.tp + self.fn
        n = self.fp + self.tn
        tpr = self.tp / p
        fpr = self.fp / n

        resultFile.write('P : ' + str(p) + '\n')
        resultFile.write('N : ' + str(n) + '\n')
        resultFile.write('TPR : ' + str(tpr) + '\n')
        resultFile.write('FPR : ' + str(fpr) + '\n')

        resultFile.write('\n')
        resultFile.write('---------------------\n')
        resultFile.write('\n')

        recall = tpr
        precision = self.tp / (self.tp + self.fp)
        accuracy = (self.tp + self.tn) / (p + n)

        resultFile.write('Recall : ' + str(recall) + '\n')
        resultFile.write('Precision : ' + str(precision) + '\n')
        resultFile.write('Accuracy : ' + str(accuracy) + '\n')






