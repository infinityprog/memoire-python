from typing import IO
import csv

from work.DepthCalculation import Status


class Compare:
    file: IO
    tp = 0
    fn = 0
    fp = 0
    tn = 0

    def initFile(self, filename: str):
        self.file = open(filename, "w")

    def addPrediction(self, time: str, status: Status):
        self.file.write(time + ';' + status.name)

    def buildResult(self, actual, expected):
        actualF = open(actual)
        actualReader = csv.reader(actualF, delimiter=';')
        expectedF = open(expected)
        expectedReader = csv.reader(expectedF, delimiter=';')
        resultFile = open('../result/result.txt', "w")

        for index, expectedRow in expectedReader:
            actualRow = actualReader[index]

            self.__constructTableClassification(actualRow, expectedRow)
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
        resultFile.write('TP : ' + str(self.tp))
        resultFile.write('FP : ' + str(self.fp))
        resultFile.write('TN : ' + str(self.tn))
        resultFile.write('FN : ' + str(self.fn))

        resultFile.write('')
        resultFile.write('---------------------')
        resultFile.write('')

        p = self.tp + self.fn
        n = self.fp + self.tn
        tpr = self.tp / p
        fpr = self.fp / n

        resultFile.write('P : ' + str(p))
        resultFile.write('N : ' + str(n))
        resultFile.write('TPR : ' + str(tpr))
        resultFile.write('FPR : ' + str(fpr))

        resultFile.write('')
        resultFile.write('---------------------')
        resultFile.write('')

        recall = tpr
        precision = self.tp / (self.tp + self.fp)
        accuracy = (self.tp + self.tn) / (p + n)

        resultFile.write('Recall : ' + str(recall))
        resultFile.write('Precision : ' + str(precision))
        resultFile.write('Accuracy : ' + str(accuracy))






