#!/bin/sh

mkdir config
touch config/__init__.py

mkdir config/res
touch config/res/__init__.py

mkdir config/saves
touch config/saves/__init__.py

python nanideshiko.py
