build-template:
	# Reset build dir
	rm -rf src/components/build
	mkdir src/components/build

	# Copy user code into build dir
	cp -r examples/template/* src/components/build/

	# Copy premade code into build dir
	# In practice, depending on what template pipeline a user is making, you would only want to copy over the components needed for that pipeline
	cp -r src/components/premade/components/ src/components/build/components/
	cp -r src/components/premade/utils/ src/components/build/utils/

	# Open bug preventing local modules from being seen when building components: https://github.com/kubeflow/pipelines/issues/8385
	# To resolve this, add the working directory to PYTHONPATH so the kfp script will see the local modules.
	# To avoid issues, all build files (e.g. components and utils modules) must use absolute imports (within the scope of the build dir)
	cd src/components/build && \
	export PYTHONPATH="${PWD}:${PYTHONPATH}" && \
	kfp component build . --component-filepattern "components/*.py" --push-image

build-custom:
	# Reset build dir
	rm -rf src/components/build
	mkdir -p src/components/build/components

	# Copy user code into build dir
	cp -r examples/custom/* src/components/build

	# Build the custom user code into a kfp component. Store in the build/components/ dir
	cd src && python -c "from utils import custom_component_build; custom_component_build()"

	# Open bug preventing local modules from being seen when building components: https://github.com/kubeflow/pipelines/issues/8385
	# To resolve this, add the working directory to PYTHONPATH so the kfp script will see the local modules.
	# To avoid issues, all build files (e.g. components and utils modules) must use absolute imports (within the scope of the build dir)
	cd src/components/build && \
	export PYTHONPATH="${PWD}:${PYTHONPATH}" && \
	kfp component build . --component-filepattern "components/*.py" --push-image

test-template:
	# Test out the template pipeline using user code with the user-defined pipeline params
	cd src && python template-runner.py

test-custom:
	# Build pipeline definition based off of signature of the built component
	cd src && python -c "from utils import custom_pipeline_build; custom_pipeline_build()"

	# Test out the custom user component with the user-defined pipeline params
	cd src && python custom-runner.py