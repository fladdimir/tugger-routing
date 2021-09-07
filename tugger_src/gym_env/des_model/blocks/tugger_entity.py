""" extends entity by its current location """


from tugger_src.gym_env.des_model.blocks.tilemap_block import TilemapBlock
from typing import Dict, List

from simpy import Environment

from tugger_src.gym_env.des_model.blocks.base_entity import BaseEntity

TEXT_COORDINATES = (550, 800)


class TuggerEntity(BaseEntity):

    ICON_PATH_LIST = {
        "empty": "tugger_src/gym_env/des_model/visualization/tugger/empty.png",
        "loaded": "tugger_src/gym_env/des_model/visualization/tugger/loaded.png",
    }

    CAPACITY_LIMIT = 25

    def __init__(
        self,
        env: Environment,
        name: str,
        location="",
        source: TilemapBlock = None,
        resource_types: List[str] = [],
    ):
        super().__init__(env, name, location=location)

        self.capacity = self.CAPACITY_LIMIT
        self.source = source
        self.text_coordinates = TEXT_COORDINATES

        self.load: Dict[str, float] = {rt: float(0) for rt in resource_types}

    def set_icon(self, status: str):
        self.process_animation_icon_path = self.ICON_PATH_LIST[status]

    def determine_icon_state(self):
        if self.is_empty():
            self.set_icon_empty()
        else:
            self.set_icon_loaded()
        self.update_text()

    def set_icon_empty(self):
        self.set_icon("empty")

    def set_icon_loaded(self):
        self.set_icon("loaded")

    def update_text(self):
        if self.source.tilemap_visualizer is not None:
            self.source.tilemap_visualizer.animate_text(
                self.name,
                self.text_coordinates,
                (self.name + "\n" + self.get_load_text()),
                anchor="nw",
            )

    def get_load_text(self) -> str:
        """return new-line separated text of currently loaded amounts"""
        return "\n".join(["%s: %s" % (load, self.load[load]) for load in self.load])

    def load_resource(self, resource: str, amount: float):
        remaining_capacity = self.capacity - self.load[resource]
        if remaining_capacity < amount:
            raise Exception(
                "cannot load %s of %s, remaining capacity: %s"
                % (amount, resource, remaining_capacity)
            )
        else:
            self.load[resource] += amount
            self.determine_icon_state()

    def unload_resource(self, resource: str, amount: float):
        if self.load[resource] - amount < 0:
            raise Exception(
                "cannot unload %s of %s, remaining load: %s"
                % (amount, resource, self.load[resource])
            )
        else:
            self.load[resource] -= amount
            self.determine_icon_state()

    def is_empty(self) -> bool:
        return sum(self.load.values()) <= 0

    def get_remaining_overall_capacity(self) -> float:
        return self.capacity - sum(self.load.values())
