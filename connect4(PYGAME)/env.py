import numpy as np
from board import Connect4Board
from random import choice
import pygame
import math
import random

class Connect4Env:
    def __init__(self):
        self.SQUARESIZE = 100
        self. RADIUS = int(self.SQUARESIZE/2 - 5)
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7

        self.game = Connect4Board(self.SQUARESIZE, self.RADIUS, self.COLUMN_COUNT, self.ROW_COUNT)
        pygame.init()

        self.WIDTH = self.game.COLUMN_COUNT * self.SQUARESIZE
        self.HEIGHT = (self.game.ROW_COUNT+1) * self.SQUARESIZE

        size = (self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode(size)
        
        self.board = self.game.create_board()

        self.game_over = False
        self.turn = 0
               
        self.PLAYER1 = 0
        self.PLAYER2 = 1

        self.EMPTY = 0
        self.PLAYER1_PIECE = 1
        self.PLAYER2_PIECE = 2

        self.BG = (0,0,0)
        self.BOARD = (0,0,255)
        self.RED = (255,0,0)
        self.YELLOW = (255,255,0)


    ##def reset(self):
        ##self.board = TicTacToeBoard()

   ## def get_reward(self):
      ##  return self.board.result()

   ## def make_move(self, move):
      ##  self.board.push(move)

  ##  def make_random_move(self):
       ## legal_moves = self.get_legal_moves()
      ##  move = choice(legal_moves)
       ## self.make_move(move)

  ##  def get_legal_moves(self):
        ##return list(self.board.legal_moves)
    def print_board(self,board):
            print(np.flip(board, 0))
    def drop_piece(self,board, row, col, piece):
        self.game.drop_piece(board, row, col, piece)

    def is_valid_location(self,board, col):
        self.game.is_valid_location(board,col)

    def get_next_open_row(self,board, col):
        self.game.get_next_open_row(board,col)

    def winning_move(self,board, piece):
        self.game.winning_move(board, piece)

    def draw_board(self,board, screen, pygame):
            for c in range(self.COLUMN_COUNT):
                for r in range(self.ROW_COUNT):
                    pygame.draw.rect(screen, self.BOARD, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                    pygame.draw.circle(screen, self.BG, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)

            for c in range(self.COLUMN_COUNT):
                for r in range(self.ROW_COUNT):
                    if board[r][c] == 1:
                        pygame.draw.circle(screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.HEIGHT-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                    elif board[r][c] == 2:
                        pygame.draw.circle(screen, self.YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.HEIGHT-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
            pygame.display.update()

    def play(self,player1, player2):
    
            self.draw_board(self.board, self.screen, pygame)
            pygame.display.update()

            myfont = pygame.font.SysFont("monospace", 75)
            

            while not self.game_over:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.BG, (0,0, self.WIDTH, self.SQUARESIZE))
                    posx = event.pos[0]
                    if self.turn == self.PLAYER1:
                        pygame.draw.circle(self.screen, self.RED, (posx, int(self.SQUARESIZE/2)), self.RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.BG, (0,0, self.WIDTH, self.SQUARESIZE))
                    #print(event.pos)
                    # Ask for Player 1 Input
                    if self.turn == self.PLAYER1:
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if self.game.is_valid_location(self.board, col):
                            row = self.game.get_next_open_row(self.board, col)
                            self.game.drop_piece(self.board, row, col, self.PLAYER1_PIECE)

                            if self.game.winning_move(self.board, self.PLAYER1_PIECE):
                                label = myfont.render("Player 1 wins!!", 1, self.RED)
                                screen.blit(label, (40,10))
                                self.game_over = True

                            self.turn += 1
                            self.turn = self.turn % 2

                            self.print_board(self.board)
                            self.draw_board(self.board, self.screen, pygame)

                    # # Ask for Player 2 Input
                    if self.turn == self.PLAYER2 and not self.game_over:

                        col = random.randint(0, self.COLUMN_COUNT-1)
                        #col = pick_best_move(board, AI_PIECE)
                        #col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

                        if self.game.is_valid_location(self.board, col):
                            pygame.time.wait(500)
                            row = self.game.get_next_open_row(self.board, col)
                            self.game.drop_piece(self.board, row, col, self.PLAYER2_PIECE)

                            if self.game.winning_move(self.board, self.PLAYER2_PIECE):
                                label = myfont.render("Player 2 wins!!", 1, self.YELLOW)
                                screen.blit(label, (40,10))
                                self.game_over = True

                            self.print_board(self.board)
                            self.draw_board(self.board, self.screen, pygame)

                            self.turn += 1
                            self.turn = self.turn % 2
                    if self.game_over:
                        pygame.time.wait(3000)
