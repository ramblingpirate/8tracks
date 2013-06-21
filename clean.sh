#!/bin/bash
find . -iname '__pycache__' -exec rm -r {} +
find . -iname '*.pyc' -exec rm -r {} +
