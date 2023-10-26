import os

import kfp
from kfp import dsl

component_yaml_path = os.path.join(
    os.path.dirname(__file__), "build", "component_metadata", "component.yaml"
)

component = kfp.components.load_component_from_file(component_yaml_path)


@dsl.pipeline(name="python-containerized-test")
def test_component_pipeline(config: dict):
    component(config=config)
