#!/usr/bin/env bash

if [[ ! `pip -V | grep virtualenvs` ]]; then
  echo 'Not inside a pipenv. Run pipenv shell before running this script.'
  exit 1
fi
mypy snake \
 --disallow-untyped-calls \
 --disallow-untyped-defs \
 --disallow-incomplete-defs \
 --disallow-untyped-decorators
