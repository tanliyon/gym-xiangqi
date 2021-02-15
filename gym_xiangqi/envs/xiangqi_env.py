import gym
# from gym import error, spaces, utils
# from gym.utils import seeding

class XiangQiEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        pass

    def step(self, action):
        return 0, 0, 0, 0

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass
