from kfp import dsl

from build.components.compute_metrics import compute_metrics
from build.components.generate_sample import generate_sample

import os
import yaml

config_path = os.path.join(os.path.dirname(__file__), "..", "build", "user", "config.yaml")
with open(config_path, "r") as f:
    user_config: dict = yaml.safe_load(f)
    pipeline_config: dict = user_config["pipeline_config"]

@dsl.pipeline(name=pipeline_config.get("display_name"))
def python_containerized_multi(n: int):
    generate_sample_op = generate_sample(n=n)
    compute_metrics(sample_dataset=generate_sample_op.output)
