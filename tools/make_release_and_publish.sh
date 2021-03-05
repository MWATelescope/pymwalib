#!/usr/bin/env bash

# Go back to the root dir
cd ..

echo Clearing old dist
rm -rf dist

echo Ensure all tools are up to date
pip install --upgrade setuptools wheel pip

echo Ensure twine is installed
pip install twine

echo Create the distribution
python setup.py sdist

# Upload to PyPi
twine upload dist/*
