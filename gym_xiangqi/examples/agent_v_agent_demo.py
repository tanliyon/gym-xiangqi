from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.constants import ALLY, PIECE_ID_TO_NAME
from gym_xiangqi.utils import action_space_to_move

import gym
import time


def main():
    env = gym.make('gym_xiangqi:xiangqi-v0')
    env.render()
    agent = RandomAgent()

    done = False
    round = 0
    while not done:
        # Add a slight delay to properly visualize the game.
        time.sleep(1)

        action = agent.move(env)
        _, reward, done, _ = env.step(action)
        turn = "Ally" if env.turn == ALLY else "Enemy"
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
