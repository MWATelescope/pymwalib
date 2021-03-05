#!/usr/bin/env bash

# Go back to the root dir
cd ..
echo Ensure all tools are up to date
pip install --upgrade pip
pip install setuptools

echo Ensure twine is installed
pip install twine

echo Create the distribution
python setup.py sdist

# Upload to PyPi
#twine upload dist/*
