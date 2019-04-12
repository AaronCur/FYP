from random import randint
import random
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

#This implementation is the basic ANN implementation of whihc i base the rest of 
#my results off of,
#When it loses all actions receive - 100 win it wins all actions receive + 100
#It has 250 in the hidden layer and has no training assistance

#Takes luck to find winning moves and repetas the same pattern of moves once it finds them
#Doesnt try to stop othre player for winning 


class AnnAgentBasic:
    def __init__(self, game, training, lr=1e-2, filename='agents/models/egreedy/250/ann_agent_basic_minimax_250.tflearn'):
        self.lr = lr
        self.filename = filename
        self.tag = "Ann"
        self.game = game
        self.training_data = []
        self.board_states = []
        self.wins = 0
        self.random_move_decrease = 0.996
        self.random_move_prob = 1
        self.hidden_nodes = 250
        self.training = training
        self.description = "ANN Basic"
        self.nn_model = self.init_model()

    def getTag(self):
        return self.tag
    
    def getDescription(self):
        return self.description

    def generate_observation(self, board):
        #Flatten board 2d array into a 1d array
        flattened = np.array(board).reshape(-1, 42, 1)
        return flattened

    def add_action_to_observation(self, observation, action):
        return np.append([action], observation)
    #Only load in ANN model if not in training mode
    def init_model(self):
        nn_model = self.model()
        if self.training == False:
            nn_model.load(self.filename)
        return nn_model

    #When the game is over, loop through all the board states that were made as a result of the
    #Ann making moves and append the appropriate reward to each set of state and actions.
    #then add the resulting list with board states, actions and rewards to training data for training
    #Board states only record board states for that game, once training begins the board state array is cleared 
    def train(self, reward):

        if self.training == True:
            for val in self.board_states:
                val.append(reward)
                self.training_data.append(
                    val)

            self.board_states = []
            self.nn_model = self.train_model(self.training_data, self.nn_model)
        else:
            pass
    #Loops through training data splitting it into the input which is board state + action
    #and outputs which is the reward
    #The resulting inputs and outputs are fed into model.fit() to train the model
    def train_model(self, training_data, model):
        X = np.array([i[0] for i in training_data]).reshape(-1, 43, 1)
        y = np.array([i[1] for i in training_data]).reshape(-1, 1)
        model.fit(X, y, n_epoch=20, shuffle=True, run_id=self.filename)
        model.save(self.filename)
        return model

    #Initialization of the ANN model, consisting of an input layer of 43 nodes
    #1 hidden layer with 22 nodes
    #1 output layer consisting of 1 node
    def model(self):
        network = input_data(shape=[None, 43, 1], name='input')
        network = fully_connected(
            network, self.hidden_nodes, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam',
                             learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(network, tensorboard_dir='log')
        return model

    #Function which returns the move the agent wants to play
    def makeMove(self, board, piece):
        prev_observation = self.generate_observation(board)
        predictions = []

        #Generate a list of predictions from the ANN model by inputting the current board state
        #and inputting each action 0-6
        for action in range(0, 7):
            predictions.append(self.nn_model.predict(
                self.add_action_to_observation(prev_observation, action).reshape(-1, 43, 1)))
            if self.game.is_valid_location(board, action) == False:
                predictions[action] = -100000

        action = np.argmax(np.array(predictions))

        if self.training == True:

            self.board_states.append([self.add_action_to_observation(prev_observation, action)])
        
        return action
     
