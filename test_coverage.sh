#!/usr/bin/env bash

pipenv run coverage run --source snake -m pytest tests
pipenv run coverage report -m
