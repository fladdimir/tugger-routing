from simpy import Environment

from tugger_src.gym_env.des_model.blocks.base_entity import BaseEntity


class ProductEntity(BaseEntity):
    """has a location (name), coordinates, and an icon which can be updated"""

    NUMBER_OF_ICONS = 9
    ICON_PATHS = [
        "tugger_src/gym_env/des_model/visualization/product/BT%s.png"
        % (i + 1)  # images go from 1 to 9
        for i in range(NUMBER_OF_ICONS)
    ]

    def __init__(self, env: Environment, name: str, location="", coordinates=(0, 0)):
        super().__init__(env, name)

        self.coordinates = coordinates
        self.icon_generator = self.create_icon_generator()

    def next_icon(self):
        self.process_animation_icon_path = next(self.icon_generator)

    def create_icon_generator(self):
        i = 0
        while True:
            yield self.ICON_PATHS[min(i, self.NUMBER_OF_ICONS - 1)]
            i += 1
