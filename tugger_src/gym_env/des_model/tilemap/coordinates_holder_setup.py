from casymda.blocks.tilemap.coordinates_holder import CoordinatesHolder, delete_cached

CSV_FILE = "tugger_src/gym_env/des_model/tilemap/layout.csv"
SCALE = 10  # px / tile
INCLUDE_DIAGONAL = True


def get_coordinates_holder():
    """gets called before model instantiation to provide the coordinates_holder"""
    return CoordinatesHolder(CSV_FILE, scale=SCALE, include_diagonal=INCLUDE_DIAGONAL)


if __name__ == "__main__":
    delete_cached(CSV_FILE)
