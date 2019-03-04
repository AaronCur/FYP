import tensorflow as tf
##from agents.human_agent import HumanAgent
from env import Connect4Env
from board import Connect4Board
from agents.random_agent import RandomAgent
from agents.human_agent import HumanAgent
from agents.best_move_agent import BestMoveAgent
from agents.minimax_agent import MiniMaxAgent
import pygame


def main():

    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE/2 - 5)
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    game = Connect4Board(SQUARESIZE, RADIUS, COLUMN_COUNT, ROW_COUNT)
    env = Connect4Env(SQUARESIZE,ROW_COUNT,COLUMN_COUNT,game)

    player1 = HumanAgent()
    #player1 = RandomAgent()
    #player1 = BestMoveAgent()
    #player1 = MiniMaxAgent(game)

    #player2 = HumanAgent()
    #player2 = RandomAgent()
    #player2 = BestMoveAgent()
    player2 = MiniMaxAgent(game)
    
    
    
    env.play(player1,player2)



if __name__ == "__main__":
    main()
