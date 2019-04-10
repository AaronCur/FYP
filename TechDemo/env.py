import numpy as np
from board import Connect4Board
from random import choice
import pygame
from pygame.locals import *
import math
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pylab
import threading


class Connect4Env:
    def __init__(self, squaresize,row,col,game):
        self.SQUARESIZE = squaresize
        self. RADIUS = int(self.SQUARESIZE/2 - 6)
        self.ROW_COUNT = row
        self.COLUMN_COUNT = col

        self.game = game
        pygame.init()

        self.WIDTH = self.game.COLUMN_COUNT * self.SQUARESIZE
        self.HEIGHT = (self.game.ROW_COUNT + 1) * self.SQUARESIZE

        self.size = (1920, 1080)

        self.screen = pygame.display.set_mode(self.size)
        self.display_screen = self.screen.copy()
        pygame.display.set_caption("FYP")
        
        self.board = self.game.create_board()

        self.game_over = False
        self.turn = 0
               
        self.PLAYER1 = 0
        self.PLAYER2 = 1

        self.EMPTY = 0
        self.PLAYER1_PIECE = 1
        self.PLAYER2_PIECE = 2

        self.BG = (255,255,255)
        self.BOARD = (66,134,215)
        self.RED = (250,56,46)
        self.YELLOW = (250,232,46)
        self.STATS = (127,127,127)

        self.win_his =[]
        self.player1_wins = []
        self.player2_wins = []
        self.drawn_games = []
        self.game_number = []

        self.games = 10
        self.battles = 100

        self.gui = False
        self.startTurn = 0

        self.totalPlayer1wins = 0
        self.totalPlayer2wins = 0
        self.myfont = pygame.font.SysFont("monospace", 60)

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
                pygame.draw.rect(screen, self.BOARD, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE , self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(screen, self.BG, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.HEIGHT-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, self.YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.HEIGHT-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        
        #pygame.display.update()
    
    def display_stats(self, player1, player2):
        #myfont = pygame.font.SysFont("monospace", 45)

        statsPosX = (self.screen.get_rect().width / 4) * 3

        agentText = self.myfont.render(
                " : Agent : ", 1, self.BOARD)
        self.screen.blit(agentText, (statsPosX - 
        agentText.get_rect().width / 2, 100))
        
        agent1 = self.myfont.render(
                str(player1.description) , 1, self.RED)
        self.screen.blit(agent1, (statsPosX- 
        (agentText.get_rect().width / 2) - agent1.get_rect().width, 100))
        
        agent2 = self.myfont.render(
                 str(player2.description), 1, self.YELLOW)
        self.screen.blit(agent2, (statsPosX+ 
        (agentText.get_rect().width / 2) , 100))
        

        wins = self.myfont.render(
                " : Wins : ", 1, self.BOARD)
        self.screen.blit(wins, (statsPosX - 
        wins.get_rect().width / 2, 200))
        
        player1WinsText = self.myfont.render(
                str(self.totalPlayer1wins)+ " ", 1, self.STATS)
        self.screen.blit(player1WinsText, (statsPosX -
        (wins.get_rect().width / 2) - player1WinsText.get_rect().width, 200))
        temp = wins.get_rect().center
        
        player2WinsText = self.myfont.render(
               " " + str(self.totalPlayer2wins), 1, self.STATS)
        self.screen.blit(player2WinsText, (statsPosX + 
        (wins.get_rect().width / 2) , 200))
        

        currentPercent = self.myfont.render(
                " : Current% : ", 1, self.BOARD)
        self.screen.blit(currentPercent, (statsPosX - 
        currentPercent.get_rect().width / 2, 300))

        if len(self.player1_wins) > 0:
            currentP1Percentage = self.player1_wins[-1]
        else:
            currentP1Percentage = 0

        if len(self.player2_wins) >0:
            currentP2Percentage = self.player2_wins[-1]
        else:
            currentP2Percentage = 0
        
        
        player1Percentage = self.myfont.render(
                 str(currentP1Percentage) + "%" , 1, self.STATS)
        self.screen.blit(player1Percentage, ((statsPosX - 
        currentPercent.get_rect().width / 2) - player1Percentage.get_rect().width, 300))

        player2Percentage = self.myfont.render(
                 str(currentP2Percentage) + "%" , 1, self.STATS)
        self.screen.blit(player2Percentage, ((statsPosX + 
        currentPercent.get_rect().width / 2), 300))

        overall = self.myfont.render(
                " : Win% : ", 1, self.BOARD)
        self.screen.blit(overall, (statsPosX - 
        overall.get_rect().width / 2, 400))

        player1Overall = self.myfont.render(
                 str(round(self.win_percentage(self.totalPlayer1wins,self.gameNumber),2)) + "% " , 1, self.STATS)
        self.screen.blit(player1Overall, ((statsPosX - 
        overall.get_rect().width / 2) - player1Overall.get_rect().width, 400))

        player2Overall = self.myfont.render(
                 " " + str(round(self.win_percentage(self.totalPlayer2wins,self.gameNumber),2)) + "%", 1, self.STATS)
        self.screen.blit(player2Overall, (statsPosX + 
        overall.get_rect().width / 2, 400))
        

    def calc_avg(self, wins):
        if wins == []:
            return 0
        else:
            return sum(wins) / len(wins) 


    def plot_history(self, player1, player2):
        
        #plt.figure(1)
        
        #plt.xlabel('Games Played')
        #plt.ylabel('Winning Rate %')
        drawsAvg = self.calc_avg(self.drawn_games)
        #if len(self.drawn_games) != 0:
         #   plt.plot(self.game_number,self.drawn_games,'b-', label="Draws" + ": " + str(drawsAvg) + "%" )
        player1Avg = self.calc_avg(self.player1_wins)
        player2Avg = self.calc_avg(self.player2_wins)
        ##For outputting graphs for testing pirposes
        #if player1.getTag() == "Ann" or player1.getTag()=="Q":
           # plt.plot(self.game_number,self.player2_wins,'r-', label=player2.getTag() + ": " + str(player2Avg) + "%" )
           # plt.plot(self.game_number, self.player1_wins, 'g-', label=player1.getTag() + ": " + str(player1Avg) + "%")
            #plt.title(str(player1.description)+' vs ' + str(player2.description))
           
       # elif player2.getTag() == "Ann" or player2.getTag() == "Q":
           # plt.plot(self.game_number,self.player2_wins,'g-', label=player2.getTag() + ": " + str(player2Avg) + "%")
            #plt.plot(self.game_number, self.player1_wins, 'r-', label=player1.getTag() + ": " + str(player1Avg) + "%")
            #if player1.training == False:
               # plt.title('Trained '+ str(player2.description)+' vs ' + str(player1.tag))
            #else:
                #plt.title('Training '+ str(player2.description)+' vs ' + str(player1.tag))
        #else :
           # plt.plot(self.game_number,self.player2_wins,'y-', label=player2.getTag() + ": " + str(player2Avg) + "%" )
            #plt.plot(self.game_number, self.player1_wins, 'r-', label=player1.getTag() + ": " + str(player1Avg) + "%")
            #plt.title(str(player1.description)+' vs ' + str(player2.description))
           

    
        #plt.legend()

        #plt.draw()
        #plt.savefig("graph.png")
        #graphImg = pygame.image.load("graph.png")
        #self.screen.fill(self.BG)
        #self.screen.blit(graphImg, (700,100))
        #pygame.display.update()
        #plt.show(block = False)

        matplotlib.use("Agg")
        fig = pylab.figure(figsize=[8, 4],  # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
        ax = fig.gca()
        ax.set_xlabel("Games Played")
        ax.set_ylabel("Winning Rate %")
        ax.set_xlim([0,1000])
        ax.set_ylim([0, 100])

        
        ax.plot(self.game_number,self.drawn_games,'b-', label="Draws " + ": " + str(round(drawsAvg,2)) + "%" )
        ax.plot(self.game_number, self.player2_wins, 'y-',
                label=player2.getTag() + ": " + str(round(player2Avg, 2)) + "%")
        ax.plot(self.game_number,self.player1_wins,'r-', label=player1.getTag()+ ": " + str(round(player1Avg,2)) + "%" )
        
        
        ax.set_title(str(player1.description)+' vs ' + str(player2.description))
        
      
        ax.legend()
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        self.graph_surf = pygame.image.fromstring(raw_data, size, "RGB")

    def final_graph(self,player1, player2):
        matplotlib.use("TkAgg")
        drawsAvg = self.calc_avg(self.drawn_games)
        player1Avg = self.calc_avg(self.player1_wins)
        player2Avg = self.calc_avg(self.player2_wins)
        plt.figure()
        plt.xlim([-10, 1010])
        plt.ylim([-10, 110])

        plt.xlabel('Games Played')
        plt.ylabel('Winning Rate %')
        drawsAvg = self.calc_avg(self.drawn_games)

        plt.plot(self.game_number, self.drawn_games, 'b-',
                 label="Draws" + ": " + str(drawsAvg) + "%")

        plt.plot(self.game_number, self.player2_wins, 'y-',
                 label=player2.getTag() + ": " + str(player2Avg) + "%")
        plt.plot(self.game_number, self.player1_wins, 'r-',
                 label=player1.getTag() + ": " + str(player1Avg) + "%")
        plt.title(str(player1.description) +
                  ' vs ' + str(player2.description))

        plt.legend()
        plt.show()

    def win_percentage(self,wins, games):
        percentage = 100 * float(wins) / float(games)
        self.win_his.append(percentage)
        return percentage

    def play(self,player1, player2):
        self.gameNumber = 0
        myfont = pygame.font.SysFont("monospace", 75)
       
        
        for i in range(self.battles):
            player1wins = 0
            player2wins = 0
            draws = 0
            #self.plot_history(player1, player2)
            for i in range(self.games):

                self.startTurn = 0
                self.turn = self.startTurn
                
                self.gameNumber+=1
            
                self.game_over = False
            
                self.board = self.game.create_board()
                print("episode "+ str(i))
                
                #self.display_stats(player1,player2)
                if i == 0:
                    self.plot_history(player1,player2)
                
                self.screen.fill(self.BG)
                numGames = myfont.render(
                "Game: " + str(self.gameNumber), 1, self.RED)
                self.screen.blit(numGames, (40, 10))

                self.draw_board(self.board, self.screen, pygame)
                self.display_stats(player1,player2)
                
                self.screen.blit(self.graph_surf, ((self.screen.get_rect().width / 4) * 3 - 400,500))
                self.display_screen.blit(pygame.transform.scale(self.screen, self.size), (0,0))
                pygame.display.flip()

                
            
                while not self.game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                sys.exit()
                        if event.type == pygame.VIDEORESIZE:
                            pass
                            self.size = event.dict['size']
                            self.display_screen = pygame.display.set_mode(self.size,RESIZABLE)
                            # On the next line, if only part of the window
                            # needs to be copied, there's some other options.
                            #urface.blit(old_surface_saved, (0,0))
                            #del old_surface_saved

                   
                    
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
                                        player1wins = player1wins + 1
                                        self.totalPlayer1wins = self.totalPlayer1wins + 1
                                        if(player2.getTag() == "Ann"):
                                            player2.train(-100)
                                        
                                        elif player2.getTag() == "Q":
                                            player2.update_values(-100)
                                            player2.train()

                                    self.turn += 1
                                    self.turn = self.turn % 2

                                    self.print_board(self.board)
                                   
                                    self.draw_board(self.board, self.screen, pygame)
                                    
                                    pygame.display.update()
                                    
                                    pygame.time.wait(250)
                        else:
                            tag = player1.getTag()

                            if tag == "Random":
                                col = player1.makeMove(self.COLUMN_COUNT)
                            elif tag == "BestMove":
                                col = player1.makeMove(self.board, self.PLAYER1_PIECE, self.game)
                            elif tag == "MiniMax":
                                depth = 2
                                col, minimax_score = player1.makeMove(
                                    self.board, depth, -math.inf, math.inf, True, self.PLAYER1_PIECE)
                            elif tag == "MiniMax level 2":
                                depth = 3
                                col, minimax_score = player1.makeMove(
                                    self.board, depth, -math.inf, math.inf, True, self.PLAYER1_PIECE)
                            elif tag == "rnd MiniMax":
                                depth = 3
                                col, minimax_score = player1.makeMove(
                                    self.board, depth, -math.inf, math.inf, True, self.PLAYER1_PIECE)
                            elif tag == "Ann" or tag == "Q":
                                col = player1.makeMove(self.board,self.PLAYER1_PIECE)
                            #col = pick_best_move(board, AI_PIECE)
                            #col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

                            if self.game.is_valid_location(self.board, col):
                                row = self.game.get_next_open_row(self.board, col)
                                self.game.drop_piece(self.board, row, col, self.PLAYER1_PIECE)

                                self.print_board(self.board)
                               
                                self.draw_board(self.board, self.screen, pygame)
                              
                                pygame.display.update()
                               

                                self.turn += 1
                                self.turn = self.turn % 2
                                #pygame.time.wait(250)

                                if self.game.winning_move(self.board, self.PLAYER1_PIECE):
                                    label = myfont.render(
                                        str(tag) + " wins!!", 1, self.RED)
                                    self.screen.blit(label, (40, 10))
                                    self.game_over = True
                                    player1wins = player1wins + 1
                                    self.totalPlayer1wins = self.totalPlayer1wins + 1
                                    if(player2.getTag() == "Ann"):
                                        player2.train(-100)
                                    elif (player1.getTag() == "Ann"):
                                        player1.train(100)
                                    
                                    if player1.getTag() == "Q":
                                        player1.update_values(100)
                                        player1.train()
                                    elif player2.getTag() == "Q":
                                        player2.update_values(-100)
                                        player2.train()

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
                                        player2wins = player2wins + 1
                                        self.totalPlayer2wins= self.player2_wins + 1
                                        if (player1.getTag() == "Ann"):
                                            player1.train(-100)

                                    self.turn += 1
                                    self.turn = self.turn % 2

                                    self.print_board(self.board)
                                    
                                    self.draw_board(self.board, self.screen, pygame)
                              
                                    pygame.display.update()
                                   
                                    pygame.time.wait(250)


                        else:
                            tag = player2.getTag()

                            if tag == "Random":
                                col = player2.makeMove(self.COLUMN_COUNT)
                            elif tag == "BestMove":
                                col = player2.makeMove(self.board, self.PLAYER2_PIECE, self.game)
                            elif tag == "MiniMax":
                                depth = 2
                                col, minimax_score = player2.makeMove(
                                    self.board, depth, -math.inf, math.inf, True, self.PLAYER2_PIECE)
                            elif tag == "MiniMax level 2":
                                depth = 3
                                col, minimax_score = player2.makeMove(
                                    self.board, depth, -math.inf, math.inf, True, self.PLAYER2_PIECE)
                            elif tag == "rnd MiniMax":
                                depth = 3
                                col, minimax_score = player2.makeMove(
                                    self.board, depth, -math.inf, math.inf, True, self.PLAYER2_PIECE)
                            elif tag == "Ann":
                                col = player2.makeMove(self.board, self.PLAYER2_PIECE)

                            if self.game.is_valid_location(self.board, col):
                                row = self.game.get_next_open_row(self.board, col)
                                self.game.drop_piece(self.board, row, col, self.PLAYER2_PIECE)

                               
                                self.print_board(self.board)
                              
                                self.draw_board(self.board, self.screen, pygame)
                                
                                pygame.display.update()
                               

                                self.turn += 1
                                self.turn = self.turn % 2
                                #pygame.time.wait(250)

                                if self.game.winning_move(self.board, self.PLAYER2_PIECE):

                                    label = myfont.render(
                                        str(tag)+" wins!!", 1, self.YELLOW)
                                    self.screen.blit(label, (40, 10))
                                    self.game_over = True
                                    player2wins = player2wins +1
                                    self.totalPlayer2wins = self.totalPlayer2wins + 1
                                    if(player2.getTag() == "Ann"):
                                        player2.train(100)

                                    elif (player1.getTag() == "Ann"):
                                        player1.train(-100)

                                    if player2.getTag() == "Q":
                                        player2.update_values(100)
                                        player2.train()
                                    elif player1.getTag() == "Q":
                                        player1.update_values(100)
                                        player1.train()
                                 

                                    if self.startTurn == 0:
                                        self.startTurn = 1
                                    else:
                                        self.startTurn = 0
                    #No empty spaces which means game is drawn
                    if 0 not in self.board:
                        self.game_over = True
                        draws = draws + 1
                        if player1.getTag() == "Q":
                            player1.update_values(50)
                            player1.train()
                        if player2.getTag() == "Q":
                            player2.update_values(50)
                            player2.train()
                    #if self.game_over:   # pygame.time.wait(3000)
            percentage = self.win_percentage(player1wins,self.games )
            self.player1_wins.append(percentage)
            percentage = self.win_percentage(player2wins, self.games)
            self.player2_wins.append(percentage)
            percentage = self.win_percentage(draws, self.games)
            self.drawn_games.append(percentage)
            self.game_number.append(self.gameNumber)
        #self.final_graph(player1,player2)
        threading.Thread(target=self.final_graph,
                        args=(player1, player2)
                       ).start()
        print("reached")
        pygame.time.wait(1000)
        if player1.description == "ANNeGreedy trained with random moves":
            player1.train_model()

