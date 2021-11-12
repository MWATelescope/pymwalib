#!/usr/bin/env bash
# Build
python setup.py install

# Check Linting
flake8 pymwalib --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics