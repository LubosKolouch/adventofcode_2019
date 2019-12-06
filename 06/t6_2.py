#! python3

import networkx as nx
from pprint import pprint

g = nx.Graph()

vertex_from = {}
vertex_to = {}

file = open('input','r')

for line in file:

    first, second = line.strip().split(')')
    vertex_from[first] = 1
    vertex_to[second] = 1

    g.add_edge(first, second)

print(len(nx.dijkstra_path(g,'YOU','SAN'))-3)
