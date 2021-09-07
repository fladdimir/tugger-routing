from typing import Dict, Tuple, cast
from casymda.visualization.canvas.scaled_canvas import ScaledCanvas
from casymda.visualization.tilemap.tilemap_visualizer import TilemapVisualizer


class TuggerTilemapVisualizer(TilemapVisualizer):
    """casymda tilemap visualizer with additional text visualization methods"""

    def __init__(
        self,
        canvas: ScaledCanvas,
        background_image_path: str = "",
        default_entity_icon_path: str = "",
    ):
        super().__init__(
            canvas,
            background_image_path=background_image_path,
            default_entity_icon_path=default_entity_icon_path,
        )

        self.texts: Dict[str, Text] = {}
        # (maps owner name - assumed to be unique - and its text)

    def animate_text(
        self, key: str, coordinates: Tuple[float, float], text: str, anchor="se"
    ):
        """write the text to canvas"""
        if key not in self.texts:
            self.texts[key] = Text(self.canvas, coordinates, text, anchor)
        self.texts[key].update_text(coordinates, text)


class Text:
    """helper class for text management"""

    def __init__(
        self,
        canvas: ScaledCanvas,
        coordinates: Tuple[float, float],
        text_value: str,
        anchor: str,
    ) -> None:
        self.canvas = canvas
        self.coordinates = self.coordinates_to_int(coordinates)
        self.text_value = text_value
        self._text = cast(
            int,
            canvas.create_text(
                *(self.coordinates), text=self.text_value, anchor=anchor
            ),
        )

    def update_text(self, coordinates: Tuple[float, float], text_value: str):
        if self.text_value == text_value:
            return
        self.coordinates = self.coordinates_to_int(coordinates)
        self.text_value = text_value
        self.canvas.set_coords(self._text, self.coordinates)
        self.canvas.set_text_value(self._text, self.text_value)

    def coordinates_to_int(self, coordinates: Tuple[float, float]):
        return tuple(map(int, coordinates))
