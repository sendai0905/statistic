from preprocessing import makeComposerList
# from keras.models import Model
# from keras.layers import Input, Dense, concatenate
# from keras.layers.recurrent import LSTM
# from keras.callbacks import EarlyStopping
import numpy as np
import soundfile as sf
import librosa
import matplotlib.pyplot as plt


def readwave(file):
    wav, samplerate = sf.read(file)
    return wav, samplerate


def MelFilterBank(file):
    pass
    # return m


def makeLSTMmodel():
    pass
    # return model


if __name__ == "__main__":
    wav, sr = readwave(
        r'C:\Users\Takumi\Desktop\statistic\data\041-Chopin-Nocturne-No2.wav')
    print(wav.shape)
    print(sr)
    t = np.arange(0, len(wav)) / sr

    # 波形をプロット
    plt.plot(t, wav)
    plt.xlabel("time [ms]")
    plt.ylabel("amplitude")
    plt.savefig("waveform.png")
    plt.show()
