import tensorflow as tf
##from agents.human_agent import HumanAgent
from env import Connect4Env
from board import Connect4Board
from agents.random_agent import RandomAgent
from agents.human_agent import HumanAgent
from agents.best_move_agent import BestMoveAgent
from agents.minimax_agent import MiniMaxAgent
from agents.ann_agent import AnnAgent
from agents.ann_agent2 import AnnAgent2
from agents.ann_agent3 import AnnAgent3
from agents.ann_agent4 import AnnAgent4
from agents.ann_agent5 import AnnAgent5
import pygame


def main():

    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE/2 - 5)
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    game = Connect4Board(SQUARESIZE, RADIUS, COLUMN_COUNT, ROW_COUNT)
    env = Connect4Env(SQUARESIZE,ROW_COUNT,COLUMN_COUNT,game)

    #player1 = HumanAgent()
    #player1 = RandomAgent()
    #player1 = BestMoveAgent()
    #player1 = MiniMaxAgent(game)
    #player1 = AnnAgent(game)
    #player1 = AnnAgent2(game)
    #player1 = AnnAgent4(game)
    player1 = AnnAgent5(game)

    #player2 = HumanAgent()
    #player2 = RandomAgent()
    #player2 = BestMoveAgent()
    player2 = MiniMaxAgent(game)
    #player2 = AnnAgent(game)
    #player2 = AnnAgent2(game)
    #player2 = AnnAgent3(game)
    #player2 = AnnAgent4(game)
    
    
    
    env.play(player1,player2)



if __name__ == "__main__":
    main()
