#! python3

from pprint import pprint
import numpy as np
import re
import copy
from math import gcd

def lcm(num1,num2):
    return (num1*num2)//gcd(num1,num2)

moons = {}

all_moons = {}
cachex = {}
cachey = {}
cachez = {}

seenx = 0
seeny = 0
seenz = 0

moon = 0
step = 0

# remember - best to read, strip and reshape in one line
with open('input', 'r') as data:

    moons[step] = {}
    moons[step]['energy'] = 0

    for line in data :
        all_moons[moon] = 1
        line = line.strip()
        moons[step][moon] = {}
        moons[step][moon]['vx'] = 0
        moons[step][moon]['vy'] = 0
        moons[step][moon]['vz'] = 0
        
        #data = np.array(list(data.read().strip())).reshape((-1, 6, 25))
        pairs = line.strip('<>').split(', ')

        for pair in pairs:
            coord, value = pair.split('=')
            moons[step][moon][coord] = int(value)

        moons[step][moon]['energy'] =  (abs(moons[step][moon]['x']) +  abs(moons[step][moon]['y']) +  abs(moons[step][moon]['z']) ) * (  abs(moons[step][moon]['vx']) +  abs(moons[step][moon]['vy']) +  abs(moons[step][moon]['vz']))

        moons[step]['energy'] += moons[step][moon]['energy']

        moon += 1



while (1) :
    step += 1
    moons[step] = copy.deepcopy(moons[step-1])
    moons[step]['energy'] = 0
    hashx = 0;
    hashy = 0;
    hashz = 0;
    for m1 in all_moons:

        for m2 in all_moons:
            if moons[step-1][m1]['x'] < moons[step-1][m2]['x']: moons[step][m1]['vx'] += 1
            if moons[step-1][m1]['x'] > moons[step-1][m2]['x']: moons[step][m1]['vx'] -= 1

            if moons[step-1][m1]['y'] < moons[step-1][m2]['y']: moons[step][m1]['vy'] += 1
            if moons[step-1][m1]['y'] > moons[step-1][m2]['y']: moons[step][m1]['vy'] -= 1
    
            if moons[step-1][m1]['z'] < moons[step-1][m2]['z']: moons[step][m1]['vz'] += 1
            if moons[step-1][m1]['z'] > moons[step-1][m2]['z']: moons[step][m1]['vz'] -= 1

        #pprint("Before applying moon "+str(m1))
        #pprint(moons)
        moons[step][m1]['x'] = int(moons[step-1][m1]['x']) + int(moons[step][m1]['vx'])
        moons[step][m1]['y'] = int(moons[step-1][m1]['y']) + int(moons[step][m1]['vy'])
        moons[step][m1]['z'] = int(moons[step-1][m1]['z']) + int(moons[step][m1]['vz'])

        hashx = str(hashx) + ' ' + str(moons[step][m1]['x']) + ' ' + str(moons[step][m1]['vx'])
        hashy = str(hashy) + ' ' + str(moons[step][m1]['y']) + ' ' + str(moons[step][m1]['vy'])
        hashz = str(hashz) + ' ' + str(moons[step][m1]['z']) + ' ' + str(moons[step][m1]['vz'])

        moons[step][m1]['energy'] =  (abs(moons[step][m1]['x']) +  abs(moons[step][m1]['y']) +  abs(moons[step][m1]['z']) ) * (  abs(moons[step][m1]['vx']) +  abs(moons[step][m1]['vy']) +   abs(moons[step][m1]['vz']))

        moons[step]['energy'] += moons[step][m1]['energy']
        #pprint("After applying moon "+str(m1))
        #pprint(moons)

    if (hashx in cachex) and (seenx == 0) :
        pprint('x : '+str(step-1))
        seenx = step -1
    else:
        cachex[hashx] = 1

    if (hashy in cachey) and (seeny == 0) :
        pprint('y : '+str(step-1))
        seeny = step -1
    else:
        cachey[hashy] = 1

    if (hashz in cachez) and (seenz == 0) :
        pprint('z : '+str(step-1))
        seenz = step -1
    else:
        cachez[hashz] = 1

    if (step == 1000) : pprint("solution 1 : "); pprint(moons[step]); pprint(step)

    if (step % 1e4 == 0) : pprint(step)

    if (seenx and seeny and seenz) : 
        pprint(lcm(lcm(seenx,seeny),seenz))
        break

