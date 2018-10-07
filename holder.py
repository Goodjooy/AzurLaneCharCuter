import os

import PIL.Image as Image


class CutSpace(object):

    def __init__(self):
        self._xy = [0, 0]
        self._size = [0, 0]
        self._orig = [0, 0]
        self._offset = [0, 0]
        self._rotate = False

    def cuter(self, pic):
        """cut every part """
        """[pygame.Surface,(x,y)]:returns"""
        cut_sp = list(self._xy)
        cut_sp.extend([self._size[0] + self._xy[0], self._size[1] + self._xy[1]])

        if self._rotate:
            cut_sp = list(self._xy)

            cut_sp.extend([self._size[1] + self._xy[0], self._size[0] + self._xy[1]])

            cut = pic.rotate(-90)
            cut = pic.crop(cut_sp)



        else:
            cut = pic.crop(cut_sp)

        x, y = self._xy

        return [cut, (x, y)]

    def add_xy(self, x, y):
        self._xy = (x, y)

    def add_size(self, size_x, size_y):
        self._size = (size_x, size_y)

    def add_rotate(self, rotate_90=False):
        self._rotate = rotate_90

    def add_orig(self, orig_x, orig_y):
        self._orig = (orig_x, orig_y)

    def add_offset(self, offset_x, offset_y):
        self._offset = (offset_x, offset_y)

    def all_to_0(self):
        self._xy = ()
        self._size = ()
        self._orig = (0, 0)
        self._offset = (0, 0)
        self._rotate = False


def body_cut(name):
    try:
        os.makedirs("out\\" + name)
    except FileExistsError:
        pass

    pic = Image.open("Texture2D\\" + name + ".png")
    space = {'body_part': {}}
    loader = CutSpace()
    in_part = None
    differ = []

    with open("TextAsset\\" + name + ".atlas.txt", 'r', encoding='utf-8')as info:
        for line in info.readlines():

            line = line[:-1]

            if not line:
                continue

            elif line[-3:] == "png":
                space['name'] = line[:-4]

            elif line[0:4] == "size":
                line = line[5:]
                line = line.split(',')
                line = [int(line[0]), int(line[1])]
                space['size'] = line

            elif line[:6] == "format":
                space["format"] = line[8:-4]

            elif line[:6] == "filter":
                line = line[8:]
                line = line.split(',')
                space["filter"] = line

            elif line[:6] == "repeat":
                if line[8:] == 'none':
                    space['repeat'] = None
                else:
                    space['repeat'] = line[8:]

            else:
                if line[0] != ' ':
                    in_part = line
                    #try:
                    space['body_part'][line] = None
                    #except UnicodeDecodeError:
                    #    return "TextAsset\\" + name + ".atlas.txt"

                    loader.all_to_0()

                elif line[0] == ' ':
                    line = line[2:]

                    if line[:6] == 'rotate':
                        line = line[8:]
                        if line == "false":
                            loader.add_rotate(False)
                        elif line == "true":
                            loader.add_rotate(True)

                    elif line[:2] == 'xy':
                        line = line[4:]
                        line = line.split(',')
                        line = [int(line[0]), int(line[1])]
                        loader.add_xy(line[0], line[1])

                    elif line[:4] == 'size':
                        line = line[6:]
                        line = line.split(',')
                        line = [int(line[0]), int(line[1])]
                        loader.add_size(line[0], line[1])

                    elif line[:4] == 'orig':
                        line = line[6:]
                        line = line.split(',')
                        line = [int(line[0]), int(line[1])]
                        loader.add_orig(line[0], line[1])

                    elif line[:6] == "offset":
                        line = line[8:]
                        line = line.split(',')
                        line = [int(line[0]), int(line[1])]
                        loader.add_offset(line[0], line[1])

                    elif line[:5] == "index":
                        space['body_part'][in_part] = loader.cuter(pic)

    i = 0
    for key in space['body_part'].keys():

        if space['body_part'][key][0] is None:
            continue

        else:
            try:
                space['body_part'][key][0].save("out\\" + name + "\\" + key + ".png")
            except FileNotFoundError:
                space['body_part'][key][0].save("out\\" + name + "\\" + str(i) + ".png")

        i += 1

    return ""
