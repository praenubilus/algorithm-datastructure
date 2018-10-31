#!/usr/bin/env bash

deactivate
rm -rf .venv
python -m venv .venv
source "./.venv/bin/activate"
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt
deactivate