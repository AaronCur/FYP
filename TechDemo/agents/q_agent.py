from random import randint
import random
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

class QAgent:
    def __init__(self, game, training, lr=2e-2, filename="agents/models/Q_Learning/Deep_q_ann.tflearn"):
        self.lr = lr
        self.filename = filename
        self.tag = "Q"
        self.game = game

        self.training_data = []
        self.board_states = []
        self.wins = 0
        self.random_move_decrease = 0.996
        self.random_move_prob = 1
        self.training = training
        self.hidden_nodes = 22
        self.description = "Deep Q ANN"
        self.nn_model = self.init_model()

        self.discount = 0.8
        self.gamma = 0.3

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

    def reverse_list(self,list_):
        reverse_list = []
        for i in reversed(list_):
            reverse_list.append(i)
        return reverse_list

    def calc_Q(self, reward, steps, prev_q):

        #Q(s, a) = reward * discount ** (playsLength - playIndex - 1)  + gamma * maxQ(previousQ)
        new_Q = (reward * self.discount ** steps) + self.gamma * prev_q
        return new_Q

    def update_values(self, reward):
        #board_states = self.reverse_list(self.board_states)
        if self.training == True:
            temp = self.board_states[0][1]
            self.board_states[0][1] = self.board_states[0][1] + reward
            for i, state in enumerate(self.board_states):
                if i > 0:
                    steps_from_win = i
                    prev_Q = self.board_states[i-1][1]
                    new_Q = round(self.calc_Q(reward, steps_from_win, prev_Q),3)

                    #Update Q value if the current Q is less then the new Q
                    state[1] = state[1] + new_Q

            ##Decrease greedy value
            
            #self.random_move_prob *= self.random_move_decrease
            #self.nn_model = self.train_model(self.training_data, self.nn_model)
            self.random_move_prob *= self.random_move_decrease
        else:
            pass

    def train(self):
        for state in self.board_states:
            if state[1] == -1000:
                print("oops")
            self.training_data.append(state)
        self.board_states = []
        X = np.array([i[0] for i in self.training_data]).reshape(-1, 43, 1)
        y = np.array([i[1] for i in self.training_data]).reshape(-1, 1)
        self.nn_model.fit(X, y, n_epoch=20, shuffle=True, run_id=self.filename)
        self.nn_model.save(self.filename)
        self.random_move_prob *= self.random_move_decrease

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
        if(randnumber < self.random_move_prob and self.training == True):
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
            #Add to the start of the list, more recent actions are first in the lsit, makes it easier 
            #to distribute award back through previous moves 
            #Instead of having to reverse the list later if i used .append
    
            self.board_states.insert(0,
                [self.add_action_to_observation(prev_observation, action),0])

            if 1 in otherboardwins:
                self.update_values(-75)

            ##If a winning move was blocked
            elif boardwins != otherboardwins:
                self.update_values(75)

            else:
                print("OOps")

        return action
