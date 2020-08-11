#!/usr/bin/env bash

find . -name '*.py' | entr pipenv run pytest -vv
