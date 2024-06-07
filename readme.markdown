# Stability and Accuracy of Python's Pickle Functionality Across Versions and Operating Systems

**Date:** 7 June 2024  
**Authors:** Fredrik Johansson and Marcus Lundgren

## Project Setup Instructions

### Prerequisites

To run the project on Linux and macOS, you need to install Python versions 3.6 through 3.12. 

### Step-by-Step Guide

1. **Install Python Versions:**
   Use `pyenv` to install the required Python versions. For example, to install Python 3.6, run:
   ```bash
   pyenv install 3.6
2. **Create Virtual Environments:**
   After installing each Python version, create a virtual environment for it. For example, to create a virtual environment for Python 3.6, run:
   ```bash
   pyenv virtualenv 3.6.15 venv-3.6
3. **Verify Virtual Environments:**
   After installing all Python versions and creating the respective virtual environments, you should have the following virtual environments:
   ```bash
   venv-3.6  venv-3.7  venv-3.8  venv-3.9  venv-3.10  venv-3.11  venv-3.12
4. **Running the Test Suite:**
   Run the following bash script to execute the test suite:
   ```bash
   ./run_tests.sh
   ```
   This script will:
   - Activate each Python environment
   - Install **colorama** for better visualization
   - Run the test suite
   - Deactivate the environment
5. **Compare Test Results:**
   The script will also run **`test_hash_comparison`**, which compares the results across Python versions 3.6 to 3.12.
