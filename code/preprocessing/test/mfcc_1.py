# %%
import librosa
import towav


# %%
def getMfcc(filename):
    y, sr = librosa.load(filename)
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)


# %%
m, w = towav.appendList()
print(w)
"""
df = getMfcc(w[0])
print(df)
"""
# %%
