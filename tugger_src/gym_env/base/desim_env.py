from typing import Tuple

from gym.core import Env
from gym.spaces import Space
from simpy import Event

from tugger_src.gym_env.base.gym_helper import (
    ActionHolder,
    BaseModel,
    ModelStateConverter,
    RewardHolder,
)


class DESimEnv(Env):
    """abstract base-wrapper for casymda-models as gym environment,
    to be extended for simulation model-specific configuration"""

    model: BaseModel
    action_holder: ActionHolder

    def __init__(
        self,
        action_space: Space,
        observation_space: Space,
        model_state_converter: ModelStateConverter,
    ) -> None:

        self.action_space = action_space
        self.observation_space = observation_space
        self.model_state_converter = model_state_converter

        self.reward_holder = RewardHolder()
        self.finished_gym_steps_in_current_episode = 0
        self.time_of_last_step = 0
        self.finished_episodes = 0
        self.finished_gym_steps_overall = 0

    """interface methods: step, reset, render"""

    def step(self, action: object) -> Tuple[object, float, bool, dict]:
        """takes action and executes simulation until next action is needed"""

        # 1. preparation
        self.reward_holder.reset_step_reward()

        # provide action via event
        self.action_holder.provided_action.succeed(action)
        self.action_holder.action_needed = Event(self.model.env)

        # 2. run model
        self.model.env.run(until=self.action_holder.action_needed)
        self.finished_gym_steps_in_current_episode += 1

        # 3. collect information to return to agent
        done = self.check_if_model_is_done()

        # enable time-dependent rewards
        time_needed_for_step = self.model.env.now - self.time_of_last_step
        reward = self.get_reward(time_needed_for_step, done)
        self.time_of_last_step = self.model.env.now

        observation = self._get_observation()
        info = self.get_info()

        if done:
            self.finished_episodes += 1
        self.finished_gym_steps_overall += 1

        return (observation, reward, done, info)

    def reset(self) -> object:
        """resets env and simulation model and return initial observation"""
        self.before_reset()

        self._initialize_model()

        # run until the first action is needed
        self.action_holder.action_needed = Event(self.model.env)
        self.model.env.run(until=self.action_holder.action_needed)

        initial_observation = self._get_observation()
        return initial_observation

    def render(self, mode=None):
        """des-model animation is controlled via sim env visualizer"""
        pass

    # helper methods:

    def _get_observation(self) -> object:
        """transform the current state of the simulation model into a gym-observation"""
        observation = self.model_state_converter.model_state_to_observation(self.model)
        return observation

    def _initialize_model(self):
        """initialize the des-model during reset"""
        self.finished_gym_steps_in_current_episode = 0
        self.time_of_last_step = 0

        self.setup_sim()  # model-specific setup
        assert self.model is not None  # to be set by child class code

        self.reward_holder = RewardHolder()
        self.action_holder = ActionHolder()

        self.initialize_action_and_reward_holder()

    # methods which might be useful to be overridden:

    def get_reward(self, time_needed_for_step: int, done: bool) -> float:
        """return reward of the last step, override for optional additional reward calculation,
        reward could depend on the time_needed_for_step or whether the episode is done"""
        collected_reward = self.reward_holder.step_reward
        self.reward_holder.increase_accumulated_reward(by=collected_reward)
        return collected_reward

    def get_info(self) -> dict:
        """returns empty dict by default"""
        return {}

    def before_reset(self):
        """called first by reset()"""
        pass

    # abstract methods to be defined by child class:

    def setup_sim(self):
        """set "model" instance variable"""
        raise NotImplementedError()

    def initialize_action_and_reward_holder(self):
        """wire action_holder and reward_holder where needed by the model"""
        raise NotImplementedError()

    def check_if_model_is_done(self) -> bool:
        """check defined criterium for the end of an episode here"""
        raise NotImplementedError()
