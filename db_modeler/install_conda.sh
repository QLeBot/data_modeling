#!/bin/bash
# Bash script to install DB Modeler in conda environment with SSL fix
# Usage: bash install_conda.sh

echo "Installing DB Modeler in conda environment..."

# Activate conda environment
echo "Activating conda environment: db_model"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate db_model

if [ $? -ne 0 ]; then
    echo "Error: Could not activate conda environment 'db_model'"
    echo "Please create it first: conda create -n db_model python=3.10"
    exit 1
fi

# Update certificates
echo "Updating certificates..."
conda update -y certifi
python -m pip install --upgrade certifi

# Install via conda-forge where possible
echo "Installing packages via conda-forge..."
conda install -y -c conda-forge fastapi uvicorn pydantic python-dotenv jinja2 httpx aiofiles

# Install Snowflake connector
echo "Installing Snowflake connector..."
conda install -y -c conda-forge snowflake-connector-python

# Install remaining packages via pip with trusted hosts
echo "Installing remaining packages via pip..."
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pydantic-settings==2.1.0
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org openai==1.3.5
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org anthropic==0.7.8

# Verify installation
echo "Verifying installation..."
python -c "import fastapi, snowflake.connector, openai; print('✓ All packages installed successfully!')"

if [ $? -eq 0 ]; then
    echo "Installation complete!"
else
    echo "Some packages may not have installed correctly. Check errors above."
fi
