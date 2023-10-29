# %%
import os
import yaml

import kfp
from pipelines.python_containerized_multi import python_containerized_multi

from google.cloud import aiplatform

# %%
DISPLAY_NAME = "py-con-multi-test"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "build", "user", "config.yaml")
PIPELINE_SPEC_FILE = os.path.join(os.path.dirname(__file__), "pipelines", "pipeline.yaml")

# %%
# replace with default config in application
default_config = {
    "location": "us-central1",
    "enable_caching": False,
    "parameter_values": {
        "n": 10
    }
}

with open(CONFIG_PATH, "r") as f:
    user_config: dict = yaml.safe_load(f)
    pipeline_config = default_config
    pipeline_config.update(user_config.get("pipeline_config", {}))

# %%
kfp.compiler.Compiler().compile(python_containerized_multi, PIPELINE_SPEC_FILE)

# %%
job = aiplatform.PipelineJob(
    template_path=PIPELINE_SPEC_FILE,
    **pipeline_config
)

# %%
job.submit(
    service_account="cvs-vai-pipeline@pg-cvs-sandbox.iam.gserviceaccount.com"
)
# https://pantheon.corp.google.com/vertex-ai/locations/us-west2/pipelines/runs/python-containerized-test-20231025152534?project=pg-cvs-sandbox&e=13803378&mods=dm_deploy_from_gcs
