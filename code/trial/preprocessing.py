import glob
import os
import shutil
from collections import Counter

import pydub
from mutagen.easyid3 import EasyID3


def genreFilter():
    path_mac = "/Volumes/test/"  # mac
    path_win = "C:/Users/Takumi/Desktop/statistic/data/mp3/"  # windows
    mp3_list = sorted(list(glob.glob(path_mac + "*.mp3")))
    if not len(mp3_list):
        mp3_list = sorted(list(glob.glob(path_win + "*.mp3")))
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
    # path = "/Volumes/test/classic/mp3/"
    path = "C:/Users/Takumi/Desktop/statistic/data/mp3/"
    mp3_list = sorted(list(glob.glob(path + "*.mp3")))
    for file in mp3_list:
        filename = file.replace("mp3", "wav")
        pydub.AudioSegment.from_mp3(file).export(filename, format="wav")
        print("{}を生成しました".format(filename))


def makeComposerList():
    path = "C:/Users/Takumi/Desktop/statistic/data/mp3/"
    mp3_list = sorted(list(glob.glob(path + "*.mp3")))
    for file in mp3_list:
        filename = file.split('\\')[-1]
        try:
            composer = EasyID3(file)['composer']
            shutil.move(file, path + "composer/" + filename)
        except Exception as e:
            print(file, e)


def makeFolder():
    path = "C:/Users/Takumi/Desktop/statistic/data/mp3/composer/"
    mp3_list = sorted(list(glob.glob(path + "*.mp3")))
    composer_list = []

    for file in mp3_list:
        composer_list.append(EasyID3(file)['composer'][0])

    c = Counter(composer_list)
    for name in c.keys():
        os.makedirs(path + name)

    for file in mp3_list:
        filename = file.split('\\')[-1]
        shutil.move(file, path + EasyID3(file)['composer'][0] + '/' + filename)
        print("{}を移動しました".format(filename))


def cutAudio():
    path = "C:/Users/Takumi/Desktop/statistic/data/mp3/composer/"
    l = ['Beethoven', 'Franz Joseph Haydn', 'J.S. Bach']
    for name in l:
        p = path + name
        mp3_list = sorted(list(glob.glob(p + "/*.mp3")))
        os.makedirs(p + '/cut', exist_ok=True)
        for file in mp3_list:
            filename = file.split('\\')[-1].split('.')[0]
            sound = pydub.AudioSegment.from_mp3(file)
            steps = (len(sound) - 30000) // 10000 + 1    # 10秒ごとに30秒切り出す
            for i in range(steps):
                try:
                    cut_sound = sound[i * 10000:i * 10000 + 30000]
                except:
                    cut_sound = sound[-30000:]

                cut_sound_name = p + '/cut/' + filename + '_' + str(i) + '.wav'
                cut_sound.export(cut_sound_name, format='wav')
                print('{}を生成しました'.format(cut_sound_name))


if __name__ == "__main__":
    # print(genreFilter())
    # to_wav()
    # makeComposerList()
    # makeFolder()
    cutAudio()
