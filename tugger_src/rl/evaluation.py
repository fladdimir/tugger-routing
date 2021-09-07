from typing import Optional, Tuple

import numpy as np
from stable_baselines3.common.evaluation import evaluate_policy
from tugger_src.gym_env.tugger_env import TuggerEnv
from tugger_src.rl.base_agent import BaseAgent, BaseAgentFactory


class PredictingAgent:
    def __init__(self, agent: BaseAgent) -> None:
        self.agent = agent

    def predict(
        self,
        observation: np.ndarray,
        state: Optional[np.ndarray] = None,
        mask: Optional[np.ndarray] = None,
        deterministic: bool = False,
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        action, _ = self.agent.predict(observation, state, deterministic)
        return [action], _  # int action -> action array for evaluation


def evaluate_agent(agent_factory: BaseAgentFactory, n_eval_episodes=10):
    tugger_env = TuggerEnv()
    tugger_env.reset()
    agent = agent_factory.create_agent(tugger_env)
    predicting_agent = PredictingAgent(agent)
    mean_reward, _ = evaluate_policy(
        predicting_agent, tugger_env, n_eval_episodes=n_eval_episodes
    )
    print("\nevaluation finished.")
    print("mean reward: %s" % (mean_reward))
