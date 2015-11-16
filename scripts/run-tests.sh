#!/bin/bash
# Run Python unit tests
./scripts/pip-install-requirements.sh
pip install -q nose
nosetests -v

# Validate example in README
./scripts/validate-readme-example.sh