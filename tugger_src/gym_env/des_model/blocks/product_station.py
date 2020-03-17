""" a station processes a product when a sufficient amount of resources is present """

from casymda.blocks.block_components.block import Block
from casymda.blocks.entity import Entity
from tugger_src.gym_env.des_model.visualization.tugger_tilemap_visualizer import (
    TuggerTilemapVisualizer,
)
from tugger_src.gym_env.des_model.blocks.tilemap_block import TilemapBlock
from typing import Dict, List, Optional, Tuple, cast

from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.tilemap.coordinates_holder import CoordinatesHolder
from simpy import Container, Environment

from tugger_src.gym_env.des_model.blocks.product_entity import ProductEntity


class ProductStation(VisualizableBlock, TilemapBlock):

    PROCESSING_TIME = 60

    def __init__(
        self,
        env: Environment,
        name: str,
        consumed_resource: str,
        coordinates_holder: CoordinatesHolder,
        consumed_per_product=1,
        block_capacity=1,
        xy: Tuple[int, int] = (0, 0),
        ways: Dict[str, List[Tuple[int, int]]] = {},
    ):
        super().__init__(env, name, block_capacity, xy, ways)

        self.coordinates_holder = coordinates_holder
        self.container = Container(
            self.env, float("inf"), init=0
        )  # (a limited capacity here can cause deadlocks due to impossible unloading of loaded resources)

        self.consumed_resource = consumed_resource

        self.location = self.name
        self.coordinates = cast(
            Tuple[float, float], self.coordinates_holder.get_coords(self.location)
        )
        # slight offset to the right:
        self.text_coordinates = cast(
            Tuple[float, float], (self.coordinates[0] + 80, self.coordinates[1] + 50)
        )

        self.consumed_per_product = consumed_per_product

        self.tilemap_visualizer: Optional[TuggerTilemapVisualizer] = None

        self.do_on_enter_list.append(self.animate_entity_on_enter)

        # additional states for observation:
        self.waiting_for_material = False
        self.processing_a_product = False

    def refill(self, by: float):
        if by > 0:
            # simpy raises an error if amount is <= 0
            self.container.put(by)
        self.animate_level()

    def animate_level(self):
        if self.tilemap_visualizer is not None:
            self.tilemap_visualizer.animate_text(
                self.name,
                self.text_coordinates,
                (
                    "%s - %s: %s"
                    % (self.name, self.consumed_resource, self.container.level)
                ),
            )

    def animate_entity(self, entity: ProductEntity):
        if self.tilemap_visualizer is not None:
            self.tilemap_visualizer.animate(entity, *entity.coordinates, self.env.now)

    def destroy_and_animate_entity(self, entity: ProductEntity):
        if self.tilemap_visualizer is not None:
            self.tilemap_visualizer.destroy(entity)
            self.animate_entity(entity)

    def actual_processing(self, entity: ProductEntity):
        # assume block capacity of 1 entity at a time
        self.waiting_for_material = True
        yield self.container.get(self.consumed_per_product)
        self.waiting_for_material = False
        self.animate_level()

        self.processing_a_product = True
        yield self.env.timeout(self.PROCESSING_TIME)
        self.processing_a_product = False

    def animate_entity_on_enter(
        self, entity: Entity, from_block: Optional[Block], to_block: Optional[Block],
    ):
        # animation on enter
        e = cast(ProductEntity, entity)
        e.coordinates = self.coordinates
        e.location = self.location
        e.next_icon()
        self.destroy_and_animate_entity(e)
