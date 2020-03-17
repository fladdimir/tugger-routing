from typing import Tuple, Type

import numpy as np

from tugger_src.gym_env.des_model.model import coordinates_holder
from tugger_src.rl.base_agent import BaseAgent, BaseAgentFactory, evaluate_agent
from tugger_src.rl.web_animation.base_runnable_tugger_env import (
    base_run_process_animation,
    base_run_tilemap_animation,
)


class Agent(BaseAgent):
    """ acts randomly """

    def predict(
        self, observation: Type[np.ndarray], state=None, deterministic=None
    ) -> Tuple[int, object]:
        target = coordinates_holder.get_random_location_name()
        action = coordinates_holder.get_location_index_by_name(target)
        return action, None


class AgentFactory(BaseAgentFactory):
    """ creates RandomAgents """

    def create_agent(self, tugger_env):
        return Agent()


def evaluate(episodes=10):
    evaluate_agent(AgentFactory(), n_eval_episodes=episodes)


def run_process_animation():
    base_run_process_animation(AgentFactory())


def run_tilemap_animation():
    base_run_tilemap_animation(AgentFactory())
