
import json
import re
from xml.dom import minidom

from tqdm import tqdm
# from wikimarkup.parser import Parser
# try: 
#     from BeautifulSoup import BeautifulSoup
# except ImportError:
#     from bs4 import BeautifulSoup
import pickle
import os
import requests

url = "https://s3.amazonaws.com/wikia_xml_dumps/b/ba/backrooms_pages_current.xml.7z"

number_pattern_str = r"\d+(\.\d+)?"
number_pattern = re.compile(number_pattern_str)
level_pattern_str = r"Level ("+number_pattern_str+")"
level_title_pattern = re.compile("^"+level_pattern_str)
level_pattern = re.compile(level_pattern_str)

# parser = Parser()

levels = []
failures = []

if os.path.exists("levels.json") and os.path.exists("failures.json"):
    with open("levels.json", "r") as f:
        levels = json.load(f)
    with open("failures.json", "r") as f:
        failures = json.load(f)
    # with open("levels.pickle", "rb") as f:
    #     levels = pickle.load(f)
    # with open("failures.pickle", "rb") as f:
    #     failures = pickle.load(f)
else:
    file = "backrooms_pages_current.xml"
    archive = "backrooms_pages_current.xml.7z"
    if not os.path.exists(file):
        print("Downloading file...")
        r = requests.get(url, allow_redirects=True)
        open(archive, 'wb').write(r.content)
        # extract file
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
        # if "." in number:
        #     number = float(number)
        # else:
        #     number = int(number)
        # print(title)
        # if number == 6:
        if True:
        # try:
            # text_data = marko.parse(text)
            # print(text_data.children)
            # print(text_data.children[0])
            # print(dir(text_data.children[0]))
            # html_text = parser.parse(text)
            # # print(html_text)
            
            # html = BeautifulSoup(html_text, "html.parser")
            
            # # get inner text of first ul after h3 with Entrances
            # entrance_h3 = html.find("h3", text="Entrances")
            # exit_h3 = html.find("h3", text="Exits")
            # # text between entrances and exits
            # children = entrance_h3.parent.children
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
            # for child in children:
            #     if child == entrance_h3:
            #         after_entrances = True
            #         continue
            #     if child == exit_h3:
            #         after_exits = True
            #         continue
            #     if after_entrances and not after_exits:
            #         entrances.append(child.get_text())
            #     if after_exits:
            #         exits.append(child.get_text())
                    
            entrances = "".join(entrances)
            exits = "".join(exits)
            
            
            
            
            # try:
            #     entrances = html.find("h3", text="Entrances").find_next("ul").get_text()
            # except Exception as e:
            #     # get <p> instead
            #     entrances = html.find("h3", text="Entrances").find_next("p").get_text()
                
            # try:
            #     exits = html.find("h3", text="Exits").find_next("ul").get_text()
            # except Exception as e:
            #     exits = html.find("h3", text="Exits").find_next("p").get_text()
            
            
            # print("Entrances:", entrances)
            # find all level numbers in text
            # entrace_numbers = re.findall(level_pattern, entrances)
            # exit_numbers = re.findall(level_pattern, exits)
            
            entrace_numbers = [float(m.group(1)) for m in re.finditer(level_pattern, entrances)]
            exit_numbers = [float(m.group(1)) for m in re.finditer(level_pattern, exits)]
            
            entrace_numbers = set(entrace_numbers) - {number}
            exit_numbers = set(exit_numbers) - {number}
            
            entrace_numbers = sorted(list(entrace_numbers))
            exit_numbers = sorted(list(exit_numbers))
            
            # print("Entrances:", entrace_numbers)
            # print("Exits:", exit_numbers)
            
            levels.append({
                "number": number,
                "entrances": entrace_numbers,
                "exits": exit_numbers,
                "title": title,
                "text": text
            })
                
            
            
            # entraces = re.search(r"<h3.*>Entrances</h3>(.*?)<ul", html, re.DOTALL | re.MULTILINE)
            # print(entraces)
            
            
            # text between <h3 ...>Extrace*</h3> and next h3 (multiple lines)
            # entraces = re.search(r"<h3.*>Entrances</h3>(*?)<h3", html, re.DOTALL | re.MULTILINE)
            # entraces = re.findall(r"<h3.*>Entrances</h3>(.*?)<h3", html)
            # print("Entraces:", entraces)
            
            # find text of section === Entrances ===
            # exit(0)
        # except Exception as e:
        #     failures.append((title, str(e)))
        #     print("Failed:", title)
        #     print(html)
        #     print(text)
        #     print(e)
        #     # print stack trace
        #     import traceback; traceback.print_exc();
        #     exit(1)
            

    # export using json
    with open("levels.json", "w") as f:
        json.dump(levels, f)
    with open("failures.json", "w") as f:
        json.dump(failures, f)

    # export using pickle
    # with open("levels.pickle", "wb") as f:
    #     pickle.dump(levels, f)
    # with open("failures.pickle", "wb") as f:
    #     pickle.dump(failures, f)

print("Found %d levels" % len(levels))
print("Failed %d levels" % len(failures))


# for level in levels:
#     if level["number"] == 8.2e-10:
#         print("Title:", level["title"])
#         print("Entrances:", level["entrances"])
#         print("Exits:", level["exits"])
#         print("text:", level["text"])
        
# exit(0)
        


# for level in levels:
#     print(level["title"])
#     print("  Entrances:", level["entrances"])
#     print("  Exits:", level["exits"])

from pyvis.network import Network

net = Network()

def id_from_number(n: float) -> str:
    if n == int(n):
        return str(int(n))
    else:
        return str(n)
        # decimal notation (not scientific)
        # return "{:g}".format(n)

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
        # print("Adding node", node)
        net.add_node(node, label="Level "+node)
        
for edge in edges:
    v1 = float(edge[0])
    v2 = float(edge[1])
    # if v1 < 10 and v2 < 10:
    #     print("Adding edge", edge)
    if max is None or (v1 <= max and v2 <= max):
        net.add_edge(*edge)
    

net.show("connection"+("" if max is None else "_"+str(max))+".html")
