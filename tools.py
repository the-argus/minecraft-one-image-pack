import os
from PIL import Image
from configure import MASTER_FILENAME, WRITING

def replace_textures(lines, textures_known=False):
    """
    recieves the json of the model as a dict
    and returns it with any "texture" or
    "textures" fields replaced with my master
    filename
    """
    final = {}
    for key in lines:
        if (key == "texture" or textures_known) and isinstance(lines[key], str):
            final[key] = MASTER_FILENAME
        elif (key == "textures" or textures_known) and isinstance(lines[key], list):
            final[key] = [MASTER_FILENAME]
        elif isinstance(lines[key], dict):
            if key == "textures":
                final[key] = replace_textures(lines[key], True)
            else:
                final[key] = replace_textures(lines[key])
        else:
            final[key] = lines[key]
    
    return final

def find_file(direct, supported_types):
    for single_file in next(os.walk(direct))[2]:
        for extension in supported_types:
            # store the path of the first image we find
            if single_file[-(len(extension)):] == extension:
                return single_file

def create_folder(target, root, read):
    """
    target is the absolute path of the root of the copied file structure
    root is the absolute path to the directory we're copying (the original dir)
    read is the absolute path of the root of the original file structure
    """
    if not WRITING:
        return None
    structure = target + root[len(read):]
    if not os.path.isdir(structure):
        os.mkdir(structure)
    else:
        print("Folder already exists!")
    return structure

def get_namespace(direct):
    final = ""
    for c in direct:
        if c == ':':
            return final
        final += c
    return None

def get_animatedtex_from_gif(gif_in):
    frames = 0
    duration = 0

    try:
        while 1:
            gif_in.seek(gif_in.tell()+1)
            frames += 1
            duration += gif_in.info['duration']
    except EOFError:
        pass
    # reset gif to first frame
    gif_in.seek(0)

    dst = Image.new('RGB', (gif_in.width, gif_in.height * frames))
    for i in range(frames):
        dst.paste(gif_in, (0, 0))
        dst.paste(gif_in, (0, gif_in.height*i))
        gif_in.seek(gif_in.tell()+1)
    framerate = frames / duration * 1000
    return (dst, framerate)