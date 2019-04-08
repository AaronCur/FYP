import random

class BestMoveAgent():
    def __init__(self):
         self.tag = "BestMove"
         self.description = self.tag

    def makeMove(self,board, piece, game):

        valid_locations = game.get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = game.get_next_open_row(board, col)
            temp_board = board.copy()
            game.drop_piece(temp_board, row, col, piece)
            score = game.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def getTag(self):
        return self.tag