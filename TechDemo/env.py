import numpy as np
from board import Connect4Board
from random import choice
import pygame
from pygame.locals import *
import math
import random
import matplotlib
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
        self.myfont = pygame.font.SysFont("monospace", 50)

        self.wait_time = 0
        self.paused = False

    #Output the current board state to the console
    def print_board(self,board):
            print(np.flip(board, 0))

    #Calculates the avg of values in a list
    def calc_avg(self, wins):
        if wins == []:
            return 0
        else:
            return sum(wins) / len(wins)

    #Calculates average win percentage by passing in how many wins the player has and the
    #total number of games played
    def win_percentage(self, wins, games):
        percentage = 100 * float(wins) / float(games)
        self.win_his.append(percentage)
        return percentage
    
    #Handles the drawing of the board state to the screen using pygame
    #Along with the board outline itself
    def draw_board(self,board, screen, pygame):
        
        #Draws a blank connect 4 board 
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                #First draws rectangles the colour of the board and overlays with a circle the same colour of the 
                #background to make it look like an empty board
                pygame.draw.rect(screen, self.BOARD, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE , self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(screen, self.BG, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)

        #Loops through each position of the board.
        #If the board state for that position contains a player 1 or player 2 piece its drawn over the empty position
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.HEIGHT-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, self.YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.HEIGHT-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
    
    #Displays the stats as text to the pygame screen for that game sesion for both players
    #Stats include the player names, avg win rate for the last 10 games,
    #avg win rate overall, total number of wins
    def display_stats(self, player1, player2):
        statsPosX = (self.screen.get_rect().width / 4) * 3

        agentText = self.myfont.render(
                ": Agent : ", 1, self.BOARD)
        self.screen.blit(agentText, (statsPosX - 
        agentText.get_rect().width / 2, 100))
        
        agent1 = self.myfont.render(
                str(player1.getDescription()) , 1, self.RED)
        self.screen.blit(agent1, (statsPosX- 
        (agentText.get_rect().width / 2) - agent1.get_rect().width, 100))
        
        agent2 = self.myfont.render(
                 str(player2.getDescription()), 1, self.YELLOW)
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
                " : Step% : ", 1, self.BOARD)
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
                " : Overall% : ", 1, self.BOARD)
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

    #Handles the plotting of a live graph to the pygame screen every 10 games
    #Plots avg win rate over games played
    #Avg win rate is calculated after every set of 10 games over a total of 1000 games
    #This means that there will be 100 data points along the X axis and 10 on the Y
    def plot_history(self, player1, player2):
        #Changes the matplotlib backend to AGG so that the matplotlib graph can be converted to a canvas,
        #then to a surface whihc can be displayed in pygame
        matplotlib.use("Agg")
        drawsAvg = self.calc_avg(self.drawn_games)
        player1Avg = self.calc_avg(self.player1_wins)
        player2Avg = self.calc_avg(self.player2_wins)
       
        matplotlib.use("Agg")
        fig = pylab.figure(figsize=[8, 4],  # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 800x400 pixels
                   )
        ax = fig.gca()
        ax.set_xlabel("Games Played")
        ax.set_ylabel("Winning Rate %")
        ax.set_ylim([-2,102])
        ax.set_xlim([-10, 1010])
        ax.set_ymargin(0.1)

        #Plots the win rate lines for both players along with drawn games%
        #Also displays the overall avg win rate % in the graph legend
        ax.plot(self.game_number,self.drawn_games,'b-', label="Draws " + ": " + str(round(drawsAvg,2)) + "%" )
        ax.plot(self.game_number, self.player2_wins, 'y-',
                label=player2.getTag() + ": " + str(round(player2Avg, 2)) + "%")
        ax.plot(self.game_number,self.player1_wins,'r-', label=player1.getTag()+ ": " + str(round(player1Avg,2)) + "%" )
        
        #Sets the title of the graph depedning on which agents are playing currently
        ax.set_title(str(player1.getDescription())+' vs ' + str(player2.getDescription()))
        ax.grid(True)

        ax.margins(10)
        ax.legend()

        #Converts matplotlib grpah to a canvas assigning it to a surface which can be displayed in pygame
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        self.graph_surf = pygame.image.fromstring(raw_data, size, "RGB")

    def final_graph(self,player1, player2):
        #Switches matplotlib backend to its default TkAgg so that the final graph is outputted in a seperate
        #interactive window allowing the user to adjust its size and save as a png
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
        plt.plot(self.game_number, self.player2_wins, 'r-',
                 label=player2.getTag() + ": " + str(player2Avg) + "%")
        plt.plot(self.game_number, self.player1_wins, 'g-',
                 label=player1.getTag() + ": " + str(player1Avg) + "%")
        plt.title(str(player1.getDescription()) +
                  ' vs ' + str(player2.getDescription()))

        plt.legend()
        #Displays the final graph in a seperate interactive window
        plt.show()

    #Handles the playing of the game player 1 and 2 make moves over 100 battles which consists of 10 games
    #a total of 1000 games
    def play(self,player1, player2):
        self.gameNumber = 0
        myfont = pygame.font.SysFont("monospace", 75)
        legendfont = pygame.font.SysFont("monospace", 40)
       
        for i in range(self.battles):
            player1wins = 0
            player2wins = 0
            draws = 0
          
            for i in range(self.games):

                self.startTurn = 0
                self.turn = self.startTurn
                self.gameNumber+=1
                self.game_over = False
                self.board = self.game.create_board()
                
                #if i == 0 it means that the game is at the start of a new battle, the game has either just been
                #started or 10 games have passed
                if i == 0:
                    self.plot_history(player1,player2)
                
                #Clear the screen with the BG colour
                self.screen.fill(self.BG)
                #Create text to be displayed to the screen
                numGames = myfont.render(
                "Game: " + str(self.gameNumber), 1, self.RED)

                inputs = legendfont.render(
                    "Keyboard Inputs: ", 1, self.STATS)

                playback = legendfont.render(
                    "1-9 -> PlayBack speed", 1, self.STATS)

                pause = legendfont.render(
                    "0 -> Pause", 1, self.STATS)

                #Display text to the screen 
                self.screen.blit(numGames, (40, 10))
                self.screen.blit(inputs, (10, 875))
                self.screen.blit(playback, (10, 925))
                self.screen.blit(pause, (10, 975))
                #Display board and stats to the screen
                self.draw_board(self.board, self.screen, pygame)
                self.display_stats(player1,player2)
                #Display graph to the screen 
                self.screen.blit(self.graph_surf, ((self.screen.get_rect().width / 4) * 3 - 400,500))
                #Scale screen if it has been changed from its starting dimensions of 1920x1080
                self.display_screen.blit(pygame.transform.scale(self.screen, self.size), (0,0))
                #Refresh pygame display
                pygame.display.flip()
                
                while not self.game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                        if event.type == pygame.VIDEORESIZE:
                            #Handles the resizing of the pygame window
                            self.size = event.dict['size']
                            self.display_screen = pygame.display.set_mode(self.size,RESIZABLE)
                        
                        #Keys 1-9 change the wait_time value whihc will be used to slow/speed up playback
                        #Key 0 will pause the game
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                                self.wait_time = "Paused"
                                self.paused = True
                            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                                self.wait_time = 450
                            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                                self.wait_time = 375
                            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                                self.wait_time = 325
                            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                                self.wait_time = 275
                            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                                self.wait_time = 215
                            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                                self.wait_time = 160
                            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                                self.wait_time = 100
                            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                                self.wait_time = 50
                            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                                self.wait_time = 0
                    #Pauses the game
                    if self.wait_time != "Paused":
                        self.paused = False

                    if self.turn == self.PLAYER1 and not self.game_over and self.paused == False:
                        if(player1.getTag() == "Human"):

                            if event.type == pygame.MOUSEMOTION:
                                pygame.draw.rect(self.screen, self.BG, (0,0, self.WIDTH, self.SQUARESIZE))
                                posx = event.pos[0]
                                
                                #Draws piece above the board so the player can move it into their desired column before dropping the piece
                                if self.turn == self.PLAYER1:
                                    pygame.draw.circle(self.screen, self.RED, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                            
                            pygame.display.update()

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pygame.draw.rect(self.screen, self.BG, (0,0, self.WIDTH, self.SQUARESIZE))
                               
                                col = player1.makeMove(event, self.SQUARESIZE)
                                #If the column selected is a valid location, find the next available row and drop the piece here
                                if self.game.is_valid_location(self.board, col):
                                    row = self.game.get_next_open_row(self.board, col)
                                    self.game.drop_piece(self.board, row, col, self.PLAYER1_PIECE)

                                    #If the move made was a winning move train the other player if its an ANN, incredment player 1 wins for that battle aswell as total wins 
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

                                    #Switches to the other players turn
                                    self.turn += 1
                                    self.turn = self.turn % 2

                                    self.print_board(self.board)
                                    self.draw_board(self.board, self.screen, pygame)
                                    
                                    pygame.display.update()
                                    pygame.time.wait(250)
                        else:
                            #If the player isnt a human, check its tag to make the correct make move call
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
                                #Pauses pygame window for time specified by player input keys 1-9
                                pygame.time.wait(self.wait_time)

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
                                    #Sets the start turn for the next game
                                    if self.startTurn == 0:
                                        self.startTurn = 1
                                    else:
                                        self.startTurn = 0
                                        
                    # # Ask for Player 2 Input
                    if self.turn == self.PLAYER2 and not self.game_over and self.paused == False:
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
                                pygame.time.wait(self.wait_time)

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
                                        player1.update_values(-100)
                                        player1.train()
                                 
                                    if self.startTurn == 0:
                                        self.startTurn = 1
                                    else:
                                        self.startTurn = 0
                    #No empty spaces left in the board means that the game was a draw
                    if 0 not in self.board:
                        self.game_over = True
                        draws = draws + 1
                        if player1.getTag() == "Q":
                            player1.update_values(50)
                            player1.train()
                        if player2.getTag() == "Q":
                            player2.update_values(50)
                            player2.train()
            #Calculate the average win rate over the previous 10 games
            percentage = self.win_percentage(player1wins,self.games )
            self.player1_wins.append(percentage)
            percentage = self.win_percentage(player2wins, self.games)
            self.player2_wins.append(percentage)
            percentage = self.win_percentage(draws, self.games)
            self.drawn_games.append(percentage)
            #Append the game number to a list after 10 games,
            #this helps with mapping win rates to the graph later
            self.game_number.append(self.gameNumber)

        #Producing the final graph caused my pc to slow 
        #To avoid this i use multithreading to put this process on a seperate thread,
        #Also avoids the problem of stopping execution of code caused by the output of matplotlib graphs
        threading.Thread(target=self.final_graph,
                        args=(player1, player2)
                       ).start()
        #For a very specific training case that i was testing 
        if player1.getDescription() == "ANNeGreedy trained with random moves":
            player1.train_model()
