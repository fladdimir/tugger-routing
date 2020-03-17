from enum import Enum, auto
from multiprocessing import Value

import casymda.visualization.web_server.flask_sim_server as fss
from casymda.environments.realtime_environment import SyncedFloat
from casymda.visualization.web_server.sim_controller import RunnableSimulation

import root_dir
from tugger_src.gym_env.base.gym_helper import RealtimeEnvironmentFactory
from tugger_src.gym_env.tugger_env import TuggerEnv
from tugger_src.rl.base_agent import BaseAgentFactory


class AnimationType(Enum):
    TILEMAP = auto()
    PROCESS = auto()


PROCESS_FLOW_SPEED = 20000


class RunnableTuggerEnv(RunnableSimulation):

    root_file = root_dir.__file__

    # width, height
    dimensions = {AnimationType.TILEMAP: (652, 928), AnimationType.PROCESS: (1628, 529)}

    def __init__(
        self, agent_provider: BaseAgentFactory, animation_type=AnimationType.TILEMAP
    ):
        self.animation_type = animation_type
        self.width, self.height = self.dimensions[animation_type]
        self.agent_provider = agent_provider

    def simulate(
        self, shared_state: dict, should_run: Value, factor: SyncedFloat
    ) -> None:

        # setup environment
        environment_provider = RealtimeEnvironmentFactory(
            synced_float=factor, should_run=should_run
        )
        env = TuggerEnv(environment_factory=environment_provider)
        env.reset()

        agent = self.agent_provider.create_agent(env)

        obs = env.reset()

        # setup model animation
        if self.animation_type == AnimationType.TILEMAP:
            env.model.initialize_web_canvas_tilemap_visualization(
                shared_state, self.width, self.height
            )
        if self.animation_type == AnimationType.PROCESS:
            env.model.initialize_web_canvas_process_visualization(
                shared_state, self.width, self.height, flow_speed=PROCESS_FLOW_SPEED
            )

        # run environment

        done = False
        while not done:
            action, _ = agent.predict(obs)
            # As some policy are stochastic by default (e.g. A2C or PPO),
            # you should also try to set deterministic=True when calling the .predict() method
            # sb-docu, unfortunately this does not seem to hold true here, since it did lead to 0 performance
            obs, rewards, done, info = env.step(action)
        env.reset()


def run_server(runnable_simulation: RunnableSimulation):
    fss.run_server(runnable_simulation)


def base_run_process_animation(agent_factory: BaseAgentFactory):
    run_server(RunnableTuggerEnv(agent_factory, animation_type=AnimationType.PROCESS))


def base_run_tilemap_animation(agent_factory: BaseAgentFactory):
    run_server(RunnableTuggerEnv(agent_factory, animation_type=AnimationType.TILEMAP))

