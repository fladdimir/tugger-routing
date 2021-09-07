from casymda.blocks.block_components.visualizable_block import VisualizableBlock
from tugger_src.gym_env.des_model.visualization.tugger_tilemap_visualizer import (
    TuggerTilemapVisualizer,
)
from typing import Dict, List, Optional, Type, cast

from casymda.blocks.block_components.block import Block

from tugger_src.gym_env.des_model.blocks.client_block import ClientBlock
from tugger_src.gym_env.des_model.blocks.tilemap_block import TilemapBlock
from tugger_src.gym_env.des_model.blocks.tugger_entity import TuggerEntity
from tugger_src.gym_env.des_model.blocks.tugger_stock import TuggerStock


class TuggerSource(VisualizableBlock, ClientBlock, TilemapBlock):

    NUMBER_OF_TUGGERS = 1

    def __init__(self, env, name, xy=None, ways=None, location="unset"):

        super().__init__(env, name, xy=xy, ways=ways)

        self.location = location
        self.tugger_entities: List[TuggerEntity] = []
        self.resource_types: List[str] = []
        self.tilemap_visualizer: Optional[TuggerTilemapVisualizer] = None

        self.max_entities = self.NUMBER_OF_TUGGERS
        self.inter_arrival_time = 0
        self.entity_counter = 0
        self.entity_type = TuggerEntity

        self.env.process(self.creation_loop())

    def creation_loop(self):
        """create entities as needed"""
        for i in range(self.max_entities):

            self.entity_counter += 1
            entity = self.entity_type(
                self.env,
                "trolley_" + str(self.entity_counter),
                location=self.location,
                source=self,
                resource_types=self.resource_types,
            )
            self.tugger_entities.append(entity)

            entity.block_resource_request = self.block_resource.request()
            yield entity.block_resource_request

            self.env.process(self.process_entity(entity))

            if i < self.max_entities - 1:
                yield self.env.timeout(self.inter_arrival_time)

    def actual_processing(self, entity: TuggerEntity):
        yield self.env.timeout(0)

        entity.determine_icon_state()
        entity.update_text()

    def auto_wire(self, blocks_dict: Dict[Type, List[Block]]):
        for t in blocks_dict[TuggerStock]:
            ts = cast(TuggerStock, t)
            self.resource_types.append(ts.loaded_resource)
