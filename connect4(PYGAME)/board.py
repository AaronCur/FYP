import numpy as np
import pygame
import sys
import math
import random

class RandomAgent():
 
    def makeMove(self, cc):
        return random.randint(0, cc-1)

class HumanAgent():
    def __init__(self):
            self.playerNum = 1
            
    def makeMove(self, pygame, screen):
         if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, game.BG, (0,0, width, SQUARESIZE))
                    #print(event.pos)
                    # Ask for Player 1 Input
                 
                    posx = event.pos[0]
                    return int(math.floor(posx/SQUARESIZE))
                    
class Connect4Board:
        def __init__(self, squaresize, radius, col, row):
            self.ROW_COUNT = row
            self.COLUMN_COUNT = col
            self.SQUARESIZE = squaresize

            

        def create_board(self):
            board = np.zeros((self.ROW_COUNT,self.COLUMN_COUNT))
            return board

        def generate_observations(self):
            return board

        def drop_piece(self,board, row, col, piece):
            board[row][col] = piece

        def is_valid_location(self, board, col):
            temp = board[self.ROW_COUNT-1][col]
            return board[self.ROW_COUNT-1][col] == 0

        def get_next_open_row(self,board, col):
            for r in range(self.ROW_COUNT):
                if board[r][col] == 0:
                    return r

        def winning_move(self,board, piece):
            # Check horizontal locations for win
            for c in range(self.COLUMN_COUNT-3):
                for r in range(self.ROW_COUNT):
                    if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                        return True

            # Check vertical locations for win
            for c in range(self.COLUMN_COUNT):
                for r in range(self.ROW_COUNT-3):
                    if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                        return True

            # Check positively sloped diaganols
            for c in range(self.COLUMN_COUNT-3):
                for r in range(self.ROW_COUNT-3):
                    if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                        return True

            # Check negatively sloped diaganols
            for c in range(self.COLUMN_COUNT-3):
                for r in range(3, self.ROW_COUNT):
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        return True

        def get_valid_locations(board):
            valid_locations = []
            for col in range(COLUMN_COUNT):
                if is_valid_location(board, col):
                    valid_locations.append(col)
            return valid_locations

        def evaluate_window(window, piece):
            score = 0
            opp_piece = PLAYER_PIECE
            if piece == PLAYER_PIECE:
                opp_piece = AI_PIECE

            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 5
            elif window.count(piece) == 2 and window.count(EMPTY) == 2:
                score += 2

            if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                score -= 4

            return score

        def score_position(board, piece):
            score = 0

            ## Score center column
            center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
            center_count = center_array.count(piece)
            score += center_count * 3

            ## Score Horizontal
            for r in range(ROW_COUNT):
                row_array = [int(i) for i in list(board[r,:])]
                for c in range(COLUMN_COUNT-3):
                    window = row_array[c:c+WINDOW_LENGTH]
                    score += evaluate_window(window, piece)

            ## Score Vertical
            for c in range(COLUMN_COUNT):
                col_array = [int(i) for i in list(board[:,c])]
                for r in range(ROW_COUNT-3):
                    window = col_array[r:r+WINDOW_LENGTH]
                    score += evaluate_window(window, piece)

            ## Score posiive sloped diagonal
            for r in range(ROW_COUNT-3):
                for c in range(COLUMN_COUNT-3):
                    window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                    score += evaluate_window(window, piece)

            for r in range(ROW_COUNT-3):
                for c in range(COLUMN_COUNT-3):
                    window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                    score += evaluate_window(window, piece)

            return score

        def is_terminal_node(board):
            return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

       

class HumanAgent():
    def __init__(self):

        AgentBase.__init__(self, name, model, env)

        self.verbose = verbose

        self.opt = tf.train.AdamOptimizer()

        self.grads = tf.gradients(self.model.value, self.model.trainable_variables)

        self.grads_s = [tf.placeholder(tf.float32, shape=tvar.get_shape()) for tvar in self.model.trainable_variables]

        self.apply_grads = self.opt.apply_gradients(zip(self.grads_s, self.model.trainable_variables),
                                                    name='apply_grads')

    def train(self, epsilon):

        lamda = 0.7

        self.env.reset()

        traces = [np.zeros(tvar.shape)
                  for tvar in self.model.trainable_variables]

        feature_vector = self.env.make_feature_vector(self.env.board)

        previous_value, previous_grads = self.sess.run([self.model.value, self.grads],
                                                       feed_dict={self.model.feature_vector_: feature_vector})
        reward = self.env.get_reward()

        while reward is None:

            if np.random.random() < epsilon:
                self.env.make_random_move()
            else:
                move = self.get_move()
                self.env.make_move(move)

            reward = self.env.get_reward()

            feature_vector = self.env.make_feature_vector(self.env.board)

            if reward is None:
                value, grads = self.sess.run([self.model.value, self.grads],
                                             feed_dict={self.model.feature_vector_: feature_vector})
            else:
                value = reward
                grads = self.sess.run(self.grads,
                                      feed_dict={self.model.feature_vector_: feature_vector})

            delta = value - previous_value
            for previous_grad, trace in zip(previous_grads, traces):
                trace *= lamda
                trace += previous_grad

            self.sess.run(self.apply_grads,
                          feed_dict={grad_: -delta * trace
                                     for grad_, trace in zip(self.grads_s, traces)})

            previous_grads = grads
            previous_value = value

        return self.env.get_reward()