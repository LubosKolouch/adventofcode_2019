#!python3

import sys
from IntCode import IntCode
from itertools import combinations
from collections import deque


assert len(sys.argv) == 2

code = open(sys.argv[1]).read().strip().split(',')
data = list(map(int, code))

processors = deque()

for i in range(50):
    processor = IntCode(i,data,i)
    processors.append( processor )

i = 0
addr = 0

while addr != 255:
    print("Running processor :",i)
    (addr,x,y) = processors[i].run_intcode()
    if addr == 255:
        print("Found 255")
        print(x,y)
        break

    if addr != -1:
        print("Returned addr",addr," x ",x," y")
        processors[addr].io.append(x)
        processors[addr].io.append(y)
        i = addr
    else :
        i += 1
        i %= 50

print("Part 1:",y)
