import sys

sys.path.append(".")

from tugger_src.rl.stable_baselines.ppo2 import (
    load_run_tilemap_animation as action,
)

if __name__ == "__main__":
    action()
