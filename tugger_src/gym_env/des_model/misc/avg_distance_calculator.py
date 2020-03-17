""" helper for logistics system analysis, calculates weighted average distances """

from simpy import Environment

from tugger_src.gym_env.des_model.blocks.product_station import ProductStation
from tugger_src.gym_env.des_model.blocks.tugger_source import TuggerSource
from tugger_src.gym_env.des_model.model import Model

model = Model(Environment())

coordinates_holder = model.coordinates_holder

location_names_list = [
    coordinates_holder.get_location_name_by_index(i) for i in range(0, 11)
]
print("\nlocations:")
print(location_names_list)
# ['A', 'B', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
print("\ndistance units (px)")

sources = model.blocks_dict[TuggerSource]
sources = sorted(sources, key=lambda b: b.name)

stations = model.blocks_dict[ProductStation]
stations = sorted(stations, key=lambda b: b.name)

# e.g. "T1" : 1.5
station_consumptions = {
    station.name: station.consumed_per_product for station in stations
}
avg_consumption_per_product_per_station = sum(station_consumptions.values()) / len(
    station_consumptions
)
print(
    "\navg resource consumption / product per station: "
    + str(avg_consumption_per_product_per_station)
)
station_weightings = {
    station.name: station.consumed_per_product / avg_consumption_per_product_per_station
    for station in stations
}


def calc_weighted_distances_between_stations_and_sources():
    distances = []
    print("\nsimple / weighted distances:")
    for station in stations:
        source_name = station.consumed_resource
        _, length = coordinates_holder.get_path_coords_and_length_from_to(
            source_name, station.name
        )
        weighting = station.consumed_per_product
        # (more frequent moves due to higher demand)
        distances.append(length * weighting)
        print(
            "|" + source_name,
            station.name + " | %.2fm | %.2fm|" % (length, length * weighting),
            sep=" -> ",
        )
    return distances


weighted_distances = calc_weighted_distances_between_stations_and_sources()


def calc_avg():
    return sum(weighted_distances) / len(weighted_distances)


avg_weighted_distance = calc_avg()

print("\naverage weighted distance: %.2f" % (avg_weighted_distance))
print()
