build-template:
	# Reset build dir
	rm -rf plexus/components/build
	mkdir plexus/components/build

	# Copy user code into build dir
	cp -r user-template/ plexus/components/build/user

	# Copy premade code into build dir
	# In practice, depending on what template pipeline a user is making, you would only want to copy over the components needed for that pipeline
	cp -r plexus/components/premade/* plexus/components/build/

	# Open bug preventing local modules from being seen when building components: https://github.com/kubeflow/pipelines/issues/8385
	# To resolve this, add the working directory to PYTHONPATH so the kfp script will see the local modules.
	# To avoid issues, all build files (e.g. components and utils modules) must use absolute imports (within the scope of the build dir)
	cd plexus/components/build && \
	export PYTHONPATH="${PWD}:${PYTHONPATH}" && \
	kfp component build . --component-filepattern "components/*.py" --push-image

build-custom:
	# Reset build dir
	rm -rf plexus/components/build
	mkdir plexus/components/build

	# Copy user code into build dir
	cp -r user-custom/ plexus/components/build/user

	# TODO: Build the custom user code into a kfp component. Store in the build/components/ dir

	# Open bug preventing local modules from being seen when building components: https://github.com/kubeflow/pipelines/issues/8385
	# To resolve this, add the working directory to PYTHONPATH so the kfp script will see the local modules.
	# To avoid issues, all build files (e.g. components and utils modules) must use absolute imports (within the scope of the build dir)
	cd plexus/components/build && \
	export PYTHONPATH="${PWD}:${PYTHONPATH}" && \
	kfp component build . --component-filepattern "components/*.py" --push-image

test-template:
	# Test out the template pipeline using user code with the user-defined pipeline params
	cd plexus && python template-runner.py

test-custom:
	# Test out the custom user component with the user-defined pipeline params
	cd plexus && python custom-runner.py