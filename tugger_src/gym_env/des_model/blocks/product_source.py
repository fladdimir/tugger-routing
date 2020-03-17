""" sets the entity icon path """
from typing import Optional, Type

from casymda.blocks import Entity
from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.block_components.block import Block

from tugger_src.gym_env.des_model.blocks.product_entity import ProductEntity


class ProductSource(VisualizableBlock):
    def __init__(
        self, env, name, xy=None, ways=None, entity_type: Type[Entity] = Entity
    ):
        super().__init__(env, name, xy=xy, ways=ways)

        self.entity_type = entity_type

        self.queuing = False  # disable queuing for this block

        self.entity_counter = 0

        self.env.process(self.create_one())  # create first
        self.do_on_exit_list.append(self.do_on_exit)

    def actual_processing(self, entity: ProductEntity):
        yield self.env.timeout(0)

    def create_one(self):
        self.entity_counter += 1
        entity = self.entity_type(self.env, "entity_" + str(self.entity_counter))

        entity.block_resource_request = self.block_resource.request()
        yield entity.block_resource_request
        self.env.process(self.process_entity(entity))

    def do_on_exit(
        self, entity: Entity, from_block: Optional[Block], to_Block: Optional[Block]
    ):
        self.env.process(self.create_one())
