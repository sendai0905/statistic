import os
from pathlib import Path
from pydub import AudioSegment as AS

p = Path("/Users/takumi/Downloads/wget/classical-sound.up.seesaa.net/image")
mp3_posixpath_list = list(p.glob("*.mp3"))
mp3_list = []
wav_list = []

for i in range(len(mp3_posixpath_list)):
    mp3_list.append(str(mp3_posixpath_list[i]))
    wav_list.append(mp3_list[i].replace("mp3", "wav"))
    data = AS.from_mp3(mp3_list[i])
    data.export(wav_list[i], format="wav")
    os.remove(mp3_list[i])
    print("{}を削除しました".format(mp3_list[i]))
