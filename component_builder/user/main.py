from kfp.dsl import Output, Dataset, Metrics
from kfp import dsl

import os
import yaml

config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(config_path, "r") as f:
    user_config: dict = yaml.safe_load(f)


@dsl.component(
    base_image=user_config.get("base_image", "python:3.9"),
    packages_to_install=user_config.get("packages_to_install", []),
    target_image=user_config.get("target_image"),
)
def component(
    config: dict, sample_dataset: Output[Dataset], mean_value: Output[Metrics]
):
    import numpy as np
    from user.utils import stats

    n = config["n"]

    sample = stats.gen_sample(n)

    mean_value.log_metric("mean", float(sample.mean()))
    np.save(sample_dataset.path, sample)
