from pathlib import Path, PurePath
import numpy as np
import re
import os
from collections import Counter
from mutagen.easyid3 import EasyID3
import pydub


def makeComposerList():
    p = Path(r"C:\Users\Takumi\Desktop\statistic\data")  # 対応するパスに変更
    mp3_list = sorted(list(p.glob("*.mp3")))
    # filename_list = [PurePath(str(x)).stem for x in wav_list]

    # print(filename_list)

    composer_list = []
    for x in mp3_list:
        # if re.match(r"[0-9]", x.split("-")[0]):
        #     composer_list.append(x.split("-")[1])
        # else:
        #     composer_list.append(x.split("-")[0])
        composer_list.append(EasyID3(x)['composer'])  # 'artist'かも

    composer_list.sort()
    num_of_composer = Counter(composer_list)
    print(num_of_composer)

    return composer_list


def to_wav(file):
    filename = file.split(".")[0] + ".wav"
    pydub.AudioSegment.from_mp3(file).export(filename, format="wav")
    os.remove(file)
    print("{}を削除しました".format(file))


if __name__ == "__main__":
    print(makeComposerList())
