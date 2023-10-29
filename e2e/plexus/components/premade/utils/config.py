from typing import Any, Optional
from copy import deepcopy

import os
import yaml

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "user", "config.yaml")

def _get_user_config(user_config_path: str = DEFAULT_CONFIG_PATH) -> dict:
    with open(user_config_path, "r") as f:
        user_config: dict = yaml.safe_load(f)
    return user_config

def _get_user_var(var_name: str, user_config_path: str = DEFAULT_CONFIG_PATH) -> Any:
    user_config = _get_user_config(user_config_path)

    if var_name in user_config:
        user_var = user_config[var_name]
        return user_var
    else:
        err_msg = f"{var_name} is not in the user config file: {user_config_path}"
        raise KeyError(err_msg)

def get_pipeline_config(base_config: Optional[dict], user_config_path: str = DEFAULT_CONFIG_PATH) -> dict:
    if base_config is not None:
        pipeline_config: dict = deepcopy(base_config)
    else:
        pipeline_config = {}

    user_pipeline_config: dict = _get_user_var("pipeline_config", user_config_path)
    pipeline_config.update(user_pipeline_config)

    return pipeline_config

def get_component_config(base_config: dict, user_config_path: str = DEFAULT_CONFIG_PATH) -> dict:
    default_base_image = base_config.get("base_image", "python:3.9")
    default_packages = base_config.get("packages_to_install", [])
    default_target_image = base_config.get("target_image") # Update with default target image if it can be generated

    user_component_config: dict = _get_user_var("component_config", user_config_path)

    component_config = {
        "base_image": user_component_config.get('base_image', default_base_image),
        "packages_to_install": list(set(user_component_config.get("packages_to_install", []) + default_packages)),
        "target_image": user_component_config.get("target_image", default_target_image)
    }
    
    return component_config