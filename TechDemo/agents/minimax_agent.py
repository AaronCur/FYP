import math
import random

class MiniMaxAgent():
    def __init__(self, game):
        self.difficulty = 1
        self.tag = "MiniMax"
        self.game = game

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
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

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
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def getTag(self):
        return self.tag
