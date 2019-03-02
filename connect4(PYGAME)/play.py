import tensorflow as tf
##from agents.human_agent import HumanAgent
from env import Connect4Env
import pygame


def main():
   ## log_dir = './log/TD2'

    env = Connect4Env()

    env.play(1,2)


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
