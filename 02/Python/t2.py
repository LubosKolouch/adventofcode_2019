# python3

from pprint import pprint
import numpy as np
import sys

file = "../input"

data = np.loadtxt(file, delimiter=',')

data[1] = 12
data[2] = 2

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

print(int(data[0]));




