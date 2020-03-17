from typing import Any, Optional

from casymda.blocks.tilemap.tilemap_movement import TilemapMovement
from simpy import Event

from tugger_src.gym_env.base.gym_helper import ActionHolder
from tugger_src.gym_env.des_model.blocks.tilemap_block import TilemapBlock
from tugger_src.gym_env.des_model.blocks.tugger_entity import TuggerEntity

SPEED = 10  # px/sec


class TuggerMovement(TilemapMovement, TilemapBlock):
    def __init__(
        self,
        env,
        name,
        xy=None,
        speed=SPEED,  # px / sec (sim-time)
        coordinates_holder=None,
        ways={},
    ):
        super().__init__(
            env,
            name,
            xy=xy,
            ways=ways,
            coordinates_holder=coordinates_holder,
            from_node=None,  # (evaluation overridden)
            to_node=None,
            speed=speed,
        )

        self.action_holder: Optional[ActionHolder] = None

    def actual_processing(self, entity: TuggerEntity):

        from_node = entity.location
        to_node = ""  # pre-initialization to make pyright happy

        if self.action_holder is None:
            to_node = self.coordinates_holder.get_random_location_name()
        else:
            # gym_env behavior
            self.action_holder.provided_action = Event(self.env)
            # this way the gym_env can run the simulation until an action is needed
            self.action_holder.action_needed.succeed()
            # consume provided action
            action = yield self.action_holder.provided_action
            to_node = self.coordinates_holder.get_location_name_by_index(action)

        (
            path_coords,
            overall_length,
        ) = self.coordinates_holder.get_path_coords_and_length_from_to(
            from_node, to_node
        )

        animation_loop: Any = None  # pre-initialization to make pyright happy
        if self.tilemap_visualizer is not None:
            animation_loop = self.env.process(
                self.animation_loop(entity, path_coords, destroy_on_arrival=False)
            )

        # set location to target, even though we did not arrive yet
        entity.location = to_node

        time_needed = overall_length / self.speed
        yield self.env.timeout(time_needed)

        if self.tilemap_visualizer is not None:
            animation_loop.interrupt()
