"""
DO NOT USE
this is for developer purposes only.
it generates the template pack.
can be used to update this tool to
a new version of minecraft.
you do still have to manually create
namespace_template for each version,
if that changes
"""


import sys
import os
import json
import pathlib

from tools import (replace_textures, create_folder)
from configure import (WRITING, NAME)

def main():
    try:
        read_path = sys.argv[1]
    except IndexError:
        print("Absolute path of default minecraft resourcepack required.")
        return
    target_path = os.path.join(sys.path[0], NAME)

    file_exceptions = [
                "gpu_warnlist.json"
    ]

    dir_exceptions = [
                "textures",
                "blockstates",
                "texts",
                "font",
                "lang",
                "shaders",
                "realms"
    ]

    for root, subs, files in os.walk(read_path):
        broken = False
        print(target_path)
        for exception in dir_exceptions:
            if os.path.sep + exception + os.path.sep in root or root.find(os.path.sep + exception) == (len(root)-1)-(len(exception+os.path.sep)-1):
                broken = True
                break
        if broken:
            continue
        
        structure = create_folder(target_path, root, read_path)

        for single_file in files:
            if (single_file[-5:] == ".json" and single_file not in file_exceptions) and WRITING:
                json.dump(  replace_textures(json.load(open(os.path.join(root, single_file), "r"))),
                            open(os.path.join(structure, single_file), "w"),
                            indent=4
                            )

if __name__ == "__main__":
    main()