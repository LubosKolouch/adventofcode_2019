#! python3

import sys
from pprint import pprint
import numpy as np
from itertools import permutations
import csv
from collections import deque,defaultdict
import networkx as nx

grid = defaultdict(str)
portals = defaultdict(str)

inner_portals = defaultdict(str)
outer_portals = defaultdict(str)

start = end = None

def process_portal_row(row,offset) :
    global outer_portals
    global inner_portals
    global start
    global end

    avoid_chars = [' ','#','.']
    for i in range(len(data[row])) :
        if grid.get((row,i)) in avoid_chars : continue
        portal_name =  grid[row,i] + grid[row+1,i]

        if (portal_name == 'AA') :
            start = (row+offset,i)
            continue

        if (portal_name == 'ZZ') :
            end = (row+offset,i)
            continue

        if (row == 0) or (row == 119) :
            # outer portals
            outer_portals[portal_name] = (row+offset,i)
        else :
            inner_portals[portal_name] = (row+offset,i)

def process_portal_column(col,offset) :
    global outer_portals
    global inner_portals

    avoid_chars = [' ','#','.']
    for i in range(len(data)) :
        if grid.get((i,col)) in avoid_chars : continue
        portal_name =  grid[i,col] + grid[i,col+1]

        if (col == 0) or (col == 117) :
            # outer portals
            outer_portals[portal_name] = (i,col+offset)
        else :
            inner_portals[portal_name] = (i,col+offset)


# ------- MAIN ----------
assert len(sys.argv) == 2

inp = open(sys.argv[1]).read().split('\n')

data = list(map(str, inp))

# first load the input to a grid

for i in (range(len(data))) :
    for j in (range(len(data[i]))) :
        grid[(i,j)] = data[i][j]

# convert the grid to graph
g = nx.Graph()

max_path = 0

for x,y in grid:
    if grid.get((x,y)) != ".": continue

    if grid.get((x-1,y),0) == '.' : g.add_edge((x,y), (x-1,y))
    if grid.get((x+1,y),0) == '.' : g.add_edge((x,y), (x+1,y))
    if grid.get((x,y-1),0) == '.' : g.add_edge((x,y), (x,y-1))
    if grid.get((x,y+1),0) == '.' : g.add_edge((x,y), (x,y+1))

base_grid = g.copy()
# find the portals

process_portal_row(0,2)
process_portal_row(31,-1)
process_portal_row(88,2)
process_portal_row(119,-1)

process_portal_column(0,2)
process_portal_column(31,-1)
process_portal_column(86,2)
process_portal_column(117,-1)

grid_part1 = g.copy()

for port in outer_portals:
    grid_part1.add_edge( (inner_portals[port]+(0,)), outer_portals[port]+(0,) )

for fr,to in base_grid.edges() :
        grid_part1.add_edge((fr[0],fr[1],0),(to[0],to[1],0))

start = start+(0,)
end = end+(0,)

print("Part 1:",len(nx.dijkstra_path(grid_part1,start,end))-1)

# Part2

grid_part2 = nx.Graph()

max_levels = 26

for level in range(max_levels):

    for fr,to in base_grid.edges() :
        grid_part2.add_edge((fr+(level,)),(to+(level,)))

    for port in outer_portals:
        grid_part2.add_edge( (inner_portals[port] + (level,)), (outer_portals[port] + (level +1,) ) )
print("Part 2:",len(nx.dijkstra_path(grid_part2,start,end))-1)
