import gym


def main():
    env = gym.make('gym_xiangqi:xiangqi-v0')

    game_over = False
    count = 0
    while not game_over:
        print(f'Round {count}')
        env.render()
        action = 5
        state, reward, done, info = env.step(action)
        count += 1

        if count == 10:
            break
    env.close()


if __name__ == '__main__':
    main()
