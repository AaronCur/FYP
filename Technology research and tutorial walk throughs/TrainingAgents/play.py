import tensorflow as tf
from agents.human_agent import HumanAgent
from agents.simple_agent import SimpleAgent
from agents.td_agent import TDAgent
from agents.forward_agent import ForwardAgent
from agents.backward_agent import BackwardAgent
from agents.leaf_agent import LeafAgent
from agents.random_agent import RandomAgent
from model import ValueModel
from env import TicTacToeEnv


def main():
    log_dir = './log/TD2'
    env = TicTacToeEnv()
    model = ValueModel(env.feature_vector_size, 100)
    #agent2 = SimpleAgent('agent_0', model, env)
    # agent = TDAgent('agent_0', model, env)
    #agent2 = ForwardAgent('agent_0', model, env)
    agent = BackwardAgent('agent_0', model, env)
    agent2 = BackwardAgent('agent_0', model, env)
    #agent = RandomAgent('agent_0', model, env)
    #agent = LeafAgent('agent_0', model, env)
    random_agent = RandomAgent(env)
    #human = HumanAgent(env)

    with tf.train.SingularMonitoredSession(checkpoint_dir=log_dir) as sess:
        agent.sess = sess
        env.sess = sess
        players = [agent2, agent]
        env.play(players, verbose=True)

if __name__ == "__main__":
    main()
