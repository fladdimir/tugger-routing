from typing import Dict, List, Tuple, Type, cast

from casymda.blocks.block_components.block import Block
from casymda.blocks.block_components.visualizable_block import VisualizableBlock
from simpy.core import Environment

from tugger_src.gym_env.des_model.blocks.client_block import ClientBlock
from tugger_src.gym_env.des_model.blocks.product_station import ProductStation
from tugger_src.gym_env.des_model.blocks.tugger_entity import TuggerEntity


class TuggerStation(VisualizableBlock, ClientBlock):
    """ unloads the tugger at its current location and refills the corresponding product_station """

    FIXED_TIME = 5
    TIME_PER_RESOURCE_UNLOADED = 0
    MAX_UNLOADED_AMOUNT_PER_VISIT = 5

    def __init__(
        self,
        env: Environment,
        name: str,
        block_capacity=float("inf"),
        xy: Tuple[int, int] = (0, 0),
        ways: Dict[str, List[Tuple[int, int]]] = {},
    ):
        super().__init__(env, name, block_capacity, xy, ways)

        # mapping of possible entity locations to ProductStations
        self.product_stations: Dict[str, ProductStation] = {}  # injected

    def actual_processing(self, entity: TuggerEntity):
        product_station = self.product_stations[entity.location]

        consumed_resource = product_station.consumed_resource
        remaining_station_capacity = (
            product_station.container.capacity - product_station.container.level
        )

        loaded_resource_amount = entity.load[consumed_resource]
        unloaded_amount = min(
            loaded_resource_amount,
            remaining_station_capacity,
            self.MAX_UNLOADED_AMOUNT_PER_VISIT,
        )

        yield self.env.timeout(
            self.FIXED_TIME + self.TIME_PER_RESOURCE_UNLOADED * unloaded_amount
        )
        entity.unload_resource(consumed_resource, unloaded_amount)
        product_station.refill(unloaded_amount)

    def auto_wire(self, blocks_dict: Dict[Type, List[Block]]):
        ps_list = blocks_dict[ProductStation]
        ps_list = cast(List[ProductStation], ps_list)
        self._post_init(ps_list)

    def _post_init(self, product_stations: List[ProductStation] = []):
        self.product_stations = {ps.location: ps for ps in product_stations}
