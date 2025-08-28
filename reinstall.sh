#!/bin/bash

if [ -f venv/bin/activate ]; then
  source venv/bin/activate
fi

if [[ "$1" == "graph_explorer" ]]; then
    packagename="graph_visualizer_web"
elif [[ "$1" == "core" ]]; then
    packagename="graph_visualizer_core"
elif [[ "$1" == "api" ]]; then
    packagename="graph_visualizer_api"
else
    packagename="$1"
fi

cd "./$1"
rm -rf ./build
rm -rf "./$packagename.egg-info"
cd ../

pip uninstall "$packagename" -y
pip install "./$1"

