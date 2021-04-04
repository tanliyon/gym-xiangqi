from gym_xiangqi.envs.xiangqi_env import XiangQiEnv  # NOQA
from gym_xiangqi.agents import RandomAgent  # NOQA
import timeit

""" Timing """
# Number of times to repeat the timing tests.
NUM_REPEAT = 10
# Number of times to call a method for each timing test.
NUM_RUN = 1

""" Setup """
ENV_SETUP = "env = XiangQiEnv()"
AGENT_SETUP = "agent = RandomAgent()"


def print_time(title, time_list):
    """
    Helper function to print latency times
    in a nice format.
    """
    assert len(time_list) == NUM_REPEAT
    print(f"{title}")
    print("--------------------")
    print(f"min    : {min(time_list):.3f}")
    print(f"max    : {max(time_list):.3f}")
    print(f"average: {sum(time_list) / len(time_list):.3f}")
    print("\n")


def s_to_ms(time_list):
    return [t * 1000 for t in time_list]


def measure_time(cmd_str, setup=""):
    return s_to_ms(timeit.repeat(
        cmd_str, setup=setup, globals=globals(),
        repeat=NUM_REPEAT, number=NUM_RUN))


def measure_and_print_latency(methods_to_setup):
    """
    Helper function to measure and print the latency
    of methods specified in methods_to_setup.

    Parameters:
        methods_to_setup (dict[str, str]): Dictionary matching method calls
            to setups needed to perform the call.
    """
    for method, setup in methods_to_setup.items():
        time_list = measure_time(cmd_str=method, setup=setup)
        print_time(title=method, time_list=time_list)


def env_latency():
    """
    Measure and print the latency of the methods defined
    in XiangQiEnv.
    """
    print("XiangQiEnv Latency (ms)")
    print("=========================")

    methods_to_setup = {
        "XiangQiEnv()": "",
        "env.init_pieces()": ENV_SETUP,
        "env.get_possible_actions(player)": f"{ENV_SETUP}; player=1;",
        "env.step(action)":
            f"{ENV_SETUP}; import numpy as np; import random;"
            "actions = np.where(env.ally_actions == 1)[0];"
            "action = random.randint(0, len(actions)-1);"
    }
    measure_and_print_latency(methods_to_setup)


def random_agent_latency():
    """
    Measure and print the latency of the methods defined
    in RandomAgent.
    """
    print("RandomAgent Latency (ms)")
    print("=========================")

    methods_to_setup = {
        "RandomAgent()": "",
        "agent.move(env)": f"{ENV_SETUP}; {AGENT_SETUP}",
    }
    measure_and_print_latency(methods_to_setup)


if __name__ == "__main__":
    # TODO: Compare latency from before and after a PR, and actually
    # fail a PR if the change if too big or if the latency
    # exceed a certain number.
    env_latency()
    random_agent_latency()
