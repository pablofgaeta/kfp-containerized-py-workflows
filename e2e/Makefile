build:
	rm -rf plexus/build

	mkdir plexus/build
	touch plexus/build/__init__.py

	cp -r user/ plexus/build/user
	cp -r plexus/components plexus/build/components

	kfp component build plexus/build/ --component-filepattern components/*.py --push-image

test:
	rm -f plexus/pipelines/pipeline.yaml
	python plexus/runner.py