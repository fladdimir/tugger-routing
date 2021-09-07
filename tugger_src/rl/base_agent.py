from typing import Tuple, Type

import numpy as np
from tugger_src.gym_env.tugger_env import TuggerEnv


class BaseAgent:
    """agent which can predict like a stable-baselines agent"""

    # tbd: check for stable_baselines3 api changes

    def predict(
        self, observation: Type[np.ndarray], state=None, deterministic=None
    ) -> Tuple[int, object]:
        raise NotImplementedError()


class BaseAgentFactory:
    def create_agent(self, tugger_env: TuggerEnv) -> BaseAgent:
        raise NotImplementedError()
