from kfp.dsl import Output, Dataset, Metrics
from kfp import dsl

import os
import yaml

config_path = os.path.join(os.path.dirname(__file__), "..", "user", "config.yaml")
with open(config_path, "r") as f:
    user_config: dict = yaml.safe_load(f)

default_config = {
    "base_image": "python:3.9",
    "packages_to_install": [],
    "target_image": None,
}

component_config: dict = user_config.get("generate_sample", default_config)


@dsl.component(
    base_image=component_config.get("base_image"),
    packages_to_install=component_config.get("packages_to_install"),
    target_image=component_config.get("target_image"),
)
def generate_sample(n: int, sample_dataset: Output[Dataset]):
    import numpy as np
    from user import stats

    sample = stats.gen_sample(n)
    np.save(sample_dataset.path, sample)
