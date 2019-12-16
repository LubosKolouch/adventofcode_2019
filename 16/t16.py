#! python3
#===============================================================================
#
#  DESCRIPTION: https://adventofcode.com/2019/day/16
#  --- Day 16: Flawed Frequency Transmission ---
#       AUTHOR: Lubos Kolouch
#===============================================================================

import sys

def get_sol1(input,times) :

    phases = [ 0, 1, 0, -1 ]

    for r in range(100) :
        out_str = ''
        for i in range(0,len(input) ) :
            #print('------------')
  
            #print(i)
            repeat = len(input) - i
            #print("repeat",repeat)

            value = 0
            for j in range( 0, i+1 ) :
                #print("j",j)
                pos_phases = ( int( ( i - j ) / repeat ) + 1 ) % len(phases)
                #print("pos phases",pos_phases)
                #print("meaning ",phases[pos_phases])
                value = int(value) + input[ -j - 1 ] * phases[pos_phases]
                #print("value",value)
            out_str = str(abs(value) % 10) + out_str
            #print("outstr",out_str)
        input = list(map(int,out_str))

    return ''.join(map(str, input[:8]))

def get_sol2(input,times,offset) :

    input = input * 10000
    input = input[offset:]


    for i in range(times) :
        sum = 0
        for j in range(len(input)-1,-1,-1) :
            sum += input[j]
            sum = sum % 10
            input[j] = sum

    return ''.join(map(str,input[:8]))

assert len(sys.argv) == 2
input = list(map(int, open(sys.argv[1]).read().strip()))

print("Part 1:",get_sol1(input,100))

offset = int(''.join(map(str, input[:7])))
print("Part 2:",get_sol2(input,100,offset))



