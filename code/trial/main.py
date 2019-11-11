# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import glob
import os
# +
import sys
from collections import Counter

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from keras import regularizers
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers.recurrent import LSTM
from keras.models import Sequential, model_from_json
from keras.optimizers import Adam
from keras.utils import np_utils
from mutagen.easyid3 import EasyID3

# -

def makeArtistList():
    path = "/home/Takumi/data/"
    l = ['Beethoven', 'Haydn', 'Bach']
    artist_list = []
    for i, name in enumerate(l):
        print('{} process start.'.format(name))
        p = path + name + '/cut/'
        file_count = len(os.listdir(p))
        l2 = [i] * file_count
        artist_list.extend(l2)

    counter = Counter(artist_list)
    print(counter)
    
    return artist_list


artist_list = makeArtistList()


# +
def readwave(file):
    wav, samplerate = librosa.load(file)
    return wav, samplerate


def MelFilterBank(y, sr):
    return librosa.feature.melspectrogram(y=y, sr=sr)


# -

path = "/home/Takumi/data/"
name_list = ['Beethoven', 'Haydn', 'Bach']
data_list = []
for name in name_list:
    print('{} process start.'.format(name))
    p = path + name + '/cut/'
    wav_list = sorted(list(glob.glob(p + "*.wav")))
    data_list.extend(wav_list)
print(len(data_list))

data_x = np.empty([128, 1292])
for i in range(len(data_list)):
    wav, sr = readwave(data_list[i])
#     print(wav.shape)
#     print(sr)
    t = np.arange(0, len(wav)) / sr
    m = MelFilterBank(wav, sr)
#     print(m)
#     print(m.shape)
#     if not i:
#         data_x = np.stack([data_x, m], 0)
#     else:
#         data_x = np.r_[data_x, m]
    data_x = np.r_['0, 3, -1', data_x, m]
    
    if not i % 100:
        print(data_x.shape)

data_x = np.delete(data_x, 0, 0)
print(data_x.shape)


def makeLSTMmodel(hidden=128, input_shape=(128, 1292,)):
    model = Sequential()
    model.add(LSTM(units=hidden, dropout=0.2, input_shape=input_shape, return_sequences=True))
    model.add(LSTM(units=hidden, dropout=0.2, input_shape=input_shape, kernel_regularizer=regularizers.l2(0.001)))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=1e-3), metrics=['accuracy'])
    return model


data_y = np.array(artist_list)

# data_y = np.delete(data_y, 0)
data_y = np_utils.to_categorical(data_y, 3)
print(data_y.shape)

model = makeLSTMmodel()
model.summary()
early_stopping = EarlyStopping(monitor="val_loss", patience=10, mode="auto")
# reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=5, factor=0.5, min_lr=0.0001, verbose=1)
# history = model.fit(data_x, data_y, batch_size=64, epochs=100, validation_split=0.2, callbacks=[early_stopping, reduce_lr])
history = model.fit(data_x, data_y, batch_size=64, epochs=100, validation_split=0.2, callbacks=[early_stopping])

with open('model.json', 'w') as json_file:
    json_file.write(model.to_json())
model.save_weights('main1.h5')

model_r = model_from_json(open('model.json', 'r').read())
model_r.load_weights('main1.h5')
model_r.compile(loss="categorical_crossentropy", optimizer=Adam(lr=1e-3), metrics=['accuracy'])
history_r = model_r.fit(data_x, data_y, batch_size=64, epochs=100, validation_split=0.2, callbacks=[early_stopping])

del model
del early_stopping
# del reduce_lr
del history


print("{}{: >25}{}{: >10}{}".format('|','Variable Name','|','Memory','|'))
print(" ------------------------------------ ")
for var_name in dir():
    if not var_name.startswith("_"):
        print("{}{: >25}{}{: >10}{}".format('|',var_name,'|',sys.getsizeof(eval(var_name)),'|'))
# -

del m
del t
del wav


# +
# %matplotlib inline

def plot_history(history):
    plt.figure(figsize=(8, 10))
    plt.subplots_adjust(hspace=0.3)
    
    plt.subplot(2, 1, 1)
    plt.plot(history.history['accuracy'], '-', label='accuracy')
    plt.plot(history.history['val_accuracy'], '-', label='val_acc')
    plt.title('model accuracy')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.legend(loc='lower right')
    
    plt.subplot(2, 1, 2)
    plt.plot(history.history['loss'], '-', label='loss')
    plt.plot(history.history['val_loss'], '-', label='val_loss')
    plt.title('model loss')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(loc='upper right')
    
    plt.show()
    
plot_history(history_r)
plt.savefig('graph.png')
# -

with open('model.json', 'w') as json_file:
    json_file.write(model_r.to_json())
model_r.save_weights('main1.h5')
