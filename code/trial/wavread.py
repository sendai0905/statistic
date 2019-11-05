import glob
import os
from collections import Counter

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Input, concatenate
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from mutagen.easyid3 import EasyID3


def readwave(file):
    wav, samplerate = librosa.load(file)
    return wav, samplerate


def MelFilterBank(y, sr):
    return librosa.feature.melspectrogram(y=y, sr=sr)


def makeArtistList():
    path = "C:/Users/Takumi/Desktop/statistic/data/mp3/composer/"
    l = ['Beethoven', 'Franz Joseph Haydn', 'J.S. Bach']
    artist_list = []
    for name in l:
        print('{} process start.'.format(name))
        p = path + name + '/cut/'
        file_count = len(os.listdir(p))
        l2 = [name] * file_count
        artist_list.extend(l2)

    counter = Counter(artist_list)
    print(counter)

    return artist_list


def makeLSTMmodel(hidden=128, input_shape=(128,)):
    model = Sequential()
    model.add(LSTM(hidden, input_shape=input_shape))
    model.add(Dense(128))
    model.compile(loss="categorical_crossentropy", optimezer="adam")
    return model


if __name__ == "__main__":
    artist_list = makeArtistList()
    # print(makeArtistList())
    path = "C:/Users/Takumi/Desktop/statistic/data/wav/"
    wav_list = sorted(list(glob.glob(path + "*.wav")))
    for i in range(3):
        wav, sr = readwave(wav_list[i])
        print(wav.shape)
        print(sr)
        t = np.arange(0, len(wav)) / sr
        m = MelFilterBank(wav, sr)
        print(m)
        print(m.shape)

    # 波形をプロット
    # plt.plot(m)
    # plt.xlabel("time [ms]")
    # plt.ylabel("amplitude")
    # plt.savefig("waveform.png")
    # plt.show()
    # librosa.display.specshow(librosa.power_to_db(
    #     m, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
    # plt.colorbar(format='%+2.0f dB')
    # plt.title('Mel spectrogram')
    # plt.tight_layout()
    # plt.savefig("waveform.png")
    # plt.show()
