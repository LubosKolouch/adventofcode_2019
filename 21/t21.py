#!python3

import sys
from IntCode import IntCode
from itertools import combinations
from collections import deque

def get_result(source_register,start) :
    instr_set = ["NOT ","AND ","OR "]
    target_register = ["T ","J "]


    compl_set = deque()

    for instr in instr_set :
        for source in source_register:
            for target in target_register:
                l = [instr,source,target]
                compl_set.append(l)

    for i in range(start,10):
        print(i)
        for comb in combinations(compl_set,i) :
            tr = list()
            for j in range(0,i):
                for c in comb[j]:
                    tr = tr + list(map(ord, c))
                tr[len(tr)-1] = 10
            tr = tr + list(map(ord,"WALK\n"))
            #print(tr)
            processor = IntCode("A", data, tr)
            
            result =  processor.run_intcode()
            if result[len(result)-1] != 10 :
                print(comb)
                return(result)

# ------- MAIN ----------

assert len(sys.argv) == 2

code = open(sys.argv[1]).read().strip().split(',')
data = list(map(int, code))

print("Part 1:")
print(get_result(["A ","B ","C ","D ","T ","J "],6))

print("Part 2:")
print(get_result(["A ","B ","C ","D ","E", "F", "G", "H","I","T ","J "],8))
