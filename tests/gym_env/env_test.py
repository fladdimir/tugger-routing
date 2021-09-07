""" basic tests for the defined env """
import random

import stable_baselines3.common.env_checker
from tugger_src.gym_env.base.gym_helper import RealtimeEnvironmentFactory
from tugger_src.gym_env.tugger_env import TuggerEnv


def test_with_stable_baselines_gym_env_checker():
    env = TuggerEnv()
    stable_baselines3.common.env_checker.check_env(env)


def test_that_tugger_env_can_be_instantiated():
    tugger_env = TuggerEnv()
    assert tugger_env is not None


def test_that_model_can_be_initialized():
    tugger_env = TuggerEnv()
    tugger_env.reset()
    assert tugger_env.model is not None


def test_that_model_can_be_executed_with_random_action(number_of_steps=1000):
    tugger_env = TuggerEnv()
    tugger_env.reset()

    available_actions = [i for i in range(tugger_env.NUMBER_OF_ACTIONS)]

    for _ in range(number_of_steps):
        action = random.choice(available_actions)
        tugger_env.step(action)

    model = tugger_env.model
    assert model.movement.overall_count_in == number_of_steps + 1
    # (first enter is part of the reset)
    assert (
        model.sink.overall_count_in == tugger_env.reward_holder.accumulated_reward_raw
    )


def test_env_with_multiple_episodes(number_of_episodes=3, time_to_be_done=100):
    tugger_env = TuggerEnv()
    tugger_env.TIME_TO_BE_DONE = time_to_be_done

    rewards = []
    for _ in range(number_of_episodes):
        tugger_env.reset()
        done = False
        episode_reward = 0
        while not done:
            obs, step_reward, done, info = tugger_env.step(0)
            episode_reward += step_reward
        rewards.append(episode_reward)

    for r in rewards:
        assert r == rewards[0]


def _env_execution_with_tilemap_visualization_and_realtime_env(number_of_steps=10):
    # def test_env_execution_with_tilemap_visualization_and_realtime_env(number_of_steps=10):
    # does not end for some reason (mac), might be related to realtime env
    synced_float = RealtimeEnvironmentFactory.create_factor_instance(factor=1 / 86400)
    rt_env_factory = RealtimeEnvironmentFactory(synced_float=synced_float)
    tugger_env = TuggerEnv(environment_factory=rt_env_factory)
    tugger_env.reset()

    model = tugger_env.model

    canvas = model.initialize_tkinter_tilemap_visualization()

    available_actions = [i for i in range(tugger_env.NUMBER_OF_ACTIONS)]
    for _ in range(number_of_steps):
        action = random.choice(available_actions)
        tugger_env.step(action)

    canvas.tk_gui.destroy()

    assert model.movement.overall_count_in == number_of_steps + 1
    # (first enter is part of the reset)
