
import json
import os
import shutil

with open("levels.json", "r") as f:
    levels = json.load(f)
        
out_dir = "pages"
if os.path.exists(out_dir):
  shutil.rmtree(out_dir)
os.mkdir(out_dir)
    
for level in levels:
  with open(os.path.join(out_dir, str(level["number"])+".md"), "a") as f:
    f.write(level["text"])
