build:
	rm -rf plexus/build
	mkdir plexus/build

	cp -r user/ plexus/build/user

	kfp component build plexus/build/ --component-filepattern user/main.py --push-image

test:
	rm -f plexus/pipeline.yaml
	python plexus/runner.py