from random import randint
import random
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

#a further building on the Q agent implementation
#This changes the structure of the ANN once again, 42 inputs and 7 outputs
#This should result in greater accuracy than the Q agent, howver with more nodes comes more complicated 
#training and greater time to learn
# from my testing of this agent over 1000 games it was by far the slowest to learn out of all my approaches
# i dint manage to train this one to the same performance as the other implementations 

class DeepQAgent:
    def __init__(self, game, training, lr=2e-2, filename="agents/models/Q_Learning/Deep_Q_Agent.tflearn"):
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
        self.hidden_nodes = 27
        if training == False:
            self.description = "Trained Deep Q Agent"
        else:
            self.description = "Training Deep Q Agent"
        self.nn_model = self.init_model()
        self.action_log = []
        self.discount = 0.8
        self.gamma = 0.3
        self.board_states_log = []
        self.QValues_log = []
        self.next_max_log = []
        self.nn_input = []
        self.nn_output = []
        self.training_data = []
        self.training_output = []
        self.training_input = []

    def getTag(self):
        return self.tag

    def getDescription(self):
        return self.description

    def generate_observation(self, board):
        #Flatten board array
        flattened = np.array(board).reshape(-1,42,1)
        return flattened

    def add_action_to_observation(self, observation, action):
        return np.append([action], observation)

    def init_model(self):
        nn_model = self.model()
        if self.training == False:
            nn_model.load(self.filename)
        return nn_model

    def reverse_list(self, list_):
        reverse_list = []
        for i in reversed(list_):
            reverse_list.append(i)
        return reverse_list

    def calc_Q(self, reward, steps, prev_q):

        #Q(s, a) = reward * discount ** (playsLength - playIndex - 1)  + gamma * maxQ(previousQ)
        new_Q = (reward * self.discount ** steps) + self.gamma * prev_q
        return new_Q

    
    def model(self):
        network = input_data(shape=[None, 42, 1], name='input')
        network = fully_connected(
            network, self.hidden_nodes, activation='relu')
        network = fully_connected(network, 7, activation='linear')
        network = regression(network, optimizer='SGD',
                             learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(network, tensorboard_dir='log')
        return model

    def get_prob(self, inputs):

        qvalues = self.nn_model.predict(inputs)

        probs = self.softmax(qvalues[0])

        return qvalues[0], probs

    def makeMove(self,board,piece):

        if piece == 1:
            otherPiece = 2
        else:
            otherPiece = 1

        self.board_states_log.insert(0,board)
        

        nn_input = self.generate_observation(board)
        qvalues, probs = self.get_prob(nn_input)

        for index, p in enumerate(qvalues):
             if self.game.is_valid_location(board, index) == False:
                    probs[index] = -1

        randnumber = np.random.rand(1)
        
        if(randnumber < self.random_move_prob and self.training == True):
            action = random.randint(0, 6)

            while self.game.is_valid_location(board, action) == False:
                action = random.randint(0, 6)
        else:
            action = np.argmax(np.array(probs))

        if len(self.action_log) > 0:
            self.next_max_log.insert(0,qvalues[action])

        self.action_log.insert(0,action)
        self.QValues_log.insert(0,qvalues)

        if self.training == True:
            boardCopy = board.copy()
            row = self.game.get_next_open_row(boardCopy, action)
            self.game.drop_piece(boardCopy, row, action, piece)

            boardwins = self.game.can_win(board, otherPiece)
            otherboardwins = self.game.can_win(boardCopy, otherPiece)
            ##If there was an oportunity to block the other player
            #Add to the start of the list, more recent actions are first in the lsit, makes it easier
            #to distribute award back through previous moves
            #Instead of having to reverse the list later if i used .append


            if 1 in otherboardwins:
                self.update_values(-75)

            ##If a winning move was blocked
            elif boardwins != otherboardwins:
                self.update_values(75)

            else:
                print("OOps")

        return action

    def softmax(self,x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def calculate_targets(self, reward):

        game_length = len(self.action_log)
        targets= []
        self.QValues_log[0][self.action_log[0]] = reward

        for i in range(game_length):
            if i > 0:
                target = self.QValues_log[i]
                self.QValues_log[i][self.action_log[i]] += (reward *self.discount **i) + self.gamma *self.QValues_log[i - 1][self.action_log[i - 1]]
                targets.append(target)
        
        return self.QValues_log

    def update_values(self, reward):
        
        
        self.next_max_log.insert(0,reward)

        if self.training:
            self.random_move_prob *= self.random_move_decrease
            self.nn_output = self.calculate_targets(reward)
        
            self.nn_input = np.array([x for x in self.board_states_log]).reshape(-1,42,1)

            #self.training_input.append(nn_input)
        #self.train(nn_input, targets)

    def train(self):
       
        self.training_input.extend(self.nn_input)
        self.training_output.extend(self.nn_output)
        #self.
        X = self.training_input
        y = self.training_output
        self.nn_model.fit(X, y, n_epoch=20, shuffle=True, run_id=self.filename)
        self.nn_model.save(self.filename)

        self.board_states_log = []
        self.action_log = []
        self.next_max_log = []
        self.QValues_log = []
        self.nn_output = []
        self.nn_input = []

