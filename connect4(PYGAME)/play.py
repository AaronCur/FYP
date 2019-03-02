import tensorflow as tf
##from agents.human_agent import HumanAgent
from env import Connect4Env
from agents.random_agent import RandomAgent
from agents.human_agent import HumanAgent
import pygame


def main():
   ## log_dir = './log/TD2'

    env = Connect4Env()
    player1 = RandomAgent()
    #player2 = RandomAgent()

   # player1 = HumanAgent()
    player2 = HumanAgent()
    
    env.play(player1,player2)


   ## model = ValueModel(env.feature_vector_size, 100)
    #agent2 = SimpleAgent('agent_0', model, env)
    # agent = TDAgent('agent_0', model, env)
    #agent2 = ForwardAgent('agent_0', model, env)
   ## agent = BackwardAgent('agent_0', model, env)
    #agent = RandomAgent('agent_0', model, env)
    #agent = LeafAgent('agent_0', model, env)
   ## random_agent = RandomAgent(env)
    #human = HumanAgent(env)

   ## with tf.train.SingularMonitoredSession(checkpoint_dir=log_dir) as sess:
       ## agent.sess = sess
       ## env.sess = sess
        ##players = [random_agent, agent]
        ##env.play(players, verbose=True)

if __name__ == "__main__":
    main()
