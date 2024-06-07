#!/bin/bash
# Check python version
python --version
# Define the virtual environments
#environments=("3.6.8" "3.6.8-win32")
environments=("3.6.8" "3.6.8-win32" "3.7.9" "3.7.9-win32" "3.8.10" "3.8.10-win32" "3.9.7" "3.9.7-win32" "3.10.1" "3.10.1-win32" "3.11.9" "3.11.9-win32" "3.12.3" "3.12.3-win32")

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
    python -m unittest test_suite.py

    echo "Deactivating virtual environment: $env"
    pyenv deactivate
done

echo "Comparing hash values across environments"
python -m unittest test_hash_comparision.py

read -p "Press any key to continue"
