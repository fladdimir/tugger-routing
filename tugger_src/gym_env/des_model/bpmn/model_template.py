"""model template for generated model files"""
from tkinter import Tk
from typing import Any, Dict, List, Type, cast

from casymda.blocks import RoundRobinGateway
from casymda.blocks.block_components.block import Block
from casymda.blocks.block_components.visualizable_block import VisualizableBlock
from casymda.visualization.canvas.scaled_canvas import ScaledCanvas
from casymda.visualization.canvas.tk_canvas import ScaledCanvasTk
from casymda.visualization.canvas.web_canvas import WebCanvas
from casymda.visualization.process_visualizer import ProcessVisualizer
from numpy.core.shape_base import block
from simpy import Environment

from tugger_src.gym_env.base.gym_helper import BaseModel
from tugger_src.gym_env.des_model.blocks import (
    ProductEntity,
    ProductSink,
    ProductSource,
    ProductStation,
    TuggerGateway,
    TuggerMovement,
    TuggerSource,
    TuggerStation,
    TuggerStock,
)
from tugger_src.gym_env.des_model.blocks.client_block import ClientBlock
from tugger_src.gym_env.des_model.blocks.tilemap_block import TilemapBlock
from tugger_src.gym_env.des_model.tilemap import coordinates_holder_setup
from tugger_src.gym_env.des_model.visualization.tugger_tilemap_visualizer import (
    TuggerTilemapVisualizer,
)

coordinates_holder = coordinates_holder_setup.get_coordinates_holder()


class Model(BaseModel):
    """generated model"""

    def __init__(self, env: Environment):

        self.env = env  # simpy env
        self.coordinates_holder = coordinates_holder

        self.model_components: Any
        self.model_graph_names: Dict[str, List[str]]

        #!resources+components

        #!model

        # translate model_graph_names into corresponding objects

        self.model_blocks = cast(Dict[str, Block], self.model_components)

        self.model_graph: Dict[Block, List[Block]] = {
            self.model_components[name]: [
                self.model_components[nameSucc]
                for nameSucc in self.model_graph_names[name]
            ]
            for name in self.model_graph_names
        }

        for block in self.model_graph:
            block.successors = self.model_graph[block]

        # injection of dependencies:
        blocks_dict: Dict[Type, List[Block]] = {}
        for block in self.model_graph:
            block_type = type(block)
            if block_type not in blocks_dict:
                blocks_dict[block_type] = []
            blocks_dict[block_type].append(block)

        for block in self.model_graph:
            if isinstance(block, ClientBlock):
                b = cast(ClientBlock, block)
                b.auto_wire(blocks_dict)
        # save for later use:
        self.blocks_dict = blocks_dict

    # process visualization
    def initialize_tkinter_process_visualization(
        self, flow_speed=200
    ) -> ScaledCanvasTk:
        tk = Tk()
        scale = 1.0
        width = 1628 * scale
        height = 529 * scale
        canvas = ScaledCanvasTk(tk, width, height, scale=scale)
        self.initialize_process_visualizer(canvas, flow_speed=flow_speed)
        return canvas

    def initialize_web_canvas_process_visualization(
        self, shared_state: dict, width: int, height: int, flow_speed=200
    ):
        canvas = WebCanvas(shared_state, width, height)
        self.initialize_process_visualizer(canvas, flow_speed=flow_speed)

    def initialize_process_visualizer(self, canvas: ScaledCanvas, flow_speed=200):
        process_visualizer = ProcessVisualizer(
            canvas,
            flow_speed=flow_speed,
            background_image_path="tugger_src/gym_env/des_model/visualization/model.png",
            default_entity_icon_path="tugger_src/gym_env/des_model/visualization/simple_entity_icon.png",
        )
        for block in self.model_graph:
            if isinstance(block, VisualizableBlock):
                block.visualizer = process_visualizer

    # tilemap visualization
    def initialize_tkinter_tilemap_visualization(self) -> ScaledCanvasTk:
        tk = Tk()
        width = 652
        height = 928
        canvas = ScaledCanvasTk(tk, width, height)
        self.initialize_tilemap_visualizer(canvas)
        return canvas

    def initialize_web_canvas_tilemap_visualization(
        self, shared_state: dict, width: int, height: int
    ):
        canvas = WebCanvas(shared_state, width, height)
        self.initialize_tilemap_visualizer(canvas)

    def initialize_tilemap_visualizer(self, canvas):
        tilemap_visualizer = TuggerTilemapVisualizer(
            canvas,
            background_image_path="tugger_src/gym_env/des_model/visualization/layout.png",
            default_entity_icon_path="tugger_src/gym_env/des_model/visualization/simple_entity_icon.png",
        )
        for block in self.model_graph:
            if isinstance(block, TilemapBlock):
                b = cast(TilemapBlock, block)
                b.tilemap_visualizer = tilemap_visualizer
