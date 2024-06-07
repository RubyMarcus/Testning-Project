# Stability and Accuracy of Python's Pickle Functionality Across Versions and Operating Systems

**Date:** 7 June 2024  
**Authors:** Fredrik Johansson and Marcus Lundgren

## Project Setup Instructions

### Prerequisites for Linux and macOS

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
   The bash script will also run **`test_hash_comparison`**, which compares the results across Python versions 3.6 to 3.12.

### Prerequisites for Windows

To run the project on Windows, you need to install Python versions 3.6 through 3.12 for both 32-bit and 64-bit.

1. **Install Python Versions:**
   Use `pyenv` to install the required Python versions. For example, to install Python 3.6 (64bit) and Python 3.6 (32bit), run:
   ```bash
   pyenv install 3.6.8
   pyenv install 3.6.8-win32
   
2. **Verify Python Installations:**
   After installing all python versions, you should have the following versions
   ```bash
   3.6.8   3.6.8-win32   3.7.9   3.7.9-win32   3.8.10   3.8.10-win32   3.9.7   3.9.7-win32
   3.10.1   3.10.1-win32   3.11.9   3.11.9-win32   3.12.3   3.12.3-win32
3. **Running the Test Suite:**
   Run the following bash script to execute the test suite:
   ```bash
   ./run_tests_win.sh
   ```
   This script will:
   - Activate each Python environment
   - Install **colorama** for better visualization (WON'T WORK ON WINDOWS)
   - Run the test suite
   - Deactivate the environment
4. **Compare Test Results:**
   The bash script will also run **`test_hash_comparison`**, which compares the results across Python versions 3.6 to 3.12.

### Comparing result between operating systems

To compare the result gained from running the bash scripts on Windows, Linux and macOS, use the following command:
   ```bash
   python3 compare_all.py
