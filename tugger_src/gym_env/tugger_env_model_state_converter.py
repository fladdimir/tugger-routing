import copy
from typing import cast

import numpy as np
from casymda.blocks.block_components.state import States
from gym.spaces import Box, Space

from tugger_src.gym_env.base.gym_helper import ModelStateConverter
from tugger_src.gym_env.des_model.blocks.product_station import ProductStation
from tugger_src.gym_env.des_model.blocks.tugger_entity import TuggerEntity
from tugger_src.gym_env.des_model.model import Model, coordinates_holder

NUMBER_OF_OBSERVATIONS_PER_STATION = 5
NUMBER_OF_STATIONS = 9
NUMBER_OF_STOCKS = 2
NUMBER_OF_TUGGERS = 1
OBSERVATIONS_PER_TUGGER = NUMBER_OF_STOCKS + 1  # current load + current movement target
NUMBER_OF_TARGETS = NUMBER_OF_STATIONS + NUMBER_OF_STOCKS

NUMBER_OF_STATION_OBSERVATIONS = NUMBER_OF_OBSERVATIONS_PER_STATION * NUMBER_OF_STATIONS
stations_low = [0 for _ in range(NUMBER_OF_STATION_OBSERVATIONS)]
stations_high = [1 for _ in range(NUMBER_OF_STATION_OBSERVATIONS)]

NUMBER_OF_TUGGER_OBSERVATIONS = OBSERVATIONS_PER_TUGGER * NUMBER_OF_TUGGERS
tuggers_low = [0 for _ in range(NUMBER_OF_TUGGER_OBSERVATIONS)]
tugger_high = [1 for _ in range(NUMBER_OF_STOCKS)]
tugger_high.append(NUMBER_OF_TARGETS)
tuggers_high = copy.deepcopy(tugger_high)
for _ in range(NUMBER_OF_TUGGERS - 1):
    # extend for each extra tugger
    tuggers_high.extend(tugger_high)

NUMBER_OF_OBSERVATIONS = NUMBER_OF_STATION_OBSERVATIONS + NUMBER_OF_TUGGER_OBSERVATIONS

lows = stations_low + tuggers_low
highs = stations_high + tugger_high


class TuggerEnvModelStateConverter(ModelStateConverter):
    """converts TuggerEnv simulation model state to an observation matching the defined space"""

    observation_space = Box(low=np.array(lows), high=np.array(highs))

    def model_state_to_observation(self, model: Model) -> object:

        coordinates_holder = model.coordinates_holder

        observation = []

        # iterate over product-stations
        # be aware that the sorting stams from the model-file (parsed from bpmn)
        for product_station in model.blocks_dict[ProductStation]:
            ps = cast(ProductStation, product_station)
            inventory = min(ps.container.level, 10) / 10  # limit & norm
            busy = 1 if ps.processing_a_product else 0
            waiting_for_material = 1 if ps.waiting_for_material else 0
            empty = 1 if ps.state_manager._current_states[States.empty.value] else 0
            blocked_by_successor = (
                1 if ps.state_manager._current_states[States.blocked.value] else 0
            )

            observation += [
                inventory,
                busy,
                waiting_for_material,
                empty,
                blocked_by_successor,
            ]

        # iterate over tuggers
        # Multi-Tugger TODO: make sure that currently observed tugger is always last
        # (provide tugger id as part of the action_needed event)
        for tugger in model.tugger_source.tugger_entities:
            load = [l / TuggerEntity.CAPACITY_LIMIT for l in list(tugger.load.values())]
            target = [coordinates_holder.get_location_index_by_name(tugger.location)]
            # (tugger location is set by movement already on start)
            observation += load
            observation += target

        return np.array(observation)
