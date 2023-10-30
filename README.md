# kfp-containerized-py-workflows

## Getting started

The `examples/` directory includes an example for each workflow. The config yaml files must be updated to point to valid GCP resources run the example `Makefile` targets.

Once the configs have been updated properly, the custom and template examples can be built with `make build-custom` and `make build-template`, respectively.

To run a test pipeline after building, the custom and template examples can be ran with `make test-custom` and `make test-template`, respectively.

## Workflow Options

1. Custom Component Creation

    - Users can define custom code to run as a component without worrying about including KFP code in their solution. Supports referencing local utility files in a `user` directory.
    - Required files:
        - `main.py`: Defines a function called `component` that defines the main entrypoint for the component code. Accepts all primitive types supported by KFP.
        - `config.yaml`: Defines the configurations for the custom component to build and the test pipeline if the pipeline runner is used.
        - `__init__.py`: Empty file to make this source code a module.
    - Optional files:
        - `user/`: Directory including any source code to be used by the custom component.
    - Build requirements:
        - Can work with any KFP DSL artifacts as long as their type hints begin with `kfp` or `dsl` (e.g. `kfp.dsl.Input[kfp.dsl.Dataset]` or `dsl.Input[dsl.Dataset]`). Both input and output artifacts are valid.
    - Pipeline test requirements:
        - Only DSL output artifacts will work for the test pipeline runner since no input artifacts can be passed when only testing a single component (e.g. `dsl.Output[dsl.Dataset]` is supported, but `dsl.Input[dsl.Dataset]` is NOT supported).

2. Template Pipeline Creation

    - In this workflow, a producer team can generate component and pipeline template files that import custom user code to define custom logic at certain steps in the pipeline. This enables users to only focus on defining their custom implementations of required functions without having to worry about any components or pipelines. The producer teams can also set defaults for the component and pipeline configuration to default to.
    - Required files:
        - `user/`: Directory including custom source code required by template components. The required modules/functions must be defined by each template pipeline producer, including input and output specifications.
        - `config.yaml`: Defines the configurations for the custom component to build and the test pipeline if the pipeline runner is used.
        - `__init__.py`: Empty file to make this source code a module.
    - Build requirements:
        - Additional dependencies used by the custom user code must be compatible with any dependencies required for the template components.
    - Pipeline test requirements:
        - No additional requirements as long as correct pipeline parameters are passed to the template pipeline and the user code follows the rules defined by the producer.


