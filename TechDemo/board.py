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
        

    def create_board(self):
        board = np.zeros((self.ROW_COUNT,self.COLUMN_COUNT))
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

    def can_win(self, board, piece):
        winning_moves =[]
        # Check horizontal locations for winable move
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

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

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

    def is_terminal_node(self,board):
        return self.winning_move(board, self.PLAYER1_PIECE) or self.winning_move(board, self.PLAYER2_PIECE) or len(self.get_valid_locations(board)) == 0

       
