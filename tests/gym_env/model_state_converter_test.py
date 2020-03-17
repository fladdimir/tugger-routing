from typing import List, cast

from tugger_src.gym_env import tugger_env_model_state_converter
from tugger_src.gym_env.base.gym_helper import BaseEnvironmentFactory
from tugger_src.gym_env.des_model.blocks.tugger_entity import TuggerEntity
from tugger_src.gym_env.des_model.blocks.tugger_stock import TuggerStock
from tugger_src.gym_env.tugger_env import TuggerEnv


def test_space():
    assert (
        len(tugger_env_model_state_converter.tuggers_high)
        == tugger_env_model_state_converter.OBSERVATIONS_PER_TUGGER
        * tugger_env_model_state_converter.NUMBER_OF_TUGGERS
    )
    assert (
        len(tugger_env_model_state_converter.lows)
        == len(tugger_env_model_state_converter.highs)
        == tugger_env_model_state_converter.NUMBER_OF_OBSERVATIONS
    )


def test_initial():
    env_factory = BaseEnvironmentFactory()
    tugger_env = TuggerEnv(environment_factory=env_factory)
    obs = tugger_env.reset()
    obs = cast(List, obs)
    print(obs)

    # tugger unloaded, located at A
    assert len(obs) == 48  # 9*5 for stations, + 3 for tugger
    assert sum(obs) == 9  # 8 are empty, 1 is waiting for material (first one)

    # first station is third in the bpmn->model, to be sorted
    # waiting for material is before empty (i3 = 12 instead of 13)
    indices_to_be_1 = [3, 8, 12, 18, 23, 28, 33, 38, 43]
    for i in indices_to_be_1:
        assert obs[i] == 1


def test_move_to_1():
    env_factory = BaseEnvironmentFactory()
    tugger_env = TuggerEnv(environment_factory=env_factory)
    tugger_env.reset()

    move_to = 1
    obs, reward, done, info = tugger_env.step(move_to)
    obs = cast(List, obs)

    # target/reached_location is last
    assert obs[-1] == 1


def test_move_to_A_and_unload_at_T1():
    env_factory = BaseEnvironmentFactory()
    tugger_env = TuggerEnv(environment_factory=env_factory)
    tugger_env.reset()

    # tugger_env.model.movement.MAX_ANIMATION_TIMESTEP = 100
    # tugger_env.model.initialize_tkinter_tilemap_visualization()

    cooh = tugger_env.model.coordinates_holder

    # load A
    move_to = cooh.get_location_index_by_name("A")
    obs, reward, done, info = tugger_env.step(move_to)
    obs = cast(List, obs)

    # target/reached_location is last
    assert obs[-2] == 0  # no B loaded
    assert (
        obs[-3] == TuggerStock.MAX_AMOUNT_LOADED_PER_VISIT / TuggerEntity.CAPACITY_LIMIT
    )  # A loaded

    # move to T2 (A unloading not possible)
    move_to = cooh.get_location_index_by_name("T2")
    obs, reward, done, info = tugger_env.step(move_to)
    obs = cast(List, obs)
    assert obs[-2] == 0  # no B loaded
    assert (
        obs[-3] == TuggerStock.MAX_AMOUNT_LOADED_PER_VISIT / TuggerEntity.CAPACITY_LIMIT
    )  # A loaded

    # move to T1 (A unloading possible)
    T1 = cooh.get_location_index_by_name("T1")
    T1_i = 2  # blocks_dict
    obs, reward, done, info = tugger_env.step(T1)
    obs = cast(List, obs)
    assert obs[-2] == 0  # no B loaded
    assert obs[-3] == 0  # A unloaded
    assert (
        obs[T1_i * 5] == (5 - 1.5) / 10
    )  # station inventory, max 10 normalized, 1.5/5 used
    # station status
    assert obs[T1_i * 5 + 1] == 1  # busy
    assert obs[T1_i * 5 + 2] == 0  # waiting
    assert obs[T1_i * 5 + 3] == 0  # empty
    assert obs[T1_i * 5 + 3] == 0  # blocked

    now = tugger_env.model.env.now
    # wait until processing is done 2x, so that the first station should be blocked by its successor
    for _ in range(25):
        obs, reward, done, info = tugger_env.step(T1)
    assert tugger_env.model.env.now - now > 120  # processing happened

    obs, reward, done, info = tugger_env.step(T1)

    # check status
    obs = cast(List, obs)
    assert obs[-2] == 0  # no B loaded
    assert obs[-3] == 0  # A unloaded

    # station status
    assert (
        obs[T1_i * 5] == (5 - 3) / 10
    )  # station inventory, max 10 normalized, 3/5 used
    assert obs[T1_i * 5 + 1] == 0  # busy
    assert obs[T1_i * 5 + 2] == 0  # waiting
    assert obs[T1_i * 5 + 3] == 0  # empty
    assert obs[T1_i * 5 + 4] == 1  # blocked

    T2_i = 0
    assert obs[T2_i * 5 + 0] == 0  # inventory
    assert obs[T2_i * 5 + 1] == 0  # busy
    assert obs[T2_i * 5 + 2] == 1  # waiting
    assert obs[T2_i * 5 + 3] == 0  # empty
    assert obs[T2_i * 5 + 4] == 0  # blocked
