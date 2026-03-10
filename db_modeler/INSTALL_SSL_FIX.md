# Fixing SSL Certificate Errors in Conda Environment

## Quick Fix (Temporary - for development only)

### Option 1: Bypass SSL verification (NOT recommended for production)

```bash
# Activate your conda environment
conda activate db_model

# Install with SSL verification disabled (temporary)
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Option 2: Update certificates

```bash
# Update conda certificates
conda update --all
conda update certifi

# Or reinstall certifi
conda install -c anaconda certifi
```

### Option 3: Use conda-forge packages (Recommended)

```bash
conda activate db_model

# Install core packages via conda
conda install -c conda-forge fastapi uvicorn pydantic python-dotenv jinja2

# Install Snowflake connector
conda install -c conda-forge snowflake-connector-python

# Install OpenAI (if available via conda, otherwise use pip with trusted hosts)
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org openai anthropic

# Install remaining packages
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pydantic-settings httpx aiofiles
```

## Permanent Fix

### Windows: Update CA Certificates

1. **Download latest certificates:**
   ```powershell
   # Download certifi bundle
   python -m pip install --upgrade certifi
   ```

2. **Set environment variable:**
   ```powershell
   $env:SSL_CERT_FILE = (python -m certifi)
   ```

3. **Or add to your conda environment:**
   ```bash
   conda env config vars set SSL_CERT_FILE=$(python -m certifi)
   conda deactivate
   conda activate db_model
   ```

### Alternative: Use conda's pip

```bash
conda activate db_model
conda install pip
python -m pip install -r requirements.txt
```

## Minimal Installation (Skip problematic packages)

If SSL issues persist, install only essential packages:

```bash
conda activate db_model

# Core packages
conda install -c conda-forge fastapi uvicorn pydantic python-dotenv

# Snowflake
conda install -c conda-forge snowflake-connector-python

# AI packages (use pip with trusted hosts)
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org openai anthropic pydantic-settings httpx aiofiles jinja2
```

## Verify Installation

```bash
python -c "import fastapi, snowflake.connector, openai; print('All packages installed!')"
```
