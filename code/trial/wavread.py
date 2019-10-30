from preprocessing import makeComposerList
from keras.models import Sequential
from keras.layers import Input, Dense, concatenate
from keras.layers.recurrent import LSTM
from keras.callbacks import EarlyStopping
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt


def readwave(file):
    wav, samplerate = librosa.load(file)
    return wav, samplerate


def MelFilterBank(y, sr):
    return librosa.feature.melspectrogram(y=y, sr=sr)


def makeLSTMmodel(hidden):
    model = Sequential()
    model.add(LSTM(hidden, input_shape=(),))
    model.add(Dense())
    model.compile(loss="categorical_crossentropy", optimezer="")
    return model


if __name__ == "__main__":
    wav, sr = readwave("J.S.Bach-invention-No.1-Harpsi.wav")
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
    librosa.display.specshow(librosa.power_to_db(
        m, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    plt.savefig("waveform.png")
    plt.show()
