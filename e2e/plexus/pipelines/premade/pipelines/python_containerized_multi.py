from kfp import dsl, components

import os

def load(component_yaml_dir: str, **pipeline_args):
    compute_metrics = components.load_component_from_file(
        file_path=os.path.join(component_yaml_dir, "compute_metrics.yaml")
    )
    generate_sample = components.load_component_from_file(
        file_path=os.path.join(component_yaml_dir, "generate_sample.yaml")
    )

    @dsl.pipeline(**pipeline_args)
    def python_containerized_multi(n: int):
        generate_sample_op = generate_sample(n=n)
        compute_metrics(sample_dataset=generate_sample_op.output)
    
    return python_containerized_multi
