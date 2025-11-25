#!/bin/bash

# ----------------------------------------
# Description: Installs Python via Homebrew, creates a virtual environment,
#              installs Python packages using pip inside the venv without activating,
#              and saves the installed packages.
# Platform: macOS
# Autor: Ronja Ehlers
# ----------------------------------------
# How to: 
# you can run the script directly from the terminal using `bash` using the command:
# bash python_install_createenv.sh
# ----------------------------------------
# What the script does:
# - Checks if Homebrew is installed and installs it if missing.
# - Installs Python via Homebrew.
# - Creates a project folder named `my_python`.
# - Sets up a virtual environment inside that folder (`venv`).
# - Upgrades `pip` inside the virtual environment.
# - Installs selected Python packages (`numpy`, `pandas`).
# - Saves the environment to `requirements.txt` without activating the environment.
# ----------------------------------------
# ----------------------------------------

# Step -1: Check if Homebrew is installed
echo "Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed."
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "Homebrew installation complete."
else
    echo "Homebrew is already installed."
fi

# Step 0: Create a new project directory
PROJECT_NAME="my_python"
PROJECT_PATH="$HOME/$PROJECT_NAME"

echo "Creating project directory in home: $PROJECT_PATH"
mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH" || exit

# Step 1: Install Python using Homebrew
if ! brew list python &>/dev/null; then
    echo "Installing Python via Homebrew..."
    brew install python
else
    echo "Python is already installed via Homebrew."
fi

# Step 2: Create a virtual environment
echo "Creating virtual environment in ./venv"
python3 -m venv venv

# Step 2.1: Upgrade pip inside the virtual environment (recommended)
echo "Upgrading pip inside virtual environment"
./venv/bin/pip install --upgrade pip

# Step 3: Install Python packages using the venv's pip without activating
echo "Installing packages"
./venv/bin/pip install numpy pandas matplotlib # vtk pyvista

# Step 4: Freeze installed packages to requirements.txt
echo "Saving installed packages to requirements.txt"
./venv/bin/pip freeze > requirements.txt

# Done message and instructions for activation
echo ""
echo "Setup complete!"
echo "To start using the virtual environment, activate it by running:"
echo "  source $PROJECT_NAME/venv/bin/activate"
echo "Your installed packages are listed in $PROJECT_NAME/requirements.txt"
echo " to recreate the same environment later, run:"
echo "  pip install -r requirements.txt"
echo ""
