# PowerShell script to install DB Modeler in conda environment with SSL fix
# Usage: .\install_conda.ps1

Write-Host "Installing DB Modeler in conda environment..." -ForegroundColor Green

# Activate conda environment
Write-Host "Activating conda environment: db_model" -ForegroundColor Yellow
conda activate db_model

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Could not activate conda environment 'db_model'" -ForegroundColor Red
    Write-Host "Please create it first: conda create -n db_model python=3.10" -ForegroundColor Yellow
    exit 1
}

# Update certificates first
Write-Host "Updating certificates..." -ForegroundColor Yellow
conda update -y certifi
python -m pip install --upgrade certifi

# Set trusted hosts for pip
$trustedHosts = "--trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org"

# Install via conda-forge where possible
Write-Host "Installing packages via conda-forge..." -ForegroundColor Yellow
conda install -y -c conda-forge fastapi uvicorn pydantic python-dotenv jinja2 httpx aiofiles

# Install Snowflake connector
Write-Host "Installing Snowflake connector..." -ForegroundColor Yellow
conda install -y -c conda-forge snowflake-connector-python

# Install remaining packages via pip with trusted hosts
Write-Host "Installing remaining packages via pip..." -ForegroundColor Yellow
python -m pip install $trustedHosts pydantic-settings==2.1.0
python -m pip install $trustedHosts openai==1.3.5
python -m pip install $trustedHosts anthropic==0.7.8

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
python -c "import fastapi, snowflake.connector, openai; print('✓ All packages installed successfully!')"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Installation complete!" -ForegroundColor Green
} else {
    Write-Host "Some packages may not have installed correctly. Check errors above." -ForegroundColor Red
}
