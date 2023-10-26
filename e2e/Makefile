build:
	rm -rf plexus/build
	mkdir plexus/build

	cp -r user/ plexus/build/user
	cp -r plexus/components plexus/build/components

	kfp component build plexus/build/ --component-filepattern components/*.py --push-image

test:
	rm -f plexus/pipeline.yaml
	python plexus/runner.py