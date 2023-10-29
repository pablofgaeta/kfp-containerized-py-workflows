build:
	# Reset build dir
	rm -rf plexus/components/build
	mkdir plexus/components/build

	# Copy user code into build dir
	cp -r user/ plexus/components/build/user

	# Copy premade code into build dir
	cp -r plexus/components/premade/* plexus/components/build/

	# Open bug preventing local modules from being seen when building components: https://github.com/kubeflow/pipelines/issues/8385
	# To resolve this, add the working directory to PYTHONPATH so the kfp script will see the local modules.
	# To avoid issues, all build files (e.g. components and utils modules) must use absolute imports (within the scope of the build dir)
	cd plexus/components/build && \
	export PYTHONPATH="${PWD}:${PYTHONPATH}" && \
	kfp component build . --component-filepattern "components/*.py" --push-image

test:
	cd plexus && python runner.py