# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xTr-NQ3LjDMmKfU8lANxen5BICZ8XFtd
"""

from __future__ import print_function, division
from builtins import range

import numpy as np
import matplotlib.pyplot as plt
import gym
from gym import wrappers

def select_action(obs , randstate_param):
  if obs.dot(randstate_param) > 0:
    return 1
  else:
    return 0

def play_episode(env , randstate):
  observation = env.reset()
  done = False
  iter = 0
  while not done and iter <100 :
    action = select_action(observation , randstate)
    observation, reward, done, info = env.step(action)
    iter+=1
  return iter

env =gym.make('CartPole-v0')
total_reward=0
for i in range(100):
  random_state = np.random.randn(4)
  run = play_episode(env,random_state)
  total_run=total_run+run
print(total_reward)