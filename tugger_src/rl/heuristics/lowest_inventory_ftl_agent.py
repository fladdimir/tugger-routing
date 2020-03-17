from typing import Dict, List, Tuple, cast

from tugger_src.gym_env.des_model.blocks.product_station import ProductStation
from tugger_src.gym_env.des_model.blocks.tugger_stock import TuggerStock
from tugger_src.gym_env.des_model.model import coordinates_holder
from tugger_src.gym_env.tugger_env import TuggerEnv
from tugger_src.rl.base_agent import BaseAgent, BaseAgentFactory, evaluate_agent
from tugger_src.rl.web_animation.base_runnable_tugger_env import (
    base_run_process_animation,
    base_run_tilemap_animation,
)


class Agent(BaseAgent):
    """ always delivers the maximum amount of material (FTL) to the station with the lowest invenvory """

    def __init__(self, env: TuggerEnv) -> None:
        self.env = env
        self.env.reset()
        model = self.env.model
        self.resource_types = model.tugger_source.resource_types

        product_stations = cast(List[ProductStation], model.blocks_dict[ProductStation])
        self.product_station_names_by_resource: Dict[str, List[str]] = {}
        for ps in product_stations:
            if ps.consumed_resource not in self.product_station_names_by_resource:
                self.product_station_names_by_resource[ps.consumed_resource] = []
            self.product_station_names_by_resource[ps.consumed_resource].append(ps.name)

        stocks = cast(List[TuggerStock], model.blocks_dict[TuggerStock])
        self.stock_locations = [st.location for st in stocks]

    def predict(
        self, observation, state=None, deterministic=None
    ) -> Tuple[int, object]:

        model = self.env.model

        # current tugger_load & position # Multi-Tugger TODO
        tugger = model.tugger_source.tugger_entities[0]
        load = tugger.load
        capa = tugger.capacity
        sum_load = sum(load.values())
        current_location = tugger.location

        action = None  # to be determined

        # stock?
        if current_location in self.stock_locations:
            if sum_load < capa:
                # continue loading
                action = coordinates_holder.get_location_index_by_name(current_location)
            else:
                # sum_load >= capa:
                # choose station with lowest inventory for currently loaded type
                loaded_type = next(rt for rt in load if load[rt] == max(load.values()))
                possible_target_names = self.product_station_names_by_resource[
                    loaded_type
                ]
                possible_targets = [
                    model.model_components[name] for name in possible_target_names
                ]
                ps = self._find_product_station_with_lowest_inventory_from_list(
                    possible_targets
                )
                action = coordinates_holder.get_location_index_by_name(ps.location)
        # station?
        else:
            if sum_load > 0:
                # continue unloading
                action = coordinates_holder.get_location_index_by_name(current_location)
            else:
                # find stock of currently lowest inventory
                product_stations = cast(
                    List[ProductStation], model.blocks_dict[ProductStation]
                )
                ps = self._find_product_station_with_lowest_inventory_from_list(
                    product_stations
                )
                needed_resource = ps.consumed_resource

                stocks = cast(List[TuggerStock], model.blocks_dict[TuggerStock])
                stock = next(s for s in stocks if s.loaded_resource == needed_resource)
                action = coordinates_holder.get_location_index_by_name(stock.location)
        return action, None

    def _find_product_station_with_lowest_inventory_from_list(
        self, product_stations: List[ProductStation],
    ) -> ProductStation:
        min_inv = min(ps.container.level for ps in product_stations)
        return next(ps for ps in product_stations if ps.container.level == min_inv)


# add test for performance under specified conditions, and refactor agent code


class AgentFactory(BaseAgentFactory):
    def create_agent(self, env: TuggerEnv):
        return Agent(env)


def evaluate():
    evaluate_agent(AgentFactory(), n_eval_episodes=3)


def run_process_animation():
    base_run_process_animation(AgentFactory())


def run_tilemap_animation():
    base_run_tilemap_animation(AgentFactory())
