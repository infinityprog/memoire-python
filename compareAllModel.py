import os
import timeit
import datetime

from work.env import repCompare

for model in ['depthmap']:

    start = timeit.default_timer()
    os.system('python memoirewithoutyolo.py True')
    stop = timeit.default_timer()

    f = open(repCompare(model) + 'time.txt', 'w+')
    f.write('Time: ' + str(datetime.timedelta(seconds=(stop - start))))
    f.close()

    os.system('python buildResult.py ' + repCompare(model) + 'actual.csv result/expected-large.csv ' + repCompare(model) + 'result.txt')
