from tugger_src.gym_env.des_model.visualization.tugger_tilemap_visualizer import (
    TuggerTilemapVisualizer,
)
from typing import Optional


class TilemapBlock:
    """ qualifies for injection of a tilemap visualizer """

    def __init__(self):
        self.tilemap_visualizer: Optional[TuggerTilemapVisualizer]
