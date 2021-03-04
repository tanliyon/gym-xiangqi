from gym_xiangqi.envs.xiangqi_env import XiangQiEnv
from agents.random_agent import RandomAgent
import timeit

NUM_REPEAT = 5
NUM_RUN = 1
ENV_SETUP = "env = XiangQiEnv()"
AGENT_SETUP = "agent = RandomAgent()"


def average(lst):
    return sum(lst) / len(lst)


def print_time(title, time_list):
    print(f"{title}")
    print("--------------------")
    print(f"min    : {min(time_list):.3f}")
    print(f"max    : {max(time_list):.3f}")
    print(f"average: {average(time_list):.3f}")
    print("\n")


def s_to_ms(time_list):
    return [t * 1000 for t in time_list]


def measure_time(cmd_str, setup=""):
    return s_to_ms(timeit.repeat(
        cmd_str, setup=setup, globals=globals(),
        repeat=NUM_REPEAT, number=NUM_RUN))


def print_latency(methods_to_setup):
    for method, setup in methods_to_setup.items():
        time_list = measure_time(cmd_str=method, setup=setup)
        print_time(title=method, time_list=time_list)


def env_latency():
    print(f"XiangQiEnv Latency (ms)")
    print("=========================")

    methods_to_setup = {
        "XiangQiEnv()": "",
        "env.init_pieces()": ENV_SETUP,
        "env.get_possible_actions()": ENV_SETUP,
        "env.step(action)":
            f"{ENV_SETUP}; import numpy as np; import random;"
            f"actions = np.where(env.possible_actions == 1)[0];"
            f"action = random.randint(0, len(actions)-1);"
    }

    print_latency(methods_to_setup)

def random_agent_latency():
    print(f"RandomAgent Latency (ms)")
    print("=========================")

    methods_to_setup = {
        "RandomAgent()": "",
        "agent.move(env)": f"{ENV_SETUP}; {AGENT_SETUP}",
    }

    print_latency(methods_to_setup)


if __name__ == "__main__":
    env_latency()
    random_agent_latency()