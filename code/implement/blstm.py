from keras.models import Model
from keras.layers import Input, Dense, concatenate
from keras.layers.recurrent import LSTM
from keras.callbacks import EarlyStopping
import numpy as np
import matplotlib.pyplot as plt

"""
参考:
https://www.researchgate.net/publication/224929665_Universal_Onset_Detection_with_Bidirectional_Long-Short_Term_Memory_Neural_Network

input_units = 160
3 hidden layers * 2(双方向なので)
LSTM units = 20
output layer units = 2
出力層:softmax(onset or nonset)
損失関数:cross entropy
"""

main_input = Input(shape=(160,), name="main_input")

lstm_1 = LSTM(20)(main_input)
lstm_2 = LSTM(20)(lstm_1)
lstm_3 = LSTM(20)(lstm_2)

blstm_1 = LSTM(20, go_backwards=True)(main_input)
blstm_2 = LSTM(20, go_backwards=True)(blstm_1)
blstm_3 = LSTM(20, go_backwards=True)(blstm_2)

merged_3 = concatenate([lstm_3, blstm_3], axis=-1)

main_output = Dense(2, activation="sigmoid")

model = Model(inputs=main_input, outputs=main_output)

model.compile(optimizer="SGD", loss="categorical_crossentropy")

early_stopping = EarlyStopping(monitor="val_loss", patience=20, mode="auto")
