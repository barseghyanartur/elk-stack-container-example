#!/usr/bin/env bash
python /usr/src/app/main.py migrate
python /usr/src/app/main.py "$@"
