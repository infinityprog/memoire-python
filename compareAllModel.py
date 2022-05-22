import os
import timeit
import datetime

from work.env import repCompare

for model in ['yolov5n', 'yolov5s', 'yolov5m', 'yolov5l']:

    start = timeit.default_timer()
    os.system('python memoire.py '+ model + ' True')
    stop = timeit.default_timer()

    f = open(repCompare(model) + 'time.txt', 'w+')
    f.write('Time: ' + str(datetime.timedelta(seconds=(stop - start))))
    f.close()

    os.system('python buildResult.py ' + repCompare(model) + 'actual.csv result/expected-large.csv ' + repCompare(model) + 'result.txt')
