#!/usr/bin/env bash
# Build
pip install .

# Check Linting
flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
