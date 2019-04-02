import math
import random
import heapq


class RndMiniMaxAgent():
    def __init__(self, game):
        self.difficulty = 1
        self.tag = "rnd MiniMax"
        self.game = game
        self.potential_moves = []

    def makeMove(self ,board, depth, alpha, beta, maximizingPlayer, PIECE):
        if PIECE == 1:
            OTHERPIECE = 2
        else:
            OTHERPIECE = 1
        
        valid_locations = self.game.get_valid_locations(board)
        is_terminal = self.game.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.game.winning_move(board, PIECE):
                    return (None, 100000000000000)
                elif self.game.winning_move(board, OTHERPIECE):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.game.score_position(board, PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.game.get_next_open_row(board, col)
                b_copy = board.copy()
                self.game.drop_piece(b_copy, row, col, PIECE)
                new_score = self.makeMove(b_copy, depth-1, alpha, beta, False, PIECE)[1]
                if new_score > value:
                    value = new_score
                    column = col
                    self.potential_moves = [[column, value]]
                elif new_score == value:
                    column = col
                    self.potential_moves.append([column, value])
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                
            max_score_moves = []
            max_score_values = []
            #Iterated through the nested lists return the list that has the highest value
            #in the index of 1
            #max_score = max(self.potential_moves, key=lambda x: x[1])
            #Index number 1 of the returned min_score is the value of that move
            max_score = max_score[1]
            for i in self.potential_moves:
                #This handles sorting through multiple moves that have the same value assocaited with them
                if i[1] == max_score:
                        #Append the value to a new list if its the highest value
                        max_score_moves.append(i[0])
                        #Append the column associated with this value to the list
                        max_score_values.append(i[1])
            #Randomly selects a move that has the same score value associated with them
            #Makes minimax non_deterministic by adding an element of randomness to it 
            index = random.choice(range(len(max_score_moves)))
            result_col = max_score_moves[index]
            result_val = max_score_values[index]
            self.potential_moves = []
            return result_col, result_val

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.game.get_next_open_row(board, col)
                b_copy = board.copy()
                self.game.drop_piece(b_copy, row, col, OTHERPIECE)
                new_score = self.makeMove(b_copy, depth-1, alpha, beta, True, PIECE)[1]
                if new_score < value:
                    value = new_score
                    column = col
                    self.potential_moves = [[column, value]]
                elif new_score == value:
                    column = col
                    self.potential_moves.append([column, value])
                beta = min(beta, value)
                if alpha >= beta:
                    break
                #if new_score == value:
                  #  value = new_score
                   # column = col
                    #self.potential_moves.append([column, value])

            min_score_moves = []
            min_score_values = []
            #Iterated through the nested lists return the list that has the highest value
            #in the index of 1
            min_score = min(self.potential_moves, key=lambda x: x[1])
            #Index number 1 of the returned min_score is the value of that move
            min_score = min_score[1]
            for i in self.potential_moves:
                if i[1] == min_score:
                        min_score_moves.append(i[0])
                        min_score_values.append(i[1])
            index = random.choice(range(len(min_score_moves)))
            result_col = min_score_moves[index]
            result_val = min_score_values[index]
            self.potential_moves = []
            return result_col, result_val

    def getTag(self):
        return self.tag
