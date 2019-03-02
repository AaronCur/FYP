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

    env = Connect4Env()

    #player1 = HumanAgent()
    #player1 = RandomAgent()
    #player1 = BestMoveAgent()
    player1 = MiniMaxAgent()

    #player2 = HumanAgent()
    #player2 = RandomAgent()
    #player2 = BestMoveAgent()
    player2 = MiniMaxAgent()
    
    
    
    env.play(player1,player2)



if __name__ == "__main__":
    main()
