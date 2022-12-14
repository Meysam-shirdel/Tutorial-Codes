# -*- coding: utf-8 -*-
"""Untitled21.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1py5IoMIlgWi54FScpOYS45glIfA0V8GQ
"""

import numpy as np
import matplotlib.pyplot as plt
from  sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

#C1 = np.random.standard_normal((200,2),)+(2,3)
c1 = np.random.normal(0 , 0.7, (200,2))+(1.5,4.5)
yc1 = np.ones((200,1),dtype=np.int32)
c2 = np.concatenate((np.random.uniform([0,1],[3.5,2],(100,2)),np.random.uniform([3,2],[4,7],(100,2))),axis=0)
yc2 = np.zeros((200,1),dtype=np.int32)

X = np.concatenate((c1,c2),axis = 0)
Y = np.concatenate((yc1,yc2),axis = 0)
plt.plot(c1[:,0], c1[:,1], 'b.')
plt.plot(c2[:,0], c2[:,1], 'r.')

xtrain, xtest, ytrain, ytest = train_test_split(X,Y, test_size=0.2)

class MyModel:
  def __init__(self) -> None:
      self.wh = np.array(np.random.rand(2,2))
      self.bh = np.ones((2,1))
      self.wout = np.array(np.random.rand(1,2))
      self.bout = 1
      self.alpha = 0.01
  
  def hardlim(self, xw):
    if xw > 0 :
      return 1
    else:
      return 0

  def sigmoid(self, z):
    return 1/(1+np.exp(-z))
    
  def deriv_sigmoid(self, z):
    return self.sigmoid(z)*(1-self.sigmoid(z))

  def feed_forward(self, x, w, b):
    return x.dot(w.T) + b
  
  def backpropagation(self):
    print('BP')

#--------------------------------------------------------------
  def train_BP(self, xf, y):

    in1h1 = self.feed_forward(xf, self.wh[0,:], self.bh[0])
    out1h1 = self.sigmoid(in1h1) 

    in2h1 = self.feed_forward(xf, self.wh[1,:], self.bh[1])
    out2h1 = self.sigmoid(in2h1)

    outh = np.array([out1h1, out2h1]).T
    
    inout = self.feed_forward(outh[0,:], self.wout[0,:], self.bout)
    pred = self.sigmoid(inout)
    error = 1/2*((pred - y))**2 
    

    # weight update
    self.wout[0,0] -= self.alpha * ((pred - y) * (self.deriv_sigmoid(inout)) * out1h1)   #w5
    self.wout[0,1] -= self.alpha * ((pred - y) * (self.deriv_sigmoid(inout)) * out2h1)   #w6
    self.wh[0,0] -= self.alpha * ((pred - y) * (self.deriv_sigmoid(inout)) * self.wout[0,0] * (self.deriv_sigmoid(in1h1)) * xf[0])  #w1
    self.wh[0,1] -= self.alpha * ((pred - y) * (self.deriv_sigmoid(inout)) * self.wout[0,0] * (self.deriv_sigmoid(in1h1)) * xf[1])  #w2
    self.wh[1,0] -= self.alpha * ((pred - y) * (self.deriv_sigmoid(inout)) * self.wout[0,1] * (self.deriv_sigmoid(in2h1)) * xf[0])  #w3
    self.wh[1,1] -= self.alpha * ((pred - y) * (self.deriv_sigmoid(inout)) * self.wout[0,1] * (self.deriv_sigmoid(in2h1)) * xf[1])  #w4

#-----------------------------------------------------------
  def predict_BP(self, test_sample):
    in1h1 = self.feed_forward(test_sample, self.wh[0,:],self.bh[0])
    out1h1 = self.sigmoid(in1h1)

    in2h1 = self.feed_forward(test_sample, self.wh[1,:], self.bh[1])
    out2h1 = self.sigmoid(in2h1)

    outh = np.array([out1h1, out2h1]).T
    inout = self.feed_forward(outh[0,:], self.wout[0,:], self.bout)
    out  = self.sigmoid(inout)

    return out

#======================== HL ================================

  def train_HL(self, xf, y):
    in1h1 = self.feed_forward(xf, self.wh[0,:], self.bh[0])
    out1h1 = self.hardlim(in1h1) 

    in2h1 = self.feed_forward(xf, self.wh[1,:], self.bh[1])
    out2h1 = self.hardlim(in2h1)

    inout = self.feed_forward(np.array([out1h1, out2h1]), self.wout, self.bout)
    pred = self.hardlim(inout)

    error = pred - y 
    self.wout += error * xf
    self.wh[0,:] += error * xf
    self.wh[1,:] += error * xf
    self.bh += error
#-------------------------------------------
    
  def predict_HL(self, data_sample):
    in1h1 = self.feed_forward(data_sample, self.wh[0,:], self.bh[0])
    out1h1 = self.hardlim(in1h1) 

    in2h1 = self.feed_forward(data_sample, self.wh[1,:], self.bh[1])
    out2h1 = self.hardlim(in2h1)

    inout = self.feed_forward(np.array([out1h1, out2h1]), self.wout, self.bout)
    out = self.hardlim(inout) 

    return out

NN = MyModel()

for j in range(200):
  for i in range(len(xtrain)):
    NN.train_BP(xtrain[i,:],ytrain[i])

predictions = np.zeros((80,1))
for i in range(80):
  pred = NN.predict_BP(xtest[i,:])
  if pred < 0.5:
    predictions[i,0]=0
  else:
    predictions[i,0]=1

tn, fp, fn, tp = confusion_matrix(ytest, predictions).ravel()

print(tn, fp, fn, tp)
print((tn+tp)/80)

np.concatenate((ytest,predictions),axis=1)