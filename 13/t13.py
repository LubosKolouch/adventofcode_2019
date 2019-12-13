#! python3

import sys
from pprint import pprint
import numpy as np
from itertools import permutations
import csv
from collections import deque

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


processor = {}
program_param = {}
grid = {}
painted = {}
block_count = 0
paddle_x = 0
ball_x =0
score =0

def get_input(cur_proc) :
 #   qu = processor[cur_proc]['io']
  #  g_value = grid.get((processor[cur_proc]['x'],processor[cur_proc]['y']),0)
  #  processor[cur_proc]['io'].append(g_value)
    if (paddle_x > ball_x) :
        processor[cur_proc]['io'].append(-1)
    elif (paddle_x < ball_x) :
        processor[cur_proc]['io'].append(1)
    else: 
        processor[cur_proc]['io'].append(0)

def process_output(cur_proc) :
    global ball_x
    global paddle_x
    qu = processor[cur_proc]['io']
    queue_length = len(qu)
    if (len(processor[cur_proc]['io']) == 3) :
        x = processor[cur_proc]['io'].popleft()
        y = processor[cur_proc]['io'].popleft()
        what= processor[cur_proc]['io'].popleft()

        if (x,y) == (-1,0):
            score = what
            pprint("score")
            pprint(score)
            return 1
        
        # paddle
        if what == 3:
            paddle_x = x
        elif what == 4:
            pprint("ball x")
            pprint(ball_x)
            ball_x = x


        grid[(x,y)] = what



def run_intcode(cur_proc) :

    # positions : 0 = position mode, 1 = immediate mode
    # ABCDE
    # 1002
    #
    #DE - two-digit opcode,      02 == opcode 2
    # C - mode of 1st parameter,  0 == position mode
    # B - mode of 2nd parameter,  1 == immediate mode
    # A - mode of 3rd parameter,  0 == position mode, omitted due to being a leading zero

    params = { 1 : 3, 2 : 3, 3 : 1,    4 : 1,    5 : 2,    6 : 2,    7 : 3,    8 : 3, 9 : 1, 99:0 }

    pos = processor[cur_proc]['position']

    while 1:
        instr = processor[cur_proc]['program'][pos]

        op = instr % 100;

        mode1 = int( instr / 100 ) % 10;
        mode2 = int( instr / 1000 ) % 10;
        mode3 = int( instr / 10000 ) % 10;

        reg1 = processor[cur_proc]['program'].get(pos+1,0)
        reg2 = processor[cur_proc]['program'].get(pos+2,0)
        reg3 = processor[cur_proc]['program'].get(pos+3,0)

        v1 = reg1

        if (op != 3) :
            if mode1 == 0:  v1 = processor[cur_proc]['program'].get(reg1,0)
            if mode1 == 2:  v1 = processor[cur_proc]['program'].get(reg1 + processor[cur_proc]['relative_base'],0)
        else:
            if mode1 == 2:  v1 += processor[cur_proc]['relative_base']

        v2 = reg2
        if mode2 == 0:  v2 = processor[cur_proc]['program'].get(reg2,0)
        if mode2 == 2:  v2 = processor[cur_proc]['program'].get(reg2 + processor[cur_proc]['relative_base'],0)

        v3 = reg3
        if mode3 == 2:  v3 += processor[cur_proc]['relative_base']

        if op == 1 :
            processor[cur_proc]['program'][ v3 ] = v1 + v2

        elif op == 2 :
            processor[cur_proc]['program'][ v3 ] = v1 * v2

        elif op == 3 :
            get_input(cur_proc)
            processor[cur_proc]['program'][ v1 ] = processor[cur_proc]['io'].popleft()

        elif op == 4 :
             processor[cur_proc]['io'].append(v1)
             process_output(cur_proc)
        
        elif op == 5 :
            if v1 > 0:
                pos = v2;
                continue
        
        elif op == 6 :
            if v1 == 0 :
                pos = v2
                continue

        elif op == 7 :
            if v1 < v2 :
                processor[cur_proc]['program'][ v3 ] = 1
            else :
                processor[cur_proc]['program'][ v3 ] = 0
        
        elif op == 8 :
            if v1 == v2 :
                processor[cur_proc]['program'][ v3 ] = 1
            else :
                processor[cur_proc]['program'][ v3 ] = 0
       
        elif op == 9 :
            processor[cur_proc]['relative_base'] += v1;

        elif op == 99 :
            return processor[cur_proc]['io']
        
        else :
            sys.exit("Unknown argument found")

        shift = params[ op ] + 1;
        pos = pos + shift;



# ------- MAIN ----------

def main(input_file,mode):

    inp = open(input_file).read().strip().split(',')
    data = list(map(int, inp))

    program_param['mode'] = 'normal';
    program_param['program_end'] = 0;

    phase_list = ''
    if program_param['mode'] == 'normal':
        phase_list='0'

    if program_param['mode'] == 'feedback':
        phase_list = '56789'


    max = 0

    for combo in permutations(phase_list,len(phase_list)):
        program_param['program_end'] = 0;

        amp = ['A']

        # initialize the processors

        input = 0;

        for phase in combo :
            cur_proc = amp.pop(0)
            processor[cur_proc] = {}
            processor[cur_proc]['phase']  = phase
            processor[cur_proc]['position'] = 0
            processor[cur_proc]['input']  = 0
            processor[cur_proc]['output']   = 0
            processor[cur_proc]['phase_set']   = 0
            processor[cur_proc]['program']   = {}
            processor[cur_proc]['io'] = deque()
            #processor[cur_proc]['io'].append(mode)
            processor[cur_proc]['relative_base']   = 0
            processor[cur_proc]['x']   = 50
            processor[cur_proc]['y']   = 50
            processor[cur_proc]['direction']   = '^'

            i = 0
            for instr in data:
                 processor[cur_proc]['program'][i]   = instr               
                 i+=1

            processor[cur_proc]['program'][0] = 2;
        end = 0;

        while (end == 0) :
            proc = ['A']
            
            # loop through the processors
            for procs in range(len(proc)) :
                cur_proc = proc[procs]
                next_proc = proc[(procs +1) % len(proc)]

                processor[next_proc]['input'] = run_intcode( cur_proc )

#                if (cur_proc == 'A') and (processor[next_amp,'input'] > max) :
 #                   max = processor[next_amp,'input']

                if ( procs == len(proc) - 1 ) : return processor[next_proc]['input']

                if (program_param['program_end'] ==1 ) :
                    end = 1;
                    break

                if program_param['mode'] == 'normal' : end =1

main('input',1)

grid = {}
painted = {}
main('input',1)

arr=np.zeros([100,100],dtype=str)

block_count = 0
for (a,b) in grid:
     if (grid[(a,b)] == 1):
        arr[a][b] =  '█'
     elif grid[(a,b)] == 2 :
        block_count += 1
     else :
        arr[a][b] = ' '

pprint("block count")
pprint(block_count)

pprint(score)
sys.exit()

arr = np.flip(arr,0)
for row in arr: # Part 2
        print(*row, sep='')
