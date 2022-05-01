import sys
import csv

def ajustTime(time):
    if int(time[3:5]) + 1 >= 60:
        time = '0' + str(int(time[1]) + 1) + time[2:5]
    val = (int(time[3:5]) + 1) % 60
    if val < 10:
        return time[0:3] + '0' + str(val)
    else:
        return time[0:3] + str(val)





def main():
    if len(sys.argv) != 2:
        print('Only one arg : Path')
        quit()

    path = sys.argv[1]
    f = open(path)
    myReader = csv.reader(f, delimiter=';')
    oldTime = None
    for row in myReader:
        time = row[0]
        value = row[1]

        if oldTime is None:
            if time != '00:00':
                print('Actual time: ' + time + ', expected time : 00:00')
                quit()
            oldTime = '00:00'
        else:
            oldTime = ajustTime(oldTime)
            if oldTime != time:
                print('Actual time: ' + time + ', expected time : ' + oldTime)
                quit()
    print('File OK')


if __name__ == "__main__":
    main()
