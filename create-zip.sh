#!/bin/bash

rm -f bundle.zip
rm -rf WordGuesser/__pycache__
zip -r bundle.zip main.py requirements.txt WordGuesser/