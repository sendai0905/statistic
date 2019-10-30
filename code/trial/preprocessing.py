import glob
import os
import re
import shutil

import numpy as np
import pydub
from mutagen.easyid3 import EasyID3


def makeComposerList():
    p = "/Volumes/test/"  # 対応するパスに変更
    mp3_list = sorted(list(glob.glob(p + "*.mp3")))
    print(len(mp3_list))
    print(mp3_list[0])

    classic_mp3_list = []
    for x in mp3_list:
        try:
            if EasyID3(x)["genre"][0] == "Classical":
                classic_mp3_list.append(x)
                shutil.move(x, "/Volumes/test/classic/" + x.split("/")[3])
                print(len(classic_mp3_list))
        except Exception as e:
            print(x, e.args)
            continue

    return classic_mp3_list


def to_wav():
    path = "/Volumes/test/classic/mp3/"
    mp3_list = sorted(list(glob.glob(path + "*.mp3")))
    for file in mp3_list:
        filename = file.replace("mp3", "wav")
        pydub.AudioSegment.from_mp3(file).export(filename, format="wav")
        print("{}を生成しました".format(filename))


if __name__ == "__main__":
    # print(makeComposerList())
    to_wav()
