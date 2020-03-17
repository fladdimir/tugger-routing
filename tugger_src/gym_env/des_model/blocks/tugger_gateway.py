"""gateway"""
from tugger_src.gym_env.des_model.blocks.client_block import ClientBlock
from typing import Any, Dict, List, Type

from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.block_components.block import Block

from tugger_src.gym_env.des_model.blocks.product_station import ProductStation
from tugger_src.gym_env.des_model.blocks.tugger_entity import TuggerEntity
from tugger_src.gym_env.des_model.blocks.tugger_station import TuggerStation
from tugger_src.gym_env.des_model.blocks.tugger_stock import TuggerStock


class TuggerGateway(VisualizableBlock, ClientBlock):
    """chooses successor depending on a tuggers location"""

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

        self.location_to_successor: Dict[str, Block]

    def actual_processing(self, entity):
        yield self.env.timeout(0)

    def find_successor(self, entity: TuggerEntity):
        return self.location_to_successor[entity.location]

    def auto_wire(self, type_dict: Dict[Type, List[Any]]):
        # partially typed wiring of block dependencies
        self._post_init(
            type_dict[TuggerStock],
            type_dict[ProductStation],
            type_dict[TuggerStation][0],
        )

    def _post_init(
        self,
        tugger_stocks: List[TuggerStock],
        product_stations: List[ProductStation],
        tugger_station: TuggerStation,
    ):
        self.location_to_successor = {}

        for ps in product_stations:
            # each product_stations' location should point to the tugger_station
            self.location_to_successor[ps.location] = tugger_station
        for ts in tugger_stocks:
            self.location_to_successor[ts.location] = ts
