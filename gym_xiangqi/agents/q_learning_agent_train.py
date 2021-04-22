from q_learning_agent import QLearningAgent

from gym_xiangqi.constants import ALLY, PIECE_ID_TO_NAME
from gym_xiangqi.utils import action_space_to_move

import tensorflow as tf
import argparse
import os
import gym
import time
import numpy as np
from datetime import datetime
from collections import defaultdict
from gym_xiangqi.constants import ALLY


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--iter', default=10, help="Number of games to train the agent.")
    parser.add_argument('--render', action="store_true", help="If the game should be rendered.")
    parser.add_argument('--load_path', help="Path to load a model from.")
    parser.add_argument('--save_path', help="Path to save the model. Defaults to Y-M-D-Time.hdf5")
    args = parser.parse_args()
    return args


def main():
    """
    Main function to train the q-learning agent
    by playing against itself.
    """
    args = parse_args()
    if not args.save_path:
        args.save_path = os.getcwd() + datetime.now().strftime("/%Y-%m-%d-%H:%M:%S") + ".hdf5"
    env = gym.make('gym_xiangqi:xiangqi-v0')
    agent = QLearningAgent(args.load_path)
    total_reward = defaultdict(float)
    total_loss = defaultdict(float)
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    loss_fn = tf.keras.losses.Huber()
    if args.render:
        env.render()
    
    for i in range(args.iter):
        env.reset()
        done = False
        print("\n===============\n")
        print(f"Round {i}")
        agent_win = False
        move_num = 0
        win_count = 0
        lose_count = 0
        while not done:
            # Agent move.
            agent_action = agent.move(env)
            state = env._state
            agent_next_state, agent_reward, done, _ = env.step(agent_action)
            total_reward[i] += agent_reward
            if done:
                total_reward[i] += agent_reward
                loss = agent.update(state, agent_next_state, agent_action, agent_reward, loss_fn, optimizer)
                total_loss[i] += loss
                agent_win = True
                win_count += 1
                break

            # Enemy move.
            enemy_action = agent.move(env)
            next_state, enemy_reward, done, _ = env.step(enemy_action)
            total_reward[i] -= enemy_reward

            # Update agent.
            loss = agent.update(state, next_state, agent_action, agent_reward, loss_fn, optimizer)
            total_loss[i] += loss

            if args.render:
                env.render()
                time.sleep(0.1)
            if done:
                lose_count += 1
                break
            move_num += 1
            if move_num % 100 == 0:
                agent.update_target_network()
                print(f"Move: {move_num}")
                print(f"Average reward: {total_reward[i] / move_num}")
                print(f"Average loss: {total_loss[i] / move_num}")
            if move_num > 10000:
                break
        agent.update_target_network()
        print(f"Round {i} average reward: {total_reward[i] / move_num}")
        print(f"Round {i} average loss: {total_loss[i] / move_num}")
        end_text = "Agent won! :)" if agent_win else "Agent lost. :("
        print(end_text)
    agent.save(args.save_path)
    env.close()


if __name__ == "__main__":
    main()