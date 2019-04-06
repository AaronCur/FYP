from random import randint
import random
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter


class DeepQAgent:
    def __init__(self, game, training, lr=2e-2, filename="agents/models/Q_Learning/Q_temporal_difference.tflearn"):
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
        self.description = "Q Temporal Difference"
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

    def updateQ(self, reward):
        #board_states = self.reverse_list(self.board_states)
        if self.training == True:
            temp = self.board_states[0][1]
            if self.board_states[0][1] < reward:
                self.board_states[0][1] = reward
            for i, state in enumerate(self.board_states):
                if i > 0:
                    steps_from_win = i
                    prev_Q = self.board_states[i-1][1]
                    new_Q = round(self.calc_Q(
                        reward, steps_from_win, prev_Q), 3)

                    #Update Q value if the current Q is less then the new Q
                    if state[1] < new_Q:
                        state[1] = new_Q

            ##Decrease greedy value
            if self.random_move_prob > 1.5:
                self.random_move_prob *= self.random_move_decrease
            #self.nn_model = self.train_model(self.training_data, self.nn_model)
        else:
            pass

    def train_model(self):
        for state in self.board_states:
            if state[1] == -1000:
                print("oops")
            self.training_data.append(state)
        self.board_states = []
        X = np.array([i[0] for i in self.training_data]).reshape(-1, 43, 1)
        y = np.array([i[1] for i in self.training_data]).reshape(-1, 1)
        self.nn_model.fit(X, y, n_epoch=20, shuffle=True, run_id=self.filename)
        self.nn_model.save(self.filename)

    

    def model(self):
        network = input_data(shape=[None, 42, 1], name='input')
        network = fully_connected(
            network, self.hidden_nodes, activation='relu')
        network = fully_connected(network, 7, activation='linear')
        network = regression(network, optimizer='adam',
                             learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(network, tensorboard_dir='log')
        return model

    def make_Move(self, board, piece):
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
                                     [self.add_action_to_observation(prev_observation, action), -1000])

            if 1 in otherboardwins:
                self.updateQ(-75)

            ##If a winning move was blocked
            elif boardwins != otherboardwins:
                self.updateQ(75)

            else:
                print("OOps")

        return action

    def get_prob(self, inputs):

        qvalues = self.nn_model.predict(inputs)

        probs = self.softmax(qvalues[0])

        return qvalues[0], probs

    def makeMove(self,board,piece):

        if piece == 1:
            otherPiece = 2
        else:
            otherPiece = 1

        self.board_states_log.append(board)
        

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
            self.next_max_log.append(qvalues[action])

        self.action_log.append(action)
        self.QValues_log.append(qvalues)

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
                self.update_values(-100)

            ##If a winning move was blocked
            elif boardwins != otherboardwins:
                self.update_values(175)

            else:
                print("OOps")

        return action

    def softmax(self,x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def calculate_targets(self, reward):

        game_length = len(self.action_log)
        targets= []

        for i in range(game_length):
            target = self.QValues_log[i]
            steps = game_length - i
            target[self.action_log[i]] = (reward *self.discount **steps) + self.gamma *self.next_max_log[i]
            targets.append(target)
        
        return targets

    def update_values(self, reward):
        if self.random_move_prob > 1.5:
                self.random_move_prob *= self.random_move_decrease
        self.next_max_log.append(reward)

        if self.training:
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

