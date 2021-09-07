from typing import Any, Dict, List, Type

from casymda.blocks.block_components.block import Block


class ClientBlock:
    """interface for dependency injection of model blocks after instantiation of the model"""

    def auto_wire(self, blocks_dict: Dict[Type, List[Block]]):
        """receives dict of all block types of the model and a corresponding list of all instances"""
        raise NotImplementedError(
            "should have 'auto_wire' to implement the ClientBlock interface"
        )
