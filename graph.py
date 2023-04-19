
import json
import re
from xml.dom import minidom

from tqdm import tqdm
import os
import requests

url = "https://s3.amazonaws.com/wikia_xml_dumps/b/ba/backrooms_pages_current.xml.7z"

number_pattern_str = r"\d+(\.\d+)?"
number_pattern = re.compile(number_pattern_str)
level_pattern_str = r"Level ("+number_pattern_str+")"
level_title_pattern = re.compile("^"+level_pattern_str)
level_pattern = re.compile(level_pattern_str)

levels = []
failures = []

if os.path.exists("levels.json") and os.path.exists("failures.json"):
    with open("levels.json", "r") as f:
        levels = json.load(f)
    with open("failures.json", "r") as f:
        failures = json.load(f)
else:
    file = "backrooms_pages_current.xml"
    archive = "backrooms_pages_current.xml.7z"
    if not os.path.exists(file):
        print("Downloading file...")
        r = requests.get(url, allow_redirects=True)
        open(archive, 'wb').write(r.content)
        print("Extracting file...")
        os.system("7z x "+archive)
        
    data = minidom.parse(file)
    pages = data.getElementsByTagName("page")
    
    level_pages = []
    for page in pages:
        title = page.getElementsByTagName("title")[0].firstChild.data
        if level_title_pattern.match(title):
            text = page.getElementsByTagName("text")[0].firstChild.data
            level_pages.append((title, text))
    
    for title, text in tqdm(level_pages):
        number = number_pattern.search(title).group()
        number = float(number)
        entrances = []
        exits = []
        after_entrances = False
        after_exits = False
        for line in text.splitlines():
            if "==" in line and "Entrances" in line:
                after_entrances = True
                continue
            if "==" in line and "Exits" in line:
                after_exits = True
                continue
            if "{{Collapse" in line and after_exits:
                break
            if after_entrances and not after_exits:
                entrances.append(line)
            if after_exits:
                exits.append(line)
                
        entrances = "".join(entrances)
        exits = "".join(exits)
        
        entrace_numbers = [float(m.group(1)) for m in re.finditer(level_pattern, entrances)]
        exit_numbers = [float(m.group(1)) for m in re.finditer(level_pattern, exits)]
        
        entrace_numbers = set(entrace_numbers) - {number}
        exit_numbers = set(exit_numbers) - {number}
        
        entrace_numbers = sorted(list(entrace_numbers))
        exit_numbers = sorted(list(exit_numbers))
        
        levels.append({
            "number": number,
            "entrances": entrace_numbers,
            "exits": exit_numbers,
            "title": title,
            "text": text
        })
            
    with open("levels.json", "w") as f:
        json.dump(levels, f)
    with open("failures.json", "w") as f:
        json.dump(failures, f)

print("Found %d levels" % len(levels))
print("Failed %d levels" % len(failures))

from pyvis.network import Network

net = Network()

def id_from_number(n: float) -> str:
    if n == int(n):
        return str(int(n))
    else:
        return str(n)

nodes = set()
for level in levels:
    nodes.add(id_from_number(level["number"]))

edges = set()
for level in levels:
    for entrance in level["entrances"]:
        node_from = id_from_number(entrance)
        node_to = id_from_number(level["number"])
        edges.add((node_from, node_to))
        nodes.add(node_from)
        nodes.add(node_to)
    for exit in level["exits"]:
        node_from = id_from_number(level["number"])
        node_to = id_from_number(exit)
        edges.add((node_from, node_to))
        nodes.add(node_from)
        nodes.add(node_to)
        
# max = None
max = 10
        
for node in nodes:
    if max is None or float(node) <= max:
        net.add_node(node, label="Level "+node)
        
for edge in edges:
    v1 = float(edge[0])
    v2 = float(edge[1])
    if max is None or (v1 <= max and v2 <= max):
        net.add_edge(*edge)
    

net.show("connection"+("" if max is None else "_"+str(max))+".html")
