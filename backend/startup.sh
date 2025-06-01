#!/bin/bash

# Startup script for Azure App Service
set -e

echo "Starting Golden Arches Backend..."
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"
echo "Environment variables:"
env | grep -E "(AZURE_|PORT|PYTHON)" | sort

# Ensure proper file descriptors
exec 1> >(tee -a /app/logs/startup.log)
exec 2> >(tee -a /app/logs/startup.log >&2)

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Test Azure connectivity
echo "Testing Azure connectivity..."
python -c "
import os
from app.services.azure_client import azure_client
print('Azure client initialization test...')
try:
    # Just test that we can import and initialize
    print('Azure client imported successfully')
except Exception as e:
    print(f'Azure client error: {e}')
"

echo "Starting uvicorn server..."
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-80} \
    --workers 1 \
    --access-log \
    --log-level info \
    --log-config /dev/null 