from stable_baselines import ACER as Agent

from tugger_src.rl.stable_baselines.base import (
    load_run_process_animation_base,
    load_run_tilemap_animation_base,
    plot_training,
    train_base,
)


def train():
    train_base(Agent)


def load_run_tilemap_animation():
    load_run_tilemap_animation_base(Agent)


def load_run_process_animation():
    load_run_process_animation_base(Agent)


def plot():
    plot_training(Agent)
