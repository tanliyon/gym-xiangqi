import time

from agents.random_agent import RandomAgent
from gym_xiangqi.constants import (     # NOQA
    RED, BLACK, PIECE_ID_TO_NAME
)
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.envs import XiangQiEnv


def main():
    # Pass in the color you want to play as (RED or BLACK)
    env = XiangQiEnv(RED)
    env.render()
    agent = RandomAgent()

    done = False
    round = 0
    while not done:
        # Add a slight delay to properly visualize the game.
        time.sleep(1)

        _, reward, done, _ = env.step_user()
        piece, start, end = env.user_move_info
        piece = PIECE_ID_TO_NAME[piece]
        end = env.game.end_pos

        print(f"Round: {round}")
        print(f"Player made the move {piece} from {start} to {end}.")
        print(f"Reward: {reward}")
        print("================")

        action = agent.move(env)
        _, reward, done, _ = env.step(action)
        move = action_space_to_move(action)
        piece = PIECE_ID_TO_NAME[move[0]]

        print(f"Round: {round}")
        print(f"RL agent made the move {piece} from {move[1]} to {move[2]}.")
        print(f"Reward: {reward}")
        print("================")

        round += 1
        env.render()
    env.close()


if __name__ == '__main__':
    main()
