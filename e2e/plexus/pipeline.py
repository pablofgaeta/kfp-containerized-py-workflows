from kfp import dsl

from build.components.compute_metrics import compute_metrics
from build.components.generate_sample import generate_sample


@dsl.pipeline(name="python-containerized-multi-test")
def test_multi_component_pipeline(n: int):
    generate_sample_op = generate_sample(n=n)
    compute_metrics(sample_dataset=generate_sample_op.output)
