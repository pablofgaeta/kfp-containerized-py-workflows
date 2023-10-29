from kfp import dsl, components

def load(component_yaml_dir: str, **pipeline_args):
    component = components.load_component_from_file(component_yaml_dir, "compute_metrics.yaml")

    @dsl.pipeline(**pipeline_args)
    def test_component_pipeline(config: dict):
        component(config=config)
    
    return test_component_pipeline
