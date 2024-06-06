#!/bin/bash

# Define the virtual environments
environments=("venv-3.6" "venv-3.7" "venv-3.8" "venv-3.9" "venv-3.10" "venv-3.11"  "venv-3.12")

# Loop through each environment and run tests
for env in "${environments[@]}"
do
	eval "$(pyenv init -)"

    echo "Activating virtual environment: $env"
    pyenv activate "$env"

    echo "Installing colorama in $env"
    pip install colorama

    echo "Running tests with $env"
    python -m unittest example_test_suite_v3.py

    echo "Deactivating virtual environment: $env"
    pyenv deactivate
done

echo "Comparing hash values across environments"
python3 -m unittest test_hash_comparision.py 
