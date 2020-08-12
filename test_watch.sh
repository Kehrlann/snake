#!/usr/bin/env bash

if [[ ! `pip -V | grep virtualenvs` ]]; then
  echo 'Not inside a pipenv. Run pipenv shell before running this script.'
  exit 1
fi
find . -name '*.py' | entr pytest -vv
