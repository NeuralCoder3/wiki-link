
import json

start = 0
goal = 100
avoid = [11]

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

connections = {}
for v1,v2 in edges:
    if v1 not in nodes or v2 not in nodes:
      continue
    if v1 not in connections:
        connections[v1] = []
    connections[v1].append(v2)

# find shortest path using dijkstra's algorithm

# initialize distances
distances = {}
for node in nodes:
    distances[node] = float('inf')
distances[start] = 0

# initialize previous nodes
previous = {}
for node in nodes:
    previous[node] = None
    
# initialize unvisited nodes
unvisited = set(nodes)

while len(unvisited) > 0:
    # find node with smallest distance
    smallest = None
    for node in unvisited:
        if smallest is None or distances[node] < distances[smallest]:
            smallest = node
    # if smallest is None:
    #     print("Smallest is None")
    #     print("Unvisited: %s" % unvisited)
    #     print("Distances: %s" % distances)
    #     print("Previous: %s" % previous)
    #     print("Connections: %s" % connections)
    #     break
    # print("Smallest: %s" % smallest)
    # print("Distances: %s" % distances)
    # print("Previous: %s" % previous)
    # print("Connections: %s" % connections)
    unvisited.remove(smallest)
    if smallest == goal:
        break
    if smallest not in connections:
        continue
    for neighbor in connections[smallest]:
        # print("Neighbor: %s" % neighbor)
        alt = distances[smallest] + 1
        if alt < distances[neighbor]:
            distances[neighbor] = alt
            previous[neighbor] = smallest
        
# print("Distances: %s" % distances)
# print("Previous: %s" % previous)

# reconstruct path
path = []
node = goal
while node is not None:
    path.append(node)
    node = previous[node]
path.reverse()

print("Path: %s" % path)

    
for level in levels:
    if level["number"] in path:
        print(level["title"])
        print("Entrances: %s" % level["entrances"])
        print("Exits: %s" % level["exits"])
        # print(level["text"])
        print()
