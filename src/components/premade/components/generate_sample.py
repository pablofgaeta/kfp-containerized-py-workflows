from kfp.dsl import Output, Dataset
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
def generate_sample(n: int, sample_dataset: Output[Dataset]):
    import logging
    import pandas as pd

    from user import stats

    sample = stats.gen_sample(n)

    df = pd.DataFrame({"sample": sample})

    sample_dataset_path = sample_dataset.path

    logging.info(f"Writing dataset to path: {sample_dataset_path}")
    df.to_parquet(sample_dataset_path, engine="fastparquet")
