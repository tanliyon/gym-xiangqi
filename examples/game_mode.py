from agents.random_agent import RandomAgent
from gym_xiangqi.constants import AGENT, PIECE_ID_TO_NAME, BLACK
from gym_xiangqi.utils import action_space_to_move

import gym
import time

from gym_xiangqi.envs import XiangQiEnv


def main():
    env = XiangQiEnv()
    env.render()
    agent = RandomAgent()

    done = False
    round = 0
    while not done:
        # Add a slight delay to properly visualize the game.
        time.sleep(1)

        action = agent.move(env)
        _, reward, done, _ = env.step_game_mode(action)
        turn = "Agent" if env.turn == AGENT else "Enemy"
        move = action_space_to_move(action)
        piece = PIECE_ID_TO_NAME[move[0]]

        print(f"Round: {round}")
        print(f"{turn} made the move {piece} from {move[1]} to {move[2]}.")
        print(f"Reward: {reward}")
        print("================")

        round += 1
        env.render()
    env.close()


if __name__ == '__main__':
    main()
