#!/bin/bash

install_component() {
    echo "Installing $1."

    output=$(eval "pip install $2" 2>&1)
    local status=$?

    if [ $status -ne 0 ]; then
        echo "Error: Installation of $1 failed!"
        echo "Details: $output"
        return 1
    fi
}

if [ -f venv/bin/activate ]; then
  source venv/bin/activate
fi

install_component "Graph visualizer API" "./api" || exit 1
install_component "Graph visualizer Core" "./core" || exit 1
install_component "Simple visualizer" "./simple_visualizer" || exit 1
install_component "Block visualizer" "./block_visualizer" || exit 1
install_component "Json loader" "./json_loader" || exit 1
install_component "Graph explorer" "./graph_explorer" || exit 1

echo "All components installed successfully."