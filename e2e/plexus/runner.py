# %%
import os
import yaml

import kfp
from pipeline import test_multi_component_pipeline

from google.cloud import aiplatform

# %%
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "build", "user", "config.yaml")
PIPELINE_SPEC_FILE = os.path.join(os.path.dirname(__file__), "pipeline.yaml")

# %%
with open(CONFIG_PATH, "r") as f:
    user_config: dict = yaml.safe_load(f)

# %%
kfp.compiler.Compiler().compile(test_multi_component_pipeline, PIPELINE_SPEC_FILE)

# %%
job = aiplatform.PipelineJob(
    display_name="python-containerized-multi-test",
    template_path=PIPELINE_SPEC_FILE,
    enable_caching=False,
    pipeline_root="gs://cvs_demo_bucket",
    parameter_values=user_config.get("config"),
    project="pg-cvs-sandbox",
    location="us-west2",
)

# %%
job.submit()
# https://pantheon.corp.google.com/vertex-ai/locations/us-west2/pipelines/runs/python-containerized-test-20231025152534?project=pg-cvs-sandbox&e=13803378&mods=dm_deploy_from_gcs
