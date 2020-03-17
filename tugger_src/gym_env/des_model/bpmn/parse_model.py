"""create a casymda model from a bpmn file and a template"""
from casymda.bpmn.bpmn_parser import parse_bpmn

BPMN_PATH = "tugger_src/gym_env/des_model/bpmn/model.bpmn"
TEMPLATE_PATH = "tugger_src/gym_env/des_model/bpmn/model_template.py"
JSON_PATH = "tugger_src/gym_env/des_model/bpmn/_temp_bpmn.json"
MODEL_PATH = "tugger_src/gym_env/des_model/model.py"


def test_parse_bpmn():
    parse_bpmn(BPMN_PATH, JSON_PATH, TEMPLATE_PATH, MODEL_PATH)


if __name__ == "__main__":
    test_parse_bpmn()
