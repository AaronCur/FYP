from random import randint
import random
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

#This implementation explored the concept of ONLY giving rewards to the action that caused 
#them, instead of giving this reward to al moves that lead to it
# the idea of this was to stop contradictory data
# from my testing it was extremly slow to learn duee to the decreased amount of training data
# there is a possibility that this implementation could have worked but it would have required 10x longer 
# to train and a PC thats much quicker than the one i have 

class AnnAgent3:
    def __init__(self, game, lr=1e-2, filename='ann_agent3_minimax.tflearn'):
        self.lr = lr
        self.filename = filename
        self.tag = "Ann"
        self.game = game
        self.nn_model = self.init_model()
        self.training_data = []
        self.board_states = []
        self.wins = 0

    def getTag(self):
        return self.tag

    def getDescription(self):
        return self.tag

    def generate_observation(self, board):
        #Flatten board array
        flattened = np.array(board).reshape(-1, 42, 1)
        return flattened

    def add_action_to_observation(self, observation, action):
        return np.append([action], observation)

    def init_model(self):
        nn_model = self.model()
        #nn_model.load(self.filename)
        return nn_model

    def train(self, reward):
        #Latest board state 
        self.board_states[-1].append(reward)
           
        self.training_data.append(self.board_states[-1])

        self.board_states = []
        self.nn_model = self.train_model(self.training_data, self.nn_model)

    def train_model(self, training_data, model):
        X = np.array([i[0] for i in training_data]).reshape(-1, 43, 1)
        y = np.array([i[1] for i in training_data]).reshape(-1, 1)
        model.fit(X, y, n_epoch=20, shuffle=True, run_id=self.filename)
        model.save(self.filename)
        return model

    def model(self):
        network = input_data(shape=[None, 43, 1], name='input')
        network = fully_connected(network, 250, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam',
                             learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(network, tensorboard_dir='log')
        return model

    def makeMove(self, board, piece):
        if piece == 1:
            otherPiece = 2
        else:
            otherPiece = 1

        prev_observation = self.generate_observation(board)
        predictions = []

        for action in range(0, 7):
            predictions.append(self.nn_model.predict(
                self.add_action_to_observation(prev_observation, action).reshape(-1, 43, 1)))
            if self.game.is_valid_location(board, action) == False:
               predictions[action] = -100000

        action = np.argmax(np.array(predictions))

        boardCopy = board.copy()
        row = self.game.get_next_open_row(boardCopy, action)
        self.game.drop_piece(boardCopy, row, action, piece)
        score = self.game.score_position(boardCopy, piece)

      
        ##If a winning move was blocked
        if self.game.can_win(board, otherPiece) == True and self.game.can_win(boardCopy, otherPiece) == False:
            self.training_data.append(
                [self.add_action_to_observation(prev_observation, action), +75])

        else:
            self.board_states.append(
                [self.add_action_to_observation(prev_observation, action)])

        return action