#! python3

import sys
from pprint import pprint
import numpy as np
from itertools import permutations

# opcodes
#
# 1 - adding, noun, verb, result (3+1)
# 2 - multiply, noun, verb, result (3+1)
# 3 - input, result (1+1)
# 4 - output, result (1+1)
# 5 - jump, zero/nonzero, where (or ignored if zero)
# 6 - jump, zero/nonzero, where if zero (or ignored)
# 7 - less than, if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
# 8 - equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.


amplifier = {}
program_param = {}

def run_intcode(cur_amp) :

    # positions : 0 = position mode, 1 = immediate mode
    # ABCDE
    # 1002
    #
    #DE - two-digit opcode,      02 == opcode 2
    # C - mode of 1st parameter,  0 == position mode
    # B - mode of 2nd parameter,  1 == immediate mode
    # A - mode of 3rd parameter,  0 == position mode, omitted due to being a leading zero

    params = { 1 : 3, 2 : 3, 3 : 1,    4 : 1,    5 : 2,    6 : 2,    7 : 3,    8 : 3, 99:0 }
    writing_instr = {    1 : 1,    2 : 1,    7 : 1,    8 : 1 }

    data = np.fromstring(amplifier[(cur_amp,'program')], dtype=int,sep=',')
    pos = amplifier[(cur_amp,'position')]

    while 1:
        what = []

        instr = str(data[pos])

        if len(instr) == 1: instr = '0' + instr

        what.append(int(instr[-2:]))
        
        if what[0] not in params:
            sys.exit()

        instr = instr[:-2]

        for p in range(1,params[what[0]]+1):
            if instr :
                mode = int(instr[-1])
                instr = instr[:-1]
            else:
                mode = 0


            if (mode == 1) or (data[pos] == 3):
                what.append(data[pos+p])
            elif (p == params[what[0]]) and (what[0] in writing_instr):
                what.append(data[pos+p])
            else :
                what.append( data[ data[ pos + p ] ])


        if what[0] == 1 :
            data[ what[3] ] = what[1] + what[2]

        elif what[0] == 2 :
            data[ what[3] ] = what[1] * what[2]

        elif what[0] == 3 :
            if amplifier[(cur_amp,'phase_set')] :
                data[ what[1] ] = amplifier[(cur_amp,'input')]
            else:
                amplifier[(cur_amp,'phase_set')] = 1
                data[ what[1] ] = amplifier[(cur_amp,'phase')]
        
        elif what[0] == 4 :
            amplifier[(cur_amp,'program')] = ','.join(str(x) for x in data)

            shift = params[ what[0] ] + 1;
            pos = pos + shift;
            amplifier[(cur_amp,'position')] = pos

            return what[1];
        
        elif what[0] == 5 :
            if what[1] > 0:
                pos = what[2];
                continue
        
        elif what[0] == 6 :
            if what[1] == 0 :
                pos = what[2]
                continue

        elif what[0] == 7 :
            if what[1] < what[2] :
                data[ what[3] ] = 1
            else :
                data[ what[3] ] = 0
        
        elif what[0] == 8 :
            if what[1] == what[2] :
                data[ what[3] ] = 1
            else :
                data[ what[3] ] = 0
        
        elif what[0] == 99 :
            program_param['program_end'] = 1;
            return "END";
        
        else :
            os.exit("Unknown argument found")

        shift = params[ what[0] ] + 1;
        pos = pos + shift;



# ------- MAIN ----------

file = open("input","r")

for line in file:
    program = line.strip()

program_param['mode'] = 'feedback';
program_param['program_end'] = 0;

phase_list = ''
if program_param['mode'] == 'normal':
    phase_list='01234'

if program_param['mode'] == 'feedback':
    phase_list = '56789'


max = 0

for combo in permutations(phase_list,5):
    program_param['program_end'] = 0;

    amp = ['A','B','C','D','E']

    # initialize the amplifiers

    input = 0;

    for phase in combo :
        cur_amp = amp.pop(0)
        amplifier[(cur_amp,'program')]  = program;
        amplifier[(cur_amp,'phase')]  = phase;
        amplifier[(cur_amp,'position')] = 0;
        amplifier[(cur_amp,'input')]  = 0;
        amplifier[(cur_amp,'output')]   = 0;
        amplifier[(cur_amp,'phase_set')]   = 0;

    end = 0;

    while (end == 0) :
        amp = ['A','B','C','D','E']
        
        # loop through the amplifiers
        for amps in range(len(amp)) :
            cur_amp = amp[amps]
            next_amp = amp[(amps +1) % len(amp)]

            amplifier[(next_amp,'input')] = run_intcode( cur_amp )

            if (cur_amp == 'E') and (amplifier[next_amp,'input'] > max) :
                max = amplifier[(next_amp,'input')]

            if (program_param['program_end'] ==1 ) :
                end = 1;
                break

            if program_param['mode'] == 'normal' : end =1

print(max)
