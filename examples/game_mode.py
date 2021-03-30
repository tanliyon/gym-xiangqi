import time

from agents.random_agent import RandomAgent
from gym_xiangqi.constants import (     # NOQA
    RED, BLACK, PIECE_ID_TO_NAME, AGENT
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
        if env.turn == AGENT:
            _, reward, done, _ = env.step_user()

            player = "You"
            piece, start, end = env.user_move_info
            piece = PIECE_ID_TO_NAME[piece]
            end = env.game.end_pos
        else:
            time.sleep(1)
            action = agent.move(env)
            _, reward, done, _ = env.step(action)

            player = "RL Agent"
            move = action_space_to_move(action)
            piece = PIECE_ID_TO_NAME[move[0]]
            start = move[1]
            end = move[2]

        env.render()
        round += 1
        print(f"Round: {round}")
        print(f"{player} made the move {piece} from {start} to {end}.")
        print(f"Reward: {reward}")
        print("================")

    env.close()


if __name__ == '__main__':
    main()
