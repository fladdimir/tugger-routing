from simpy import Environment, RealtimeEnvironment
from tugger_src.gym_env.des_model.model import Model


def test_that_model_intializes():
    env = Environment()
    model = Model(env)
    assert model is not None


def test_that_model_auto_wires_tugger_sources():
    env = Environment()
    model = Model(env)
    assert len(model.tugger_source.resource_types) == 2


def test_that_model_produces_tuggers():
    env = Environment()
    model = Model(env)
    env.run(until=1)
    assert model.tugger_source.overall_count_in == model.tugger_source.max_entities
    # (should all be produced at 0)


def test_that_T1_receives_some_product():
    env = Environment()
    model = Model(env)
    env.run(until=1000)
    assert model.T1.overall_count_in > 0


def test_model_with_tk_process_visualization(
    until=0.00001, factor=0.1, flow_speed=10 ** 10
):
    env = RealtimeEnvironment(factor=factor, strict=False)
    model = Model(env)
    canvas = model.initialize_tkinter_process_visualization(flow_speed=flow_speed)
    env.run(until=until)
    canvas.tk_gui.destroy()
    assert True


def test_model_run_1_hour():
    env = Environment()
    model = Model(env)
    env.run(until=3600)
    assert model.T1.overall_count_in > 0
    assert model.movement.overall_count_in > 1
    # assuming more than 1 completed move per hour


def test_model_with_tk_tilemap_visualization(until=0.00001, factor=1 / 10 ** 10):
    env = RealtimeEnvironment(factor=factor, strict=False)
    model = Model(env)
    canvas = model.initialize_tkinter_tilemap_visualization()
    env.run(until=until)
    canvas.tk_gui.destroy()
