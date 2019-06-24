#!/usr/bin/env python
# coding: utf-8

# In[2]:


import librosa
from pathlib import Path
import numpy as np


# In[3]:


def getMfcc(filename):
    y, sr = librosa.load(filename)
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)


# In[4]:


p = Path("/Users/takumi/Downloads/wget/classical-sound.up.seesaa.net/image")
wav_list = sorted(list(p.glob("*.wav")))
wav_list[0]


# In[40]:


df2 = getMfcc(wav_list[1])


# In[41]:


df = getMfcc(wav_list[0])


# In[54]:


print(df)
print(df.shape)


# In[5]:


import matplotlib.pyplot as plt
import librosa.display
get_ipython().run_line_magic('matplotlib', 'inline')


# In[67]:


plt.figure(figsize=(10, 4))
librosa.display.specshow(df, x_axis='time',cmap="magma")
plt.ylabel("dimension")
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()

plt.figure(figsize=(10, 4))
librosa.display.specshow(df2, x_axis='time',cmap="magma")
plt.ylabel("dimension")
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()


# In[8]:


from sklearn.decomposition import PCA


# In[84]:


pca = PCA(n_components = 3)
pca.fit(df2)


# In[89]:


print(pca.components_.shape)


# In[76]:


print(df2)
print(pca.components_)


# In[6]:


from pathlib import PurePath
filename_list = [PurePath(str(x)).stem for x in wav_list]
print(filename_list)


# In[53]:


import re
composer_list2 = []
for x in filename_list:
    if re.match(r"[0-9]", x.split("-")[0]):
        composer_list2.append(x.split("-")[1])
    else:
        composer_list2.append(x.split("-")[0])
        
composer_list2.sort()
print(composer_list2)


# In[71]:


composer_list2[composer_list2.index("ELGAR")] = "Elgar"


# In[72]:


composer_list2


# In[12]:


from collections import Counter


# In[52]:


Counter(composer_list)


# In[44]:


from scipy.cluster.vq import whiten, kmeans, vq


# In[45]:


# エルボー法を適用したい
def show_dist(mfcc_data):
    # 正規化
    w = whiten(mfcc_data)
    dist_list = []
    for i in range(1,13):
        _, dist = kmeans(w, i)
        dist_list.append(dist)
    plt.plot(range(1, 13), dist_list, marker=".")
    plt.xlabel("Number of clusters")
    plt.ylabel("Values of Distortion")


# In[46]:


show_dist(df)


# In[47]:


show_dist(df2)


# In[56]:


df_w = whiten(df)
codebook, _ = kmeans(df_w, 3)
print(codebook)
code, dist = vq(df_w, codebook)
print(code)


# In[1]:


len(composer_list)


# In[ ]:




