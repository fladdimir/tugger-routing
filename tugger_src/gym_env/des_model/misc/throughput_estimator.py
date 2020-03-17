from tugger_src.gym_env.tugger_env import TuggerEnv
import tugger_src.gym_env.des_model.blocks.tugger_movement as tugger_movement
import tugger_src.gym_env.des_model.misc.avg_distance_calculator as adc
from tugger_src.gym_env.des_model.blocks.product_station import ProductStation
from tugger_src.gym_env.des_model.blocks.tugger_entity import TuggerEntity
from tugger_src.gym_env.des_model.blocks.tugger_station import TuggerStation
from tugger_src.gym_env.des_model.blocks.tugger_stock import TuggerStock

model = adc.model
stations = adc.stations

print("\nupper bound: station capacity (takt_time)")
takt_time = ProductStation.PROCESSING_TIME
print("processing time per product: " + str(takt_time))
max_throughput = 1 / takt_time
max_episode = TuggerEnv.TIME_TO_BE_DONE * max_throughput
print("max episode: " + str(max_episode))

print("\ncycle_time = loading + driving + unloading + driving")
tugger_load = TuggerEntity.CAPACITY_LIMIT
num_loading_moves = tugger_load / TuggerStock.MAX_AMOUNT_LOADED_PER_VISIT
time_per_loading_move = TuggerStock.FIXED_TIME + (
    TuggerStock.TIME_PER_RESOURCE_LOADED * TuggerStock.MAX_AMOUNT_LOADED_PER_VISIT
)
loading_time = num_loading_moves * time_per_loading_move
print("loading time: " + str(loading_time))
tugger_speed = tugger_movement.SPEED  # px / sec
driving_time = adc.avg_weighted_distance / tugger_speed
print("avg driving time: " + str(driving_time))
num_unloading_moves = tugger_load / TuggerStation.MAX_UNLOADED_AMOUNT_PER_VISIT
time_per_unloading_move = TuggerStation.FIXED_TIME + (
    TuggerStation.TIME_PER_RESOURCE_UNLOADED
    * TuggerStation.MAX_UNLOADED_AMOUNT_PER_VISIT
)
unloading_time = num_unloading_moves * time_per_unloading_move
print("unloading time: " + str(unloading_time))
cycle_time = sum((loading_time, driving_time, loading_time, driving_time))
print("avg cycle_time: " + str(cycle_time))
print("delivered per cycle: " + str(tugger_load))
delivered_per_time = tugger_load / cycle_time
print("delivered_per_time: " + str(delivered_per_time))

print("\nutilization = (delivered / demand) (max 1)")
num_stations = len(stations)
demand_per_product = adc.avg_consumption_per_product_per_station * num_stations
print("demand_per_product: " + str(demand_per_product))
demand_per_time = demand_per_product / takt_time
print("demand_per_time: " + str(demand_per_time))

utilization = delivered_per_time / demand_per_time
print("expected_utilization: %.2f " % (utilization))

expected_throughput_episode = max_episode * utilization
print("\nexpected throughput episode: " + str(expected_throughput_episode))

print()
