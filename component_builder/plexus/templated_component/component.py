from kfp import dsl

import os
import yaml

from build.user import main

config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(config_path, "r") as f:
    user_config: dict = yaml.safe_load(f)

component = dsl.component(
    func=main.component_func,
    base_image=user_config.get("base_image", "python:3.9"),
    packages_to_install=user_config.get("packages_to_install", []),
    target_image=user_config.get("target_image"),
)
