#!python

import sys 
import numpy as np
from collections import defaultdict
from copy import deepcopy

def process_maze_part1(what):

    row,col = np.shape(what)
    value = 0
    pos = 0
    for i in range(row) :
        for j in range(col):
            #bug
            count = 0
            pos += 1
            if (i > 0) and (maze[i-1][j] == "#") :
                count += 1

            if (i < row-1) and (maze[i+1][j] == "#") :
                count += 1

            if (j < col-1) and (maze[i][j+1] == "#") :
                count += 1

            if (j > 0) and (maze[i][j-1] == "#") :
                count += 1

            if what[i][j] == '.' and (count == 1 or count == 2):
                what[i][j] = '#'

            elif what[i][j] == "#" and count != 1:
                    what[i][j] = '.'

            if what[i][j]=='#':
                value += (2 ** (pos-1))

    return what, value

def process_level(lev):
    row,col = np.shape(maze)
    value = 0

    for i in range(row) :
        for j in range(col):
            count = 0

            # rows - looking only up and down
            # for first row (0)
            if i == 0 :
                # up
                if levels[lev-1][1][2] == "#":
                    count += 1

                # down
                if levels[lev][1][j] == "#": 
                    count += 1

            # for second row (1)
            if i == 1 :

                # up
                if levels[lev][0][j] == "#": 
                    count += 1
        
                # down
                if j == 2:
                    for x in range(5):
                        if levels[lev+1][0][x] == "#":
                            count += 1
                else:
                    if levels[lev][2][j] == "#": 
                        count += 1                   

            # for third row (2)
            if i == 2 :
                 if j != 2:
                    # up
                    if levels[lev][1][j] == "#":
                        count += 1   

                    # down
                    if levels[lev][3][j] == "#":
                        count += 1   

            # for fourth row (3)
            if i == 3:
                
                # down
                if levels[lev][4][j] == "#": 
                    count += 1

                # up
                if j == 2:
                    for x in range(5):
                        if levels[lev+1][4][x] == "#":
                            count += 1
                else:
                 if levels[lev][2][j] == "#": 
                    count += 1                   

            # for fifth row (4)
            if i == 4:
                # down
                if levels[lev-1][3][2] == "#":
                    count += 1

                # up
                if levels[lev][3][j] == "#": 
                    count += 1

            # ------------ process columns, looking left and right -------
            # for first column (0)
            if j == 0 :
                # left
                if levels[lev-1][2][1] == "#":
                    count += 1

                # right
                if levels[lev][i][1] == "#": 
                    count += 1

            # for second column (1)
            if j == 1 :

                # left
                if levels[lev][i][0] == "#": 
                    count += 1
                
                # right
                if i == 2:
                    for x in range(5):
                        if levels[lev+1][x][0] == "#":
                            count += 1
                else:
                 if levels[lev][i][2] == "#": 
                    count += 1                   

            # for third column (2)
            if j == 2 :
                 if i != 2:

                    # left
                    if levels[lev][i][1] == "#":
                        count += 1   

                    # right
                    if levels[lev][i][3] == "#":
                        count += 1   

            # for fourth column (3)
            if j == 3:
                # right
                if levels[lev][i][4] == "#": 
                    count += 1
    
                # left
                if i == 2:
                    for x in range(5):
                        if levels[lev+1][x][4] == "#":
                            count += 1
                else:
                 if levels[lev][i][2] == "#": 
                    count += 1                   

            # for fifth column (4)
            if j == 4:
                #left
                if levels[lev][i][3] == "#": 
                    count += 1
              
                # right
                if levels[lev-1][2][3] == "#":
                    count += 1


            if levels[lev][i][j] == '.' and (count == 1 or count == 2):
                new_levels[lev][i][j] = '#'


            elif levels[lev][i][j] == "#" and count != 1:
                new_levels[lev][i][j] = '.'


            if new_levels[lev][i][j] == '#':
                value += 1

    return value




# MAIN
assert len(sys.argv) == 2

#levels are for part 2
levels = defaultdict()

values = defaultdict(int)
value = 0

with open(sys.argv[1]) as f:
        maze = np.array([list(s.strip()) for s in f.readlines()])

levels[0] = maze

while values[value] != 2:
    maze, value = process_maze_part1(maze.copy())
    values[value] += 1

print("Part 1: ",value)

# Part2
# pre-generate empty levels
for i in range(-202,202):
    levels[i] = np.full((5,5),'.')


with open(sys.argv[1]) as f:
        maze = np.array([list(s.strip()) for s in f.readlines()])

levels[0] = maze
for i in range(-202,202):
    levels[i][2][2] = '?'

# 200 minutes
new_levels = defaultdict()

for minute in range(1,201):
    #print('------------',minute,'----------')

    new_levels = deepcopy(levels)

    bugs_count = 0
    # process the arrays
    for lev in range(-201,201):
        bugs_count += process_level(lev)

    #print("minute ",minute," bugs ",bugs_count)
    levels = deepcopy(new_levels)
    #for i in range(-6,7):
    #    print(i)
    #    print(levels[i])
print("Part2: ",bugs_count)
    
