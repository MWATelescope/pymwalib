#!/usr/bin/env bash

# Go back to the root dir
cd ..

echo Clearing old dist
rm -rf dist
rm -rf build
rm -rf .pymwalib.egg-info

echo Ensure all tools are up to date
pip install --upgrade pip setuptools distutils wheel twine

echo Build
python setup.py install

echo Create the distribution
python setup.py sdist

# Upload to PyPi
twine upload dist/*
