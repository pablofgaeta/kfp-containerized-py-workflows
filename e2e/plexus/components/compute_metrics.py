from kfp.dsl import Input, Output, Dataset, Metrics
from kfp import dsl

import os
import yaml

config_path = os.path.join(os.path.dirname(__file__), "..", "user", "config.yaml")
with open(config_path, "r") as f:
    user_config: dict = yaml.safe_load(f)
    component_config: dict = user_config["component_config"]

default_config = {
    "base_image": "python:3.9",
    "packages_to_install": ["pandas", "gcsfs", "fastparquet"],
    "target_image": None,
}

base_image = component_config.get('base_image', default_config["base_image"])
packages_to_install = list(set(default_config["packages_to_install"] + component_config.get('packages_to_install', [])))
target_image = component_config.get("target_image", default_config["target_image"])

@dsl.component(
    base_image=base_image,
    packages_to_install=packages_to_install,
    target_image=target_image,
)
def compute_metrics(sample_dataset: Input[Dataset], mean_value: Output[Metrics]):
    import logging
    import pandas as pd

    from user import stats

    try:
        sample_dataset_path = sample_dataset.path

        logging.info(f"Reading dataset from path: {sample_dataset_path}")
        sample_df = pd.read_parquet(sample_dataset_path, engine="fastparquet")

        mean_value.log_metric("mean", stats.sample_mean(sample_df['sample']))
    except Exception as e:
        logging.exception(e)