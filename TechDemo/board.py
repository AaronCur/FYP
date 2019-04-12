import numpy as np
import pygame
import sys
import math
import random
               
class Connect4Board:
    def __init__(self, squaresize, radius, col, row):
        self.ROW_COUNT = row
        self.COLUMN_COUNT = col
        self.SQUARESIZE = squaresize
        self.PLAYER1 = 0
        self.PLAYER2 = 1
        self.PLAYER1_PIECE = 1
        self.PLAYER2_PIECE = -1
        self.EMPTY = 0
        self.WINDOW_LENGTH = 4
        
    #Initalizes board with 0s, creating an empty board
    def create_board(self):
        board = np.zeros((self.ROW_COUNT,self.COLUMN_COUNT))
        return board

    #Modifies board state by adding a value of certain piece to to the board at that row and column
    def drop_piece(self,board, row, col, piece):
        board[row][col] = piece

    #Checks if placing a piece at a certain col is valid
    #Wont be valid if that column is full
    def is_valid_location(self, board, col):
        return board[self.ROW_COUNT-1][col] == 0

    #At a certain column checks which is the next open row
    #To calculate what row the piece should be placed, at a certain column 
    def get_next_open_row(self,board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    #Checks the board state for wins for whatever piece is passed in
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

    #Checks at a board state if a certain piece can win with their next move
    #For each check a 1 is appended to a list if the player can win and a 0 if not
    #This creates a list of values which can then be compared for different board states
    #Eg if the list of values arent the same from one state to the next it means the other player
    #blocked a winable move
    def can_win(self, board, piece):
        winning_moves =[]
        #For each situation, every case is checked for winable moves,
        #e.g checking each position in a line of 4 that could result in a winning move
        #Check horizontal locations for winable move
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == self.EMPTY:
                    #Check if placing in empty col will result in a win
                    row = self.get_next_open_row(board, c+3)

                    if row == r:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
                        
                if board[r][c] == self.EMPTY and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                        #Check if placingin empty col will result in a win
                    row = self.get_next_open_row(board, c)
                    if row == r:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)

                if board[r][c] == piece and board[r][c+1] == self.EMPTY and board[r][c+2] == piece and board[r][c+3] == piece:
                    #Check if placingin empty col will result in a win
                    row = self.get_next_open_row(board, c+1)
                    if row == r:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
                
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == self.EMPTY and board[r][c+3] == piece:
                    #Check if placingin empty col will result in a win
                    row = self.get_next_open_row(board, c+2)
                    if row == r:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)

        # Check vertical locations for winable move
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == self.EMPTY:
                    winning_moves.append(1)
                else:
                    winning_moves.append(0)

        # Check positively sloped diaganols for winable move
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == self.EMPTY:
                
                    row = self.get_next_open_row(board, c+3)
                    if row == r+3:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
                if board[r][c] == self.EMPTY and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    
                    row = self.get_next_open_row(board, c)
                    if row == r:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)

                if board[r][c] == piece and board[r+1][c+1] == self.EMPTY and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    
                    row = self.get_next_open_row(board, c+1)
                    if row == r+1:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == self.EMPTY and board[r+3][c+3] == piece:
                    
                    row = self.get_next_open_row(board, c+2)
                    if row == r+2:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
        # Check negatively sloped diaganols for winable move
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == self.EMPTY:
                    
                    row = self.get_next_open_row(board, c+3)
                    if row == r-3:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
                if board[r][c] == self.EMPTY and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    
                    row = self.get_next_open_row(board, c)
                
                    if row == r:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
                if board[r][c] == piece and board[r-1][c+1] == self.EMPTY and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
            
                    row = self.get_next_open_row(board, c+1)
                
                    if row == r-1:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == self.EMPTY and board[r-3][c+3] == piece:
                    
                    row = self.get_next_open_row(board, c+2)
                    
                    if row == r-2:
                        winning_moves.append(1)
                    else:
                        winning_moves.append(0)
          
        return winning_moves

    #Returns all valid cols that a piece can be placed in for the board
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    #Searches through the given window (4x4 subgrid of the board) to calculate score for a given move
    def evaluate_window(self,window, piece):
        score = 0
        opp_piece = self.PLAYER1_PIECE
        if piece == self.PLAYER1_PIECE:
            opp_piece = self.PLAYER2_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    #Calculates score for a certain move, for minimax algorithms
    def score_position(self,board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(self.COLUMN_COUNT-3):
                window = row_array[c:c+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(self.ROW_COUNT-3):
                window = col_array[r:r+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    #Checks if either player can win or if the board is full
    def is_terminal_node(self,board):
        return self.winning_move(board, self.PLAYER1_PIECE) or self.winning_move(board, self.PLAYER2_PIECE) or len(self.get_valid_locations(board)) == 0

       
