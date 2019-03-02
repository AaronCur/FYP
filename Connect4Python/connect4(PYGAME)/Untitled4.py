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
                    
class Connect4Game:
        def __init__(self):
            self.BOARD = (0,0,255)
            self.BG = (0,0,0)
            self.RED = (255,0,0)
            self.YELLOW = (255,255,0)

            self.ROW_COUNT = 6
            self.COLUMN_COUNT = 7
            
            PLAYER = 0
        AI = 1

        EMPTY = 0
        PLAYER_PIECE = 1
        AI_PIECE = 2

        def create_board(self):
            board = np.zeros((self.ROW_COUNT,self.COLUMN_COUNT))
            return board

        def generate_observations(self):
            return board

        def drop_piece(self,board, row, col, piece):
            board[row][col] = piece

        def is_valid_location(self,board, col):
            return board[self.ROW_COUNT-1][col] == 0

        def get_next_open_row(self,board, col):
            for r in range(self.ROW_COUNT):
                if board[r][col] == 0:
                    return r

        def print_board(self,board):
            print(np.flip(board, 0))

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

        def draw_board(self,board):
            for c in range(self.COLUMN_COUNT):
                for r in range(self.ROW_COUNT):
                    pygame.draw.rect(screen, self.BOARD, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                    pygame.draw.circle(screen, self.BG, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

            for c in range(self.COLUMN_COUNT):
                for r in range(self.ROW_COUNT):
                    if board[r][c] == 1:
                        pygame.draw.circle(screen, self.RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                    elif board[r][c] == 2:
                        pygame.draw.circle(screen, self.YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            pygame.display.update()

if __name__ == "__main__":
        randomAgent = RandomAgent()
        human = HumanAgent()
        game = Connect4Game()
        board = Connect4Game().create_board()
        game_over = False
        turn = 0
        pygame.init()

        SQUARESIZE = 100

        width = game.COLUMN_COUNT * SQUARESIZE
        height = (game.ROW_COUNT+1) * SQUARESIZE

        size = (width, height)

        RADIUS = int(SQUARESIZE/2 - 5)

        screen = pygame.display.set_mode(size)
        Connect4Game().draw_board(board)
        pygame.display.update()

        myfont = pygame.font.SysFont("monospace", 75)
        
        turn = 0

        while not game_over:

            for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                        sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BG, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BG, (0,0, width, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40,10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        # # Ask for Player 2 Input
        if turn == 1 and not game_over:

            col = random.randint(0, COLUMN_COUNT-1)
            #col = pick_best_move(board, AI_PIECE)
            #col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if game.is_valid_location(board, col):
                pygame.time.wait(500)
                row = game.get_next_open_row(board, col)
                game.drop_piece(board, row, col, 2)

                if game.winning_move(board, 2):
                    label = myfont.render("Player 2 wins!!", 1, game.YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True

                game.print_board(board)
                game.draw_board(board)

                turn += 1
                turn = turn % 2
        if game_over:
            pygame.time.wait(3000)

board = game.create_board()

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