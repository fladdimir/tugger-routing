from tugger_src.gym_env.des_model.blocks.product_station import ProductStation
from gym.spaces import Discrete

from tugger_src.gym_env.base.desim_env import DESimEnv
from tugger_src.gym_env.base.gym_helper import BaseEnvironmentFactory
from tugger_src.gym_env.des_model.model import Model
from tugger_src.gym_env.tugger_env_model_state_converter import (
    TuggerEnvModelStateConverter,
)

from enum import Enum


class Info(Enum):
    FINISHED_PRODUCTS = "finished_products"


class TuggerEnv(DESimEnv):
    """Wraps the tugger-routing des model as gym env"""

    NUMBER_OF_ACTIONS = 11
    TIME_TO_BE_DONE = 86400  # 1 day

    model: Model

    def __init__(self, environment_factory=BaseEnvironmentFactory()):
        """ optional environment provider e.g. for setup of RealtimeEnvironments """

        action_space = Discrete(self.NUMBER_OF_ACTIONS)
        observation_space = TuggerEnvModelStateConverter.observation_space
        model_state_converter = TuggerEnvModelStateConverter()
        super().__init__(action_space, observation_space, model_state_converter)

        self.environment_factory = environment_factory

        self.expected_reward = 0

    # implement abstract methods:

    def setup_sim(self):
        env = self.environment_factory.create_env()
        self.model = Model(env)

    def initialize_action_and_reward_holder(self):
        self.model.sink.reward_holder = self.reward_holder
        self.model.movement.action_holder = self.action_holder

    def check_if_model_is_done(self) -> bool:
        return self.model.env.now >= self.TIME_TO_BE_DONE

    # optional overrides:

    def get_reward(self, time_needed_for_step: int, done: bool) -> float:
        # introduce a "cost" penalty for elapsed time to reward time-efficient behaviour

        # To facilitate learning, reward and penalty need to be balanced.
        # When taking some upper bound to calculate the expectaction,
        # there will be no learning in the beginning, since any actual reward
        # is small compared to the penalty.
        # -> idea: let the penalty increase with the reward
        # -> the expectation equals the highest reward seen so far
        expected_per_sec = self.expected_reward / self.TIME_TO_BE_DONE
        time_penalty = time_needed_for_step * expected_per_sec

        collected_reward = self.reward_holder.step_reward
        corrected_reward = collected_reward - time_penalty

        self.reward_holder.increase_accumulated_reward(by=corrected_reward)
        return corrected_reward


    def get_info(self):
        info = {}
        info[Info.FINISHED_PRODUCTS.value] = self.model.sink.overall_count_in
        return info

    def before_reset(self):
        self._calculate_expected_reward()
        print("\nReset")
        try:
            print("Episode: %s" % (self.finished_episodes))
            print(
                "Finished gym steps episode: %s"
                % (self.finished_gym_steps_in_current_episode)
            )
            print("Finished gym steps overall: %s" % (self.finished_gym_steps_overall))
            print(
                "Number of finished products: %s" % (self.model.sink.overall_count_in)
            )
            print("Accumulated reward: %s" % (self.reward_holder.accumulated_reward))
        except AttributeError:
            # called before first reset
            pass

    # private helper

    def _calculate_expected_reward(self):
        self.expected_reward = max(self.expected_reward, self.reward_holder.accumulated_reward_raw)
