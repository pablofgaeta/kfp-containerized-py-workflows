from kfp.dsl import Input, Output, Dataset, Metrics
from kfp import dsl

from utils import config

import os
USER_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "user", "config.yaml")

component_config = config.get_component_config(
    base_config={
        "base_image": "python:3.9",
        "packages_to_install": ["pandas", "gcsfs", "fastparquet"],
        "target_image": None,
    },
    user_config_path=USER_CONFIG_PATH
)

@dsl.component(
    base_image=component_config["base_image"],
    packages_to_install=component_config["packages_to_install"],
    target_image=component_config["target_image"],
)
def compute_metrics(sample_dataset: Input[Dataset], mean_value: Output[Metrics]):
    import logging
    import pandas as pd

    from user import stats

    sample_dataset_path = sample_dataset.path

    logging.info(f"Reading dataset from path: {sample_dataset_path}")
    sample_df = pd.read_parquet(sample_dataset_path, engine="fastparquet")

    mean_value.log_metric("mean", stats.sample_mean(sample_df['sample']))
