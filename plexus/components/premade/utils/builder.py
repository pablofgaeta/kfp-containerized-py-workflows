from kfp import dsl

from user import main
from utils import config

def build(component_func):
    component_config = config.get_component_config()

    component = dsl.component(
        func=main.component_func,
        base_image=component_config.get("base_image"),
        packages_to_install=component_config.get("packages_to_install"),
        target_image=component_config.get("target_image"),
    )
