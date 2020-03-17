from typing import Tuple
from casymda.blocks.entity import Entity
from simpy import Environment


class BaseEntity(Entity):
    def __init__(self, env: Environment, name: str, location=""):
        super().__init__(env, name)

        self.location = location
