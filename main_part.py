import os
import time

import holder as ch

differ = []
try:
    os.makedirs("texture2D")
except FileExistsError:
    pass
try:
    os.makedirs("textAsset")
except FileExistsError:
    pass
try:
    os.makedirs("out")
except FileExistsError:
    pass

texture2D = os.listdir('texture2D')
textAsset = os.listdir('textAsset')
text_ = []
for text in textAsset:
    text_.append(text.split('.'))
textAsset = []
for text in text_:
    textAsset.append(text[0])
textAsset = set(textAsset)
text_ = []
for text in texture2D:
    text_.append(text.split('.'))

texture2D = []
for text in text_:
    texture2D.append(text[0])

for name in texture2D:
    if name not in textAsset:
        print("切分文件丢失，请添加【" + name + ".atlas.txt】至TextAsset文件夹")
    else:
        differ.append( ch.body_cut(name))

        print(f'完成一个，为{name}')

print("完成，将于15s后关闭")



time.sleep(15)
