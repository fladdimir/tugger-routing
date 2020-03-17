from stable_baselines import DQN as Agent
from stable_baselines.deepq import MlpPolicy

from tugger_src.rl.stable_baselines.base import (
    load_run_process_animation_base,
    load_run_tilemap_animation_base,
    train_base,
)


def train():
    train_base(Agent, MlpPolicy)


def load_run_tilemap_animation():
    load_run_tilemap_animation_base(Agent)


def load_run_process_animation():
    load_run_process_animation_base(Agent)
