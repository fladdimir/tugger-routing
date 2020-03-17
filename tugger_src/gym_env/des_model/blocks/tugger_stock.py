# needs access to the product stations which it refills

from typing import Dict, List, Tuple, cast

from casymda.blocks.block_components.visualizable_block import VisualizableBlock
from simpy.core import Environment

from tugger_src.gym_env.des_model.blocks.product_station import ProductStation
from tugger_src.gym_env.des_model.blocks.tugger_entity import TuggerEntity


class TuggerStock(VisualizableBlock):

    FIXED_TIME = 5
    TIME_PER_RESOURCE_LOADED = 0
    MAX_AMOUNT_LOADED_PER_VISIT = 5

    def __init__(
        self,
        env: Environment,
        name: str,  # corresponds to the loaded resource
        block_capacity=float("inf"),
        xy: Tuple[int, int] = (0, 0),
        ways: Dict[str, List[Tuple[int, int]]] = {},
    ):
        super().__init__(env, name, block_capacity, xy, ways)

        self.location = self.name
        self.loaded_resource = self.name

    def actual_processing(self, entity: TuggerEntity):
        # load as much as possible of the provided resource
        loaded_resource = self.loaded_resource
        remaining_tugger_capacity = entity.get_remaining_overall_capacity()

        loaded_amount = min(remaining_tugger_capacity, self.MAX_AMOUNT_LOADED_PER_VISIT)

        yield self.env.timeout(
            self.FIXED_TIME + self.TIME_PER_RESOURCE_LOADED * loaded_amount
        )
        entity.load_resource(loaded_resource, loaded_amount)
