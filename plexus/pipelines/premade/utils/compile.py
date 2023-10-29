import kfp.compiler
import os
from typing import Callable

DEFAULT_BUILD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "build")

def compile(pipeline: Callable, pipeline_build_dir: str = DEFAULT_BUILD_DIR):
    package_path = os.path.join(pipeline_build_dir, f"{pipeline.name}.yaml")
    kfp.compiler.Compiler().compile(pipeline, package_path)
    return package_path