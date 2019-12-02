# python3

from pprint import pprint
import numpy as np
import sys

file = "../input"



for i in range(0,99):
    for j in range(0,99):
        data = np.loadtxt(file, delimiter=',')

        data[1] = i
        data[2] = j

        pos=0;

        while (data[pos] != 99):
            arg1 = int(data[int(data[pos+1])])
            arg2 = int(data[int(data[pos+2])])

            if (data[pos] == 1):
                data[int(data[pos+3])] = arg1+arg2
            elif (data[pos] == 2): 
                data[int(data[pos+3])] = arg1*arg2       
            else:
                sys.exit("Unknown argument found")
            pos += 4;

        if (data[0] == 19690720):
            print(int(100*data[1]+data[2]))
            sys.exit()



