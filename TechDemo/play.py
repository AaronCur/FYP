import tensorflow as tf
##from agents.human_agent import HumanAgent
from env import Connect4Env
from board import Connect4Board
from agents.random_agent import RandomAgent
from agents.human_agent import HumanAgent
from agents.best_move_agent import BestMoveAgent
from agents.minimax_agent import MiniMaxAgent
from agents.minimax_2_agent import MiniMax2Agent
from agents.rnd_minimax_agent import RndMiniMaxAgent
from agents.ann_agent import AnnAgent
from agents.ann_agent2 import AnnAgent2
from agents.ann_agent3 import AnnAgent3
from agents.ann_agent4 import AnnAgent4
from agents.ann_agent_250_greedy import AnnAgent250greedy
from agents.ann_agent_22_greedy import AnnAgent22greedy
from agents.ann_agent_basic import AnnAgentBasic
from agents.ann_agent_more_rewards import AnnAgentMoreRewards
from agents.ann_agent_random import AnnAgentRandom
from agents.q_agent import QAgent
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

    Training = True
    #player1 = AnnAgent22greedy(game, Training)
    #player1 = AnnAgent250greedy(game, Training)
    #player1 = AnnAgentBasic(game, Training)
    #player1 = AnnAgentMoreRewards(game, Training)
    #player1 = AnnAgentRandom(game, Training)
    player1 = QAgent(game, Training)

    #player2 = HumanAgent()
    #player2 = RandomAgent()
    #player2 = BestMoveAgent()
    
    player2 = MiniMaxAgent(game)
    #player2 = MiniMax2Agent(game)
    #player2 = RndMiniMaxAgent(game)
    #player2 = AnnAgent(game)
    #player2 = AnnAgent2(game)
    #player2 = AnnAgent3(game)
    #player2 = AnnAgent4(game)
    
    
    
    env.play(player1,player2)



if __name__ == "__main__":
    main()
