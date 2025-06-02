#!/bin/bash
set -e

echo "Starting Golden Arches Backend..."
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"
echo "Environment variables:"
env | grep -E "(AZURE_|PORT|PYTHON)" | sort

# Use PORT environment variable from Azure App Service, fallback to 80
APP_PORT=${PORT:-80}
echo "Using port: $APP_PORT"

# Skip Azure ML client initialization in App Service to avoid chmod permission errors
export SKIP_AZURE_ML_CLIENT=true
echo "Set SKIP_AZURE_ML_CLIENT=true to avoid permission issues"

# Test Azure connectivity
echo "Testing Azure connectivity..."
python -c "
try:
    from app.core.azure_client import azure_client
    print('Azure client imported successfully')
except Exception as e:
    print(f'Azure client error: {e}')
"

echo "Starting uvicorn server on port $APP_PORT..."
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port $APP_PORT \
    --workers 1 \
    --log-level info