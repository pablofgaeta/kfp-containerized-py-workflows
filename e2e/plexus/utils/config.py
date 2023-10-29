from typing import Any

import os
import yaml

USER_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "build", "user", "config.yaml")

def get_user_config() -> dict:
    with open(USER_CONFIG_PATH, "r") as f:
        user_config: dict = yaml.safe_load(f)
    return user_config

def get_user_var(var_name: str) -> Any:
    user_config = get_user_config()

    if var_name in user_config:
        user_var = user_config[var_name]
        return user_var
    else:
        err_msg = f"{var_name} is not in the user config file: {USER_CONFIG_PATH}"
        raise KeyError()