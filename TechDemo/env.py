import numpy as np
from board import Connect4Board
from random import choice
import pygame
import math
import random
import matplotlib.pyplot as plt

class Connect4Env:
    def __init__(self, squaresize,row,col,game):
        self.SQUARESIZE = squaresize
        self. RADIUS = int(self.SQUARESIZE/2 - 5)
        self.ROW_COUNT = row
        self.COLUMN_COUNT = col

        self.game = game
        pygame.init()

        self.WIDTH = self.game.COLUMN_COUNT * self.SQUARESIZE
        self.HEIGHT = (self.game.ROW_COUNT+1) * self.SQUARESIZE

        self.size = (self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode(self.size)
        
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

        self.win_his =[]
        self.player1_wins = []
        self.player2_wins = []
        self.drawn_games = []
        self.game_number = []

        self.games = 10
        self.battles = 100

        self.gui = False
        self.startTurn = 0

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
    def calc_avg(self, wins):
        return sum(wins) / len(wins) 


    def plot_history(self, player1, player2):
        plt.figure()
        
        plt.xlabel('Games Played')
        plt.ylabel('Winning Rate %')
        drawsAvg = self.calc_avg(self.drawn_games)
        if len(self.drawn_games) != 0:
            plt.plot(self.game_number,self.drawn_games,'b-', label="Draws" + ": " + str(drawsAvg) + "%" )
        player1Avg = self.calc_avg(self.player1_wins)
        player2Avg = self.calc_avg(self.player2_wins)
        
        if player1.getTag() == "Ann":
            plt.plot(self.game_number,self.player2_wins,'r-', label=player2.getTag() + ": " + str(player2Avg) + "%" )
            plt.plot(self.game_number, self.player1_wins, 'g-', label=player1.getTag() + ": " + str(player1Avg) + "%")
            if player1.training == False:
                plt.title('Trained '+ str(player1.description)+' vs ' + str(player2.tag))
            else:
                plt.title('Training '+ str(player1.description)+' vs ' + str(player2.tag))
        else:
            plt.plot(self.game_number,self.player2_wins,'g-', label=player2.getTag() + ": " + str(player2Avg) + "%")
            plt.plot(self.game_number, self.player1_wins, 'r-', label=player1.getTag() + ": " + str(player1Avg) + "%")
            if player1.training == False:
                plt.title('Trained '+ str(player2.description)+' vs ' + str(player1.tag))
            else:
                plt.title('Training '+ str(player2.description)+' vs ' + str(player1.tag))
    
        plt.legend()
  
        plt.show()

    def win_percentage(self,wins, games):
        percentage = 100 * float(wins) / float(games)
        self.win_his.append(percentage)
        return percentage

    def play(self,player1, player2):
        gameNumber = 0
       
        for i in range(self.battles):
            player1wins = 0
            player2wins = 0
            draws = 0
            for i in range(self.games):

                self.startTurn = 0
                self.turn = self.startTurn
                
                gameNumber+=1
                
                self.screen = pygame.display.set_mode(self.size)
                myfont = pygame.font.SysFont("monospace", 75)
                self.game_over = False
            
                self.board = self.game.create_board()
                print("episode "+ str(i))

                numGames = myfont.render(
                    "Game: " + str(gameNumber), 1, self.RED)
                self.screen.blit(numGames, (40, 10))

                self.draw_board(self.board, self.screen, pygame)
                pygame.display.update()

            
                while not self.game_over:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                sys.exit()
                    if self.turn == self.PLAYER1 and not self.game_over:
                        if(player1.getTag() == "Human"):


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
                                col = player1.makeMove(event, self.SQUARESIZE)

                                if self.game.is_valid_location(self.board, col):
                                    row = self.game.get_next_open_row(self.board, col)
                                    self.game.drop_piece(self.board, row, col, self.PLAYER1_PIECE)

                                    if self.game.winning_move(self.board, self.PLAYER1_PIECE):
                                        label = myfont.render("Human 1 wins!!", 1, self.RED)
                                        self.screen.blit(label, (40,10))
                                        self.game_over = True
                                        if(player2.getTag() == "Ann"):
                                            player2.train(-100)

                                    self.turn += 1
                                    self.turn = self.turn % 2

                                    self.print_board(self.board)
                                    self.draw_board(self.board, self.screen, pygame)
                                    pygame.time.wait(250)
                        else:
                            tag = player1.getTag()

                            if tag == "Random":
                                col = player1.makeMove(self.COLUMN_COUNT)
                            elif tag == "BestMove":
                                col = player1.makeMove(self.board, self.PLAYER1_PIECE, self.game)
                            elif tag == "MiniMax":
                                col, minimax_score = player1.makeMove(self.board, 2, -math.inf, math.inf, True, self.PLAYER1_PIECE)
                            elif tag == "Ann":
                                col = player1.makeMove(self.board,self.PLAYER1_PIECE)
                            #col = pick_best_move(board, AI_PIECE)
                            #col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

                            if self.game.is_valid_location(self.board, col):
                                row = self.game.get_next_open_row(self.board, col)
                                self.game.drop_piece(self.board, row, col, self.PLAYER1_PIECE)

                                self.print_board(self.board)
                                self.draw_board(self.board, self.screen, pygame)

                                self.turn += 1
                                self.turn = self.turn % 2
                                #pygame.time.wait(250)

                                if self.game.winning_move(self.board, self.PLAYER1_PIECE):
                                    label = myfont.render(
                                        str(tag) + " wins!!", 1, self.RED)
                                    self.screen.blit(label, (40, 10))
                                    self.game_over = True
                                    player1wins = player1wins + 1
                                    if(player2.getTag() == "Ann"):
                                        player2.train(-100)
                                    elif (player1.getTag() == "Ann"):
                                        player1.train(100)
                                        player1.wins = player1.wins + 1
                                    
                                    if self.startTurn == 0:
                                        self.startTurn = 1
                                    else:
                                        self.startTurn = 0
                                        


                    # # Ask for Player 2 Input
                    if self.turn == self.PLAYER2 and not self.game_over:
                        if(player2.getTag() == "Human"):
                            if event.type == pygame.MOUSEMOTION:
                                pygame.draw.rect(self.screen, self.BG, (0,0, self.WIDTH, self.SQUARESIZE))
                                posx = event.pos[0]
                                if self.turn == self.PLAYER2:
                                    pygame.draw.circle(self.screen, self.YELLOW, (posx, int(self.SQUARESIZE/2)), self.RADIUS)

                            pygame.display.update()

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pygame.draw.rect(self.screen, self.BG, (0,0, self.WIDTH, self.SQUARESIZE))
                                #print(event.pos)
                                # Ask for Player 2 Input
                                col = player2.makeMove(event, self.SQUARESIZE)

                                if self.game.is_valid_location(self.board, col):
                                    row = self.game.get_next_open_row(self.board, col)
                                    self.game.drop_piece(self.board, row, col, self.PLAYER2_PIECE)

                                    if self.game.winning_move(self.board, self.PLAYER2_PIECE):
                                        label = myfont.render("Human 2 wins!!", 1, self.YELLOW)
                                        self.screen.blit(label, (40,10))
                                        self.game_over = True
                                        
                                        if (player1.getTag() == "Ann"):
                                            player1.train(-100)

                                    self.turn += 1
                                    self.turn = self.turn % 2

                                    self.print_board(self.board)
                                    self.draw_board(self.board, self.screen, pygame)
                                    pygame.time.wait(250)


                        else:
                            tag = player2.getTag()

                            if tag == "Random":
                                col = player2.makeMove(self.COLUMN_COUNT)
                            elif tag == "BestMove":
                                col = player2.makeMove(self.board, self.PLAYER2_PIECE, self.game)
                            elif tag == "MiniMax":
                                col, minimax_score = player2.makeMove(self.board, 2, -math.inf, math.inf, True, self.PLAYER2_PIECE)
                            elif tag == "Ann":
                                col = player2.makeMove(self.board, self.PLAYER2_PIECE)

                            if self.game.is_valid_location(self.board, col):
                                row = self.game.get_next_open_row(self.board, col)
                                self.game.drop_piece(self.board, row, col, self.PLAYER2_PIECE)

                               
                                self.print_board(self.board)
                            
                                self.draw_board(self.board, self.screen, pygame)

                                self.turn += 1
                                self.turn = self.turn % 2
                                #pygame.time.wait(250)

                                if self.game.winning_move(self.board, self.PLAYER2_PIECE):

                                    label = myfont.render(
                                        str(tag)+" wins!!", 1, self.YELLOW)
                                    self.screen.blit(label, (40, 10))
                                    self.game_over = True
                                    player2wins = player2wins + 1
                                    if(player2.getTag() == "Ann"):
                                        player2.train(100)
                                        player2.wins = player2.wins + 1

                                    elif (player1.getTag() == "Ann"):
                                        player1.train(-100)

                                    if self.startTurn == 0:
                                        self.startTurn = 1
                                    else:
                                        self.startTurn = 0
                    #No empty spaces which means game is drawn
                    if 0 not in self.board:
                        self.game_over = True
                        draws = draws + 1
                    #if self.game_over:
                    # pygame.time.wait(3000)
            percentage = self.win_percentage(player1wins,self.games )
            self.player1_wins.append(percentage)
            percentage = self.win_percentage(player2wins, self.games)
            self.player2_wins.append(percentage)
            percentage = self.win_percentage(draws, self.games)
            self.drawn_games.append(percentage)
            self.game_number.append(gameNumber)

        self.plot_history(player1, player2)
