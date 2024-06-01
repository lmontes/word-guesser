.PHONY: test

lib:
	python src/lib/setup.py sdist bdist_wheel

zip:
	rm -rf build/app
	mkdir -p build/app/WordGuesser/
	cp -r src/app/* build/app/
	cp -r src/lib/WordGuesser/* build/app/WordGuesser/
	# Create zip
	rm -f dist/bundle.zip
	mkdir -p dist
	zip -r dist/bundle.zip \
		build/app/* \
		--exclude __pycache__

test:
	pytest test/