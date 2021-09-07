import sys

sys.path.append(".")

from tugger_src.rl.stable_baselines.ppo import train as action


if __name__ == "__main__":
    action()
