import os
import shutil
import json
from PIL import Image
from tools import find_file, get_namespace, get_animatedtex_from_gif
from configure import (OUTFILE, NAMESPACE_TEMPLATE, PACK_TEMPLATE, MASTER_FILENAME, MCMETA)

def main():
    supported_types = (
                    ".png",
                    ".jpeg",
                    ".jpg",
                    ".gif"
    )

    home = os.path.join(os.getcwd(), os.path.dirname(__file__))
    outroot = os.path.join(home,  OUTFILE)
    # too lazy to make enum
    filetype = 0

    user_image_path = os.path.join(os.getcwd(), find_file(os.getcwd(), supported_types))
    if user_image_path[-4:] == ".jpg":
        filetype = 1
    elif user_image_path[-5:] == ".jpeg":
        filetype = 2
    elif user_image_path[-4:] == ".gif":
        filetype = 3
    # make outfile
    os.mkdir(outroot)

    # copy template into target folder
    for root, subfolders, files in os.walk(os.path.join(os.path.dirname(__file__), PACK_TEMPLATE)):
        # relative path from the root of a resourcepack to the folder
        relative = root[len(PACK_TEMPLATE)+1:]

        # create all subfolders in root
        for subfolder in subfolders:
            os.mkdir(os.path.join(outroot, relative, subfolder))

        # create all files in root
        for single_file in files:
            shutil.copy2(os.path.join(home, root, single_file), os.path.join(outroot, relative, single_file))
    
    # copy namespace template into outroot/assets, replacing master.png with the file at user_image_path
    os.mkdir(os.path.join(outroot, "assets", get_namespace(MASTER_FILENAME)))
    for root, subfolders, files in os.walk(os.path.join(os.path.dirname(__file__), NAMESPACE_TEMPLATE)):
        relative = os.path.join("assets", get_namespace(MASTER_FILENAME), root[len(NAMESPACE_TEMPLATE)+1:])

        for subfolder in subfolders:
            os.mkdir(os.path.join(outroot, relative, subfolder))

        for single_file in files:
            if filetype == 0:
                shutil.copy2(user_image_path, os.path.join(outroot, relative, single_file))
            elif filetype == 1:
                #this is fucked but i dont want to fix it rn
                im1 = Image.open(user_image_path)
                im1.save(os.path.join(outroot, relative, (single_file[:-4] + ".png")))
                im1.close()
            elif filetype == 2:
                #this is fucked but i dont want to fix it rn
                im1 = Image.open(user_image_path)
                im1.save(os.path.join(outroot, relative, (single_file[:-5] + ".png")))
                im1.close()
            elif filetype == 3:
                # open gif
                im = Image.open(user_image_path)
                # turn gif into a bigass strip of frames
                final_image, fps = get_animatedtex_from_gif(im)
                # save strip
                final_image.save(os.path.join(outroot, relative, (single_file[:-4] + ".png")))
                im.close()
                final_image.close()
                # mcmeta json
                final_json = MCMETA
                # convert fps of gif to framerate
                final_json["animation"]["frametime"] = (1/fps) * 20
                json.dump(final_json, open(os.path.join(outroot, relative, (single_file[:-4] + ".png.mcmeta")), "x"), indent=4)
                



if __name__ == "__main__":
    main()