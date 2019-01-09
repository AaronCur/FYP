import gym
import random
import numpy as np
import tflearn
from tflearn.layer.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter

##LearningRate
LR = le-3
env = gym.make('CartPolve-v0')
env.reset()

goal_Steps = 500
score_requirement = 50
initial_games = 10000

def some_random_games_first():
    for episode in range(5):
        env.reset()
        for t in range(goal_Steps):
            env.render()
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)

            if done:
                break
                
some_random_games_first()

#env = env.unwrapped

#for i_episode in range(100):
#    s = env.reset()
#    while True:
#        env.render()
#        a = RL.choose_actions(s)
#        s_, r, done, info = env.step(a)

        #Run your updates here

#        if done:
#            break
#        s = s_
