from random import randint
import random
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

#Builiding on the 22 node e-greedy implementation by smartly distributing awards
#Moves on the board early in the game should have a lesser impact on the end result than
# the later moves. This is why we use Q-Learning to calculate the rewards, it follows the wquation of 
# #Q(s, a) = reward * discount ** (playsLength - playIndex - 1)  + gamma * maxQ(previousQ)
#q(s,a) being the reward for teh current state and action, the reward is discounted back to previous
#moves that lead to the victory

#this lead to smarter playing, lots of variation and more likely to ein in a lot more ways than the previous
#implementations
#However it takes much longer to train to achieve this performance, over 1000 games
#it only achieved the same performance as the 250 node egreedy implementation
#howevr if ran over 10,000 games it would hae much greater performance than any other approach 
#Unfortunalty my hardware was not capabale of achieving this test 

class QAgent:
    def __init__(self, game, training, lr=2e-2, filename="agents/models/Q_Learning/Q_temporal_difference_3.tflearn"):
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
    
    def getDescription(self):
        return self.description

    #Creates an array containing both the current board state and action 
    def generate_observation(self, board):
        #Flatten board array
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

    #Reverses list so recent moves appear first 
    def reverse_list(self,list_):
        reverse_list = []
        for i in reversed(list_):
            reverse_list.append(i)
        return reverse_list

    #Calculates the discounted Q value of an action depending on the reward of the previous move
    #and how many steps that action was from the game winning action
    #Gamma is added to take into account the importance of the previous value in the equation 
    def calc_Q(self, reward, steps, prev_q):
        #Q Value equation
        #Q(s, a) = reward * discount ** (playsLength - playIndex - 1)  + gamma * maxQ(previousQ)
        new_Q = (reward * self.discount ** steps) + self.gamma * prev_q
        return new_Q

    #Update q values of all the actions that lead to that reward
    #Starting at the action that resulted in that reward 
    def update_values(self, reward):
        #board_states = self.reverse_list(self.board_states)
        if self.training == True:
            #Set action that resulted in the rewards Q value to the reward itself 
            self.board_states[0][1] = self.board_states[0][1] + reward
            for i, state in enumerate(self.board_states):
                if i > 0:
                    steps_from_win = i
                    prev_Q = self.board_states[i-1][1]
                    new_Q = round(self.calc_Q(reward, steps_from_win, prev_Q),3)

                    #Update Q value if the current Q is less then the new Q
                    state[1] = state[1] + new_Q
        else:
            pass
    #Loops through training data splitting it into the input which is board state + action
    #and outputs which is the reward
    #The resulting inputs and outputs are fed into model.fit() to train the model
    def train(self):
        if self.training == True:
            for state in self.board_states:
                self.training_data.append(state)
            self.board_states = []
            X = np.array([i[0] for i in self.training_data]).reshape(-1, 43, 1)
            y = np.array([i[1] for i in self.training_data]).reshape(-1, 1)
            self.nn_model.fit(X, y, n_epoch=20, shuffle=True, run_id=self.filename)
            self.nn_model.save(self.filename)
            self.random_move_prob *= self.random_move_decrease

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
        if piece == 1:
            otherPiece = 2
        else:
            otherPiece = 1

        prev_observation = self.generate_observation(board)
        predictions = []

        #Generates random number between 0 and 1
        randnumber = np.random.rand(1)

        ##greedy element
        #If random number generated is less than the random move probability the agent will make a 
        #completely random move, only happens when training the model
        if(randnumber < self.random_move_prob and self.training == True):
            action = random.randint(0, 6)

            #If the action generated isnt valid, generate again
            while self.game.is_valid_location(board, action) == False:
                action = random.randint(0, 6)
        else:
            #Generate a list of predictions from the ANN model by inputting the current board state
            #and inputting each action 0-6
            for action in range(0, 7):
                predictions.append(self.nn_model.predict(
                    self.add_action_to_observation(prev_observation, action).reshape(-1, 43, 1)))
                if self.game.is_valid_location(board, action) == False:
                    predictions[action] = -100000

            #Take the highest value action from the list of probabilities
            action = np.argmax(np.array(predictions))

        if self.training == True:
            #Create a copy of the board and take the action decided above on it to see what the resulting board state would be 
            #after it takes the action 
            boardCopy = board.copy()
            row = self.game.get_next_open_row(boardCopy, action)
            self.game.drop_piece(boardCopy, row, action, piece)
            score = self.game.score_position(boardCopy, piece)
            
            #Generate win cases before and after taking the action on the board
            boardwins = self.game.can_win(board, otherPiece)
            otherboardwins = self.game.can_win(boardCopy, otherPiece)
           
            #Add to the start of the list, more recent actions are first in the lsit, makes it easier 
            #to distribute award back through previous moves 
            #Instead of having to reverse the list later if i used .append

            self.board_states.insert(0,
                                     [self.add_action_to_observation(prev_observation, action), 0])
            
            ##If there was an oportunity to block the other player
            if 1 in otherboardwins:
                self.update_values(-75)

            ##If a winning move was blocked
            if boardwins != otherboardwins:
                self.update_values(50)

        return action
