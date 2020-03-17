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

        self.source = ProductSource(
            self.env,
            "source",
            xy=(66, 57),
            entity_type=ProductEntity,
            ways={"T1": [(84, 57), (210, 57)]},
        )

        self.tugger_source = TuggerSource(
            self.env,
            "tugger_source",
            xy=(1439, 32),
            location="A",
            ways={"movement": [(1439, 50), (1439, 88)]},
        )

        self.sink = ProductSink(self.env, "sink", xy=(66, 463), ways={})

        self.T2 = ProductStation(
            self.env,
            "T2",
            xy=(519, 57),
            consumed_resource="B",
            coordinates_holder=coordinates_holder,
            consumed_per_product=0.5,
            ways={"T3": [(569, 57), (718, 57)]},
        )

        self.T3 = ProductStation(
            self.env,
            "T3",
            xy=(768, 57),
            consumed_resource="A",
            coordinates_holder=coordinates_holder,
            consumed_per_product=1.5,
            ways={"T4": [(818, 57), (945, 57)]},
        )

        self.T1 = ProductStation(
            self.env,
            "T1",
            xy=(260, 57),
            consumed_resource="A",
            coordinates_holder=coordinates_holder,
            consumed_per_product=1.5,
            ways={"T2": [(310, 57), (469, 57)]},
        )

        self.T8 = ProductStation(
            self.env,
            "T8",
            xy=(519, 463),
            consumed_resource="B",
            coordinates_holder=coordinates_holder,
            consumed_per_product=0.5,
            ways={"T9": [(469, 463), (310, 463)]},
        )

        self.T9 = ProductStation(
            self.env,
            "T9",
            xy=(260, 463),
            consumed_resource="A",
            coordinates_holder=coordinates_holder,
            consumed_per_product=1.5,
            ways={"sink": [(210, 463), (84, 463)]},
        )

        self.movement = TuggerMovement(
            self.env,
            "movement",
            xy=(1439, 128),
            coordinates_holder=coordinates_holder,
            ways={"gateway": [(1439, 168), (1439, 209)]},
        )

        self.T7 = ProductStation(
            self.env,
            "T7",
            xy=(768, 463),
            consumed_resource="A",
            coordinates_holder=coordinates_holder,
            consumed_per_product=1.5,
            ways={"T8": [(718, 463), (569, 463)]},
        )

        self.T5 = ProductStation(
            self.env,
            "T5",
            xy=(1087, 232),
            consumed_resource="A",
            coordinates_holder=coordinates_holder,
            consumed_per_product=1.5,
            ways={"T6": [(1087, 272), (1087, 463), (1045, 463)]},
        )

        self.T4 = ProductStation(
            self.env,
            "T4",
            xy=(995, 57),
            consumed_resource="B",
            coordinates_holder=coordinates_holder,
            consumed_per_product=0.5,
            ways={"T5": [(1045, 57), (1087, 57), (1087, 192)]},
        )

        self.T6 = ProductStation(
            self.env,
            "T6",
            xy=(995, 463),
            consumed_resource="B",
            coordinates_holder=coordinates_holder,
            consumed_per_product=0.5,
            ways={"T7": [(945, 463), (818, 463)]},
        )

        self.A = TuggerStock(
            self.env,
            "A",
            xy=(1253, 336),
            ways={"union": [(1253, 376), (1253, 439), (1414, 439)]},
        )

        self.T = TuggerStation(
            self.env,
            "T",
            xy=(1523, 336),
            ways={"union": [(1523, 376), (1523, 439), (1464, 439)]},
        )

        self.B = TuggerStock(
            self.env,
            "B",
            xy=(1374, 336),
            ways={"union": [(1374, 376), (1374, 439), (1414, 439)]},
        )

        self.gateway = TuggerGateway(
            self.env,
            "gateway",
            xy=(1439, 234),
            ways={
                "A": [(1414, 234), (1253, 234), (1253, 296)],
                "T": [(1464, 234), (1523, 234), (1523, 296)],
                "B": [(1414, 234), (1374, 234), (1374, 296)],
            },
        )

        self.union = RoundRobinGateway(
            self.env,
            "union",
            xy=(1439, 439),
            ways={
                "movement": [
                    (1439, 464),
                    (1439, 497),
                    (1596, 497),
                    (1596, 128),
                    (1489, 128),
                ]
            },
        )

        #!model

        self.model_components = {
            "source": self.source,
            "tugger_source": self.tugger_source,
            "sink": self.sink,
            "T2": self.T2,
            "T3": self.T3,
            "T1": self.T1,
            "T8": self.T8,
            "T9": self.T9,
            "movement": self.movement,
            "T7": self.T7,
            "T5": self.T5,
            "T4": self.T4,
            "T6": self.T6,
            "A": self.A,
            "T": self.T,
            "B": self.B,
            "gateway": self.gateway,
            "union": self.union,
        }

        self.model_graph_names = {
            "source": ["T1"],
            "tugger_source": ["movement"],
            "sink": [],
            "T2": ["T3"],
            "T3": ["T4"],
            "T1": ["T2"],
            "T8": ["T9"],
            "T9": ["sink"],
            "movement": ["gateway"],
            "T7": ["T8"],
            "T5": ["T6"],
            "T4": ["T5"],
            "T6": ["T7"],
            "A": ["union"],
            "T": ["union"],
            "B": ["union"],
            "gateway": ["A", "T", "B"],
            "union": ["movement"],
        }
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
