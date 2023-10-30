# %%
import os

import pipelines
from pipelines import python_containerized_multi

from google.cloud import aiplatform

# %%
# Where component yamls are stored. If uploaded to a central repo, can instead pull from there.
component_yaml_dir = os.path.join(os.getcwd(), "components", "build", "component_metadata")

# User config where build time default pipeline params are stored. Not needed, but easy to grab for demo.
user_config_path = os.path.join(os.getcwd(), "components", "build", "user", "config.yaml")

# %%
# Get build time config. Not needed if running a custom pipeline job.
from utils import config
pipeline_config = config.get_pipeline_config(
    base_config={"location": "us-central1", "enable_caching": False},
    user_config_path=user_config_path
)

# %%
# Load and compile target pipeline
pipeline = python_containerized_multi.load(
    component_yaml_dir = component_yaml_dir,
    name = pipeline_config['display_name']
)
pipeline_spec_file = pipelines.compile(pipeline)

# %%
# Construct pipeline job
job = aiplatform.PipelineJob(template_path=pipeline_spec_file, **pipeline_config)

# %%
# Run pipeline job
job.submit(service_account="cvs-vai-pipeline@pg-cvs-sandbox.iam.gserviceaccount.com")
