#!/bin/sh

mkdir -p config/res config/saves
touch config/__init__.py config/res/__init__.py config/saves/__init__.py

python nanideshiko.py
