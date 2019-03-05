from random import randint
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

class AnnAgent:
    def __init__(self, game, initial_games = 100, test_games = 100, goal_steps = 100, lr = 1e-2, filename = 'ann_agent.tflearn'):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.filename = filename
        self.tag = "Ann"
        self.game = game
        self.nn_model = self.init_model()

    def getTag(self):
        return self.tag

    def generate_observation(self, board):
        #Flatten board array
        flattened = np.array(board).reshape(-1, 42, 1)
        return flattened

    def init_model(self):
        nn_model = self.model()
        #nn_model.load(self.filename)
        return nn_model

    def model(self):
        network = input_data(shape=[None, 43, 1], name='input')
        network = fully_connected(network, 250, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam',learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(network, tensorboard_dir='log')
        return model 
    
    def makeMove(self, board):
        prev_observation = self.generate_observation(board)
