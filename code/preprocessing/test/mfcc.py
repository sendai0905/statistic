# %%
import librosa
import librosa.display
import matplotlib.pyplot as plt


def getMfcc(filename):
    y, sr = librosa.load(filename)
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)


hoge = getMfcc('hoge.wav')
print(hoge)
print(hoge.shape)
print(hoge.size)

plt.figure(figsize=(10, 4))
librosa.display.specshow(hoge, x_axis='time')
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()
plt.show()
