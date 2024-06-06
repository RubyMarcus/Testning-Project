#!/bin/bash
# Check python version
python --version
# Define the virtual environments
environments=("3.9.13" "3.10.1" "3.8.10")
pyenv shell 3.10.1  # Ensure pyenv is initialized
pyenv rehash
pyenv vname
python --version
# Loop through each environment and run tests
for env in "${environments[@]}"
do
    pyenv local $env  # Ensure pyenv is initialized
    pyenv rehash
    pyenv vname
    python --version

    echo "Activating virtual environment: $env"
    pyenv activate 3

    echo "Installing colorama in $env"
    pip install colorama

    echo "Running tests with $env"
    python -m unittest example_test_suite_v2.py

    echo "Deactivating virtual environment: $env"
    pyenv deactivate
done

echo "Comparing hash values across environments"
python -m unittest test_hash_comparision.py
