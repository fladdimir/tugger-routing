""" increase reward on product exit """
import logging
from typing import Optional

from casymda.blocks import Entity, Sink
from casymda.blocks.block_components.block import Block
from casymda.visualization.tilemap.tilemap_visualizer import TilemapVisualizer

from tugger_src.gym_env.base.gym_helper import RewardHolder
from tugger_src.gym_env.des_model.blocks.tilemap_block import TilemapBlock


REWARD_PER_FINISHED_PRODUCT = 1


class ProductSink(Sink, TilemapBlock):
    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

        self.reward_holder: Optional[RewardHolder] = None

        self.tilemap_visualizer: Optional[TilemapVisualizer] = None

        self.do_on_exit_list.append(self.do_on_exit)

    def do_on_exit(
        self, entity: Entity, from_block: Optional[Block], to_Block: Optional[Block]
    ):
        if self.reward_holder is not None:
            self.reward_holder.increase_step_reward(REWARD_PER_FINISHED_PRODUCT)
        if self.tilemap_visualizer is not None:
            self.tilemap_visualizer.destroy(entity)
