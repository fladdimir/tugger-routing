from stable_baselines import PPO2 as Agent

from tugger_src.rl.stable_baselines.base import (
    load_run_process_animation_base,
    load_run_tilemap_animation_base,
    train_base,
)


def train():
    train_base(Agent)


def load_run_tilemap_animation():
    load_run_tilemap_animation_base(Agent)


def load_run_process_animation():
    load_run_process_animation_base(Agent)
