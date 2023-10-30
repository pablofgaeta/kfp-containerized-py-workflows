from jinja2 import Environment, FileSystemLoader

from utils import config

import inspect 
import os

COMPONENT_TEMPLATE_DIR = os.path.join(os.getcwd(), "components", "premade", "templates")
PIPELINE_TEMPLATE_DIR = os.path.join(os.getcwd(), "pipelines", "premade", "templates")
USER_CONFIG_PATH = os.path.join(os.getcwd(), "components", "build", "config.yaml")
COMPONENT_DIR = os.path.join(os.getcwd(), "components", "build", "components")
PIPELINE_DIR = os.path.join(os.getcwd(), "pipelines", "build")

def custom_pipeline_build():
    from components.build import main

    component_config: dict = config.get_component_config(
        user_config_path=USER_CONFIG_PATH
    )
    component_name = component_config["component_name"]

    pipeline_config: dict = config.get_pipeline_config(
        user_config_path=USER_CONFIG_PATH
    )

    pipeline_params: dict = pipeline_config["parameter_values"]
    pipeline_name = pipeline_params.get('display_name', f'{component_name}_pipeline')

    rendered_pipeline_path = os.path.join(PIPELINE_DIR, f"{pipeline_name}.py")
    with open(rendered_pipeline_path, "w") as rendered_pipeline_file:
        jinja_env = Environment(loader=FileSystemLoader(PIPELINE_TEMPLATE_DIR))
        jinja_template = jinja_env.get_template("_base_pipeline.jinja2")

        component_yaml_basename = f"{main.component.__name__}.yaml"
        comp_annotations = main.component.__annotations__

        simple_comp_annotations = ",".join([f"{k}: {comp_annotations[k].__name__}" for k in pipeline_params.keys()])
        simple_comp_kwargs = ",".join([f"{k} = {k}" for k in pipeline_params.keys()])
        simple_comp_kwargs = ",".join([f"{k} = {k}" for k in pipeline_params.keys()])


        pipeline_str = jinja_template.render(
            component_yaml_basename = component_yaml_basename,
            pipeline_signature = simple_comp_annotations,
            keyword_arguments = simple_comp_kwargs
        )

        rendered_pipeline_file.write(pipeline_str)
    
    return rendered_pipeline_path

def custom_component_build():
    from components.build import main

    component_config: dict = config.get_component_config(
        user_config_path=USER_CONFIG_PATH
    )

    python_func = inspect.getsource(main.component)
    base_image = component_config.get("base_image")
    packages_to_install = component_config.get("packages_to_install")
    target_image = component_config.get("target_image")

    rendered_component_path = os.path.join(COMPONENT_DIR, "component.py")
    with open(rendered_component_path, "w") as rendered_component_file:
        jinja_env = Environment(loader=FileSystemLoader(COMPONENT_TEMPLATE_DIR))
        jinja_template = jinja_env.get_template("_base_component.jinja2")

        component_str = jinja_template.render(
            python_func = python_func,
            base_image = base_image,
            packages_to_install = packages_to_install,
            target_image = target_image
        )

        rendered_component_file.write(component_str)
    
    return rendered_component_path
