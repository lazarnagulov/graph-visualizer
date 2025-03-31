#!/bin/bash
cd "./$1"
rm -rf ./build
rm -rf "./$1.egg-info"
cd ../

pip uninstall $1 -y
pip install "./$1"

