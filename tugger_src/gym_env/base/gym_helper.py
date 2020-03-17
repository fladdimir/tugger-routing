""" helper classes for gym environment wrapping """
from multiprocessing import Value

from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment,
    SyncedFloat,
)
from gym.spaces import Space
from simpy import Environment, Event


class RewardHolder:
    """ collects the reward per step and per episode """

    def __init__(self):
        self.step_reward: float = 0
        self.accumulated_reward_raw: float = 0  # without correction
        self.accumulated_reward: float = 0  # with correction after each step

    def increase_step_reward(self, by: float):
        self.step_reward += by
        self.accumulated_reward_raw += by

    def increase_accumulated_reward(self, by: float):
        self.accumulated_reward += by

    def reset_step_reward(self):
        self.step_reward = 0


class ActionHolder:
    """ provides a central point of access to global actions """

    action_needed: Event  # will be succeeded somewhere when an action is needed, so that we can run until
    provided_action: Event  # to be succeeded to communicate back the action to whereever its needed


class BaseModel:
    """ consists of a simpy environment which can be used for execution """

    env: Environment


class ModelStateConverter:
    """ returns the observation for a given model """

    def model_state_to_observation(self, model: BaseModel) -> Space:
        raise NotImplementedError()


class BaseEnvironmentFactory:
    """ creates simpy environments """

    def create_env(self):
        return Environment()


class RealtimeEnvironmentFactory(BaseEnvironmentFactory):
    """ creates casymda realtime environments which can be controlled from a different process """

    def __init__(
        self,
        synced_float: SyncedFloat = ChangeableFactorRealtimeEnvironment.create_factor_instance(),
        should_run: Value = ChangeableFactorRealtimeEnvironment.create_should_run_instance(),
    ):
        self.synced_float: SyncedFloat = synced_float
        self.should_run: Value = should_run

    def create_env(self):
        return ChangeableFactorRealtimeEnvironment(
            factor=self.synced_float, should_run=self.should_run
        )

    @classmethod
    def create_factor_instance(cls, factor=1.0) -> SyncedFloat:
        """ obtain a factor instance for sharing """
        return ChangeableFactorRealtimeEnvironment.create_factor_instance(factor=factor)
