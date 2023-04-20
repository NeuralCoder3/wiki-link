
import json

start = 0
goal = 100
avoid = []

with open("levels.json", "r") as f:
    levels = json.load(f)
    
nodes = set()
edges = set()
for level in levels:
    nodes.add(level["number"])
    for entrance in level["entrances"]:
        edges.add((entrance, level["number"]))
        nodes.add(entrance)
    for exit in level["exits"]:
        edges.add((level["number"], exit))
        nodes.add(exit)

assert(start in nodes)
assert(goal in nodes)

nodes = nodes - set(avoid)

remove = set()
for v1,v2 in edges:
    if v1 in avoid or v2 in avoid:
        remove.add((v1,v2))
        
edges = edges - remove


connections = {}
for v in nodes:
    if v not in connections:
        connections[v] = []

for v1,v2 in edges:
    if v1 not in nodes or v2 not in nodes:
      continue
    connections[v1].append(v2)

path_count = 20

import networkx as nx
import shortestpaths as sp

# G = nx.Graph()
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

paths = sp.k_shortest_paths(G, start, goal, k=path_count)
sp.print_paths(paths)
# sp.plot_paths(paths, G)

# print(paths)
    
# for level in levels:
#     if level["number"] in paths[0][0]:
#         print(level["title"])
#         print("Entrances: %s" % level["entrances"])
#         print("Exits: %s" % level["exits"])
#         # print(level["text"])
#         print()
