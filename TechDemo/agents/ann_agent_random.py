from random import randint
import random
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter
#EGREEDY


class AnnAgentRandom:
    def __init__(self, game, training, initial_games=100, test_games=100, goal_steps=100, lr=2e-2, filename='agents/models/egreedy/22/ann_agent5_minimax_random.tflearn'):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.filename = filename
        self.tag = "Ann"
        self.game = game

        self.training_data = []
        self.board_states = []
        self.wins = 0
        self.random_move_decrease = 0.995
        self.random_move_prob = 1
        self.training = training
        self.hidden_nodes = 22
        self.description = "E-GreedyRnd"

        self.nn_model = self.init_model()

    def getTag(self):
        return self.tag

    def generate_observation(self, board):
        #Flatten board array
        flattened = np.array(board).reshape(-1, 42, 1)
        return flattened

    def add_action_to_observation(self, observation, action):
        return np.append([action], observation)

    def init_model(self):
        nn_model = self.model()
        if self.training == False:
            nn_model.load(self.filename)
        return nn_model

    def train(self, reward):

        if self.training == True:

            for val in self.board_states:
                val.append(reward)
                self.training_data.append(
                    val)

            self.board_states = []
        else:
            pass

    def train_model(self):
        X = np.array([i[0] for i in self.training_data]).reshape(-1, 43, 1)
        y = np.array([i[1] for i in self.training_data]).reshape(-1, 1)
        self.nn_model.fit(X, y, n_epoch=20, shuffle=True, run_id=self.filename)
        self.nn_model.save(self.filename)
     
    def model(self):
        network = input_data(shape=[None, 43, 1], name='input')
        network = fully_connected(
            network, self.hidden_nodes, activation='relu')
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

        randnumber = np.random.rand(1)
        ##greedy element
        if(self.training == True):
            action = random.randint(0, 6)

            while self.game.is_valid_location(board, action) == False:
                action = random.randint(0, 6)
        else:

            for action in range(0, 7):
                predictions.append(self.nn_model.predict(
                    self.add_action_to_observation(prev_observation, action).reshape(-1, 43, 1)))
                if self.game.is_valid_location(board, action) == False:
                    predictions[action] = -100000

            action = np.argmax(np.array(predictions))

        #if move isnt valid redo move
        #temp = self.game.is_valid_location(board, action)

       # if(self.game.is_valid_location(board, action)):
        if self.training == True:
            boardCopy = board.copy()
            row = self.game.get_next_open_row(boardCopy, action)
            self.game.drop_piece(boardCopy, row, action, piece)
            score = self.game.score_position(boardCopy, piece)

            boardwins = self.game.can_win(board, otherPiece)
            otherboardwins = self.game.can_win(boardCopy, otherPiece)
            ##If there was an oportunity to block the other player
            if 1 in otherboardwins:
                self.training_data.append(
                    [self.add_action_to_observation(prev_observation, action), -175])

            ##If a winning move was blocked
            elif boardwins != otherboardwins:
                self.training_data.append(
                    [self.add_action_to_observation(prev_observation, action), +175])

            else:
                self.board_states.append(
                    [self.add_action_to_observation(prev_observation, action)])
        #self.training_data.append(
        #   [self.add_action_to_observation(prev_observation, action), 1])
        return action
       # else:
        # boardCopy = board.copy()
        # self.board_states.append([self.add_action_to_observation(prev_observation, action)])
        #self.training_data.append([self.add_action_to_observation(prev_observation, action), -10000])
        #self.nn_model = self.train_model(self.training_data, self.nn_model)
        #self.makeMove(board, piece)
        # action = random.randint(0, 6)

        # while self.game.is_valid_location(board, action) == False:
        #  action = random.randint(0, 6)
        # self.training_data.append(
        #[self.add_action_to_observation(prev_observation, action), -10000])
        #self.nn_model = self.train_model(self.training_data, self.nn_model)
        # return action
