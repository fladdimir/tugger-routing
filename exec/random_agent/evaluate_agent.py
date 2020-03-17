import sys

sys.path.append(".")

from tugger_src.rl.heuristics.random_agent import evaluate as action

if __name__ == "__main__":
    action(episodes=101)
