#! python3

import networkx as nx
from pprint import pprint

g = nx.DiGraph()

vertex_from = {}
vertex_to = {}

file = open('input','r')

for line in file:

    first, second = line.strip().split(')')
    vertex_from[first] = 1
    vertex_to[second] = 1

    g.add_edge(first, second)

sp = dict(nx.all_pairs_shortest_path_length(g))

count = 0

for item in sp:
    if (len(sp[item]) != 1):
        for sitem in sp[item]:
            if sp[item][sitem] != 0 : count += 1

print(count)
