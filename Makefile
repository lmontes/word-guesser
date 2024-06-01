.PHONY: test

lib:
	python src/lib/setup.py sdist bdist_wheel

zip:
	rm -rf build/cloud_function
	mkdir -p build/cloud_function/WordGuesser/
	cp -r src/cloud_function/* build/cloud_function/
	cp -r src/lib/WordGuesser/* build/cloud_function/WordGuesser/
	# Create zip
	rm -f dist/bundle.zip
	mkdir -p dist
	cd build/cloud_function && zip -r ../../dist/bundle.zip * -x '*/__pycache__/*'

test:
	pytest test/

clean:
	rm -rf .pytest_cache build dist word_guesser.egg-info
