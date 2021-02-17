from gym.envs.registration import register

register(
    id='xiangqi-v0',
    entry_point='gym_xiangqi.envs:XiangQiEnv',
)
