from kfp.dsl import Input, Output, Dataset, Metrics
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

component_config: dict = user_config.get("compute_metrics", default_config)


@dsl.component(
    base_image=component_config.get("base_image"),
    packages_to_install=component_config.get("packages_to_install"),
    target_image=component_config.get("target_image"),
)
def compute_metrics(sample_dataset: Input[Dataset], mean_value: Output[Metrics]):
    import numpy as np

    from user import stats

    import gcsfs

    fs = gcsfs.GCSFileSystem()
    with fs.open(sample_dataset.path, "r") as sample_file:
        sample = np.load(sample_file)

    mean_value.log_metric("mean", stats.sample_mean(sample))
