#!/usr/bin/env bash

cd /app
python3 manage.py test
pycodestyle --max-line-length=120 --exclude=migrations --ignore=W503,E203,W606,W293 .
