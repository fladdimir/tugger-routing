from typing import Tuple, Type

import numpy as np
from stable_baselines.common.evaluation import evaluate_policy

from tugger_src.gym_env.tugger_env import TuggerEnv


class BaseAgent:
    """ agent which can predict like a stable-baselines agent """

    def predict(
        self, observation: Type[np.ndarray], state=None, deterministic=None
    ) -> Tuple[int, object]:
        raise NotImplementedError()


class BaseAgentFactory:
    def create_agent(self, tugger_env: TuggerEnv) -> BaseAgent:
        raise NotImplementedError()


def evaluate_agent(agent_factory: BaseAgentFactory, n_eval_episodes=10):
    tugger_env = TuggerEnv()
    tugger_env.reset()
    agent = agent_factory.create_agent(tugger_env)
    mean_reward, total_steps = evaluate_policy(
        agent, tugger_env, n_eval_episodes=n_eval_episodes
    )
    print("\nevaluation finished.")
    print("mean reward: %s" % (mean_reward))
    print("average number of gym-steps/episode: %s" % (total_steps / n_eval_episodes))
