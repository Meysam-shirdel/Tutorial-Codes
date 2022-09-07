# -*- coding: utf-8 -*-
"""Untitled17.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HsrvbzslvynNVvuAgbIpxq9mcIVBEe16
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_biclusters, make_blobs
from sklearn import model_selection

minxc1 = 2
maxxc1 = 5
minxc2 = 4
maxxc2 = 1

c1 = np.array(np.random.standard_normal((100,2)))+(minxc1,maxxc1)
c2 = np.array(np.random.standard_normal((100,2)))+(minxc2,maxxc2)
yc1 = np.ones((100,1), dtype=np.int32)
yc2 = np.zeros((100,1),dtype=np.int32)
Y = np.concatenate((yc1,yc2),axis=0)
X = np.concatenate((c1,c2),axis=0)
xtrain, xtest ,ytrain, ytest = model_selection.train_test_split(X,Y,test_size=0.1)
plt.plot(c1[:,0], c1[:,1], 'b.')
plt.plot(c2[:,0], c2[:,1], 'r.')

def train (slop, x, y):
  
  pointposition = slop*x[0] -x[1]
  target_slop = (x[1]+0.1) / x[0]
  error = target_slop - slop

  if y == 0 and pointposition <0 :
    slop = slop +error
  elif y == 1 and pointposition > 0:
    slop = slop +error
  #print(slop)
  return slop

w = np.random.rand(1,2)

init_slop = w[0,1] / w[0,0]

line = np.arange(np.min([minxc1,minxc2], axis=0)-2, np.max([maxxc1, maxxc2],axis=0)+2)
fig, ax = plt.subplots()

ax.plot(line ,init_slop*line,'b', linewidth=3 ,label="initial")
for i in range (200):
  init_slop = train(init_slop , X[i,:], Y[i,0])
  plt.plot(line ,init_slop*line,'g', linewidth=0.5 )

plt.plot(c1[:,0], c1[:,1], 'b.')
plt.plot(c2[:,0], c2[:,1], 'r.')
plt.plot(line, init_slop*line,'r--', linewidth=4,label="Final")
plt.legend()
plt.grid()
#plt.show()

pred = init_slop * c2[0:100,0]- c2[0:100,1]
print(pred)