import os
import time
from typing import Callable

import matplotlib.pyplot as plt
import pandas
from stable_baselines.bench import Monitor
from stable_baselines.common import BaseRLModel
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env.dummy_vec_env import DummyVecEnv

from tugger_src.gym_env.tugger_env import Info, TuggerEnv
from tugger_src.rl.base_agent import BaseAgentFactory
from tugger_src.rl.stable_baselines.config import STEPS
from tugger_src.rl.web_animation.base_runnable_tugger_env import (
    base_run_process_animation,
    base_run_tilemap_animation,
)

STEPS = int(STEPS)  # needs to be int


def _get_save_path(AgentClass):
    save_name = "_temp_" + AgentClass.__name__ + "_" + str(STEPS)
    # (*_temp_* files will be .gitignored)

    save_dir = "training_results"
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, save_name)
    return save_path


def create_monitor_dummy_vec_env(save_path: str):
    env = TuggerEnv()
    env = Monitor(
        env,
        filename=save_path,
        allow_early_resets=False,
        info_keywords=(Info.FINISHED_PRODUCTS.value,),
    )
    env = DummyVecEnv([lambda: env])
    return env


def train_base(AgentClass: Callable[..., BaseRLModel], PolicyClass=MlpPolicy):
    save_path = _get_save_path(AgentClass)

    start = time.time()

    env = create_monitor_dummy_vec_env(save_path)
    agent = AgentClass(PolicyClass, env)
    agent.learn(total_timesteps=STEPS)
    agent.save(save_path)

    needed_time = time.time() - start
    print("\ndone.\ntime: %.2f [sec]" % (needed_time))


class SbAgentFactory(BaseAgentFactory):
    def __init__(self, AgentClass) -> None:
        self.save_path = _get_save_path(AgentClass)
        self.AgentClass = AgentClass

    def create_agent(self, tugger_env: TuggerEnv):
        return self.AgentClass.load(self.save_path)


def load_run_tilemap_animation_base(AgentClass):
    agent_factory = SbAgentFactory(AgentClass)
    base_run_tilemap_animation(agent_factory)


def load_run_process_animation_base(AgentClass):
    agent_factory = SbAgentFactory(AgentClass)
    base_run_process_animation(agent_factory)


def plot(path: str, column=Info.FINISHED_PRODUCTS.value):
    print("plotting " + path)
    df = pandas.read_csv(path, skiprows=1)
    print(df.head())
    plt.plot(df[column])
    plt.show()


def plot_training(AgentClass):
    path = _get_save_path(AgentClass) + ".monitor.csv"
    plot(path)


# to be added: helper for multiprocess-monitor
# sub-processes need to log to separated files
# example:
# https://github.com/araffin/rl-baselines-zoo/blob/master/utils/utils.py#L112
