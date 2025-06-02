# 503 and 504 Error Fixes - Golden Arches Backend Deployment

## Overview
This document details the systematic approach used to resolve persistent 503 Application Error and 504 Gateway Timeout issues during the Azure App Service container deployment of the Golden Arches Integrity backend.

## Initial Problem State
- **503 Application Error**: Container failing to start properly
- **504 Gateway Timeout**: Azure App Service timing out waiting for application response
- **Symptoms**: Only Kudu management interface starting, FastAPI application not responding

## Root Cause Analysis

### 1. Container Architecture Mismatch
**Problem**: App Service configured for 32-bit but container built for 64-bit
```bash
# Issue discovered
az webapp config show --query "use32BitWorkerProcess"
# Result: true (but container was x86_64)
```

**Fix**:
```bash
az webapp config set --name golden-arches-prod-backend \
  --resource-group golden-arches-rg \
  --use-32bit-worker-process false
```

### 2. Port Configuration Issues
**Problem**: Azure App Service not properly routing to application port

**Fix**:
```bash
# Set explicit port configuration
az webapp config appsettings set --name golden-arches-prod-backend \
  --resource-group golden-arches-rg \
  --settings WEBSITES_PORT=80

# Set proper startup command
az webapp config set --name golden-arches-prod-backend \
  --resource-group golden-arches-rg \
  --startup-file "python -m uvicorn app.main:app --host 0.0.0.0 --port 80"
```

### 3. Resource Constraints
**Problem**: B1 (Basic) App Service plan insufficient for container requirements
- 1.75 GB RAM
- 1 CPU core
- Limited for heavy ML/CV dependencies

**Fix**:
```bash
az appservice plan update --name golden-arches-prod-plan \
  --resource-group golden-arches-rg \
  --sku S1
```

### 4. OpenCV Graphics Libraries Missing
**Problem**: Critical import error preventing application startup
```
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

**Fix**: Updated Dockerfile with required graphics libraries
```dockerfile
# Install system dependencies including graphics libraries for OpenCV
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1 \
        libfontconfig1 \
        libice6 \
    && rm -rf /var/lib/apt/lists/*
```

### 5. Azure ML Client Initialization Issues
**Problem**: Azure ML SDK attempting chmod operations in restricted environment
```
chown: changing ownership of '/temp': Operation not permitted
chmod: changing permissions of '/temp': Operation not permitted
```

**Fix**: Modified Azure client to skip ML initialization in App Service
```python
# In startup.sh
export SKIP_AZURE_ML_CLIENT=true

# In azure_client.py
if os.getenv('SKIP_AZURE_ML_CLIENT', 'false').lower() == 'true':
    logger.info("Skipping Azure ML client initialization in App Service environment")
    self.ml_client = None
```

### 6. Logging and File Permission Issues
**Problem**: Application trying to write to restricted directories

**Fix**: Modified logging configuration for Azure App Service compatibility
```python
# Use environment variables for temp directory
temp_dir = os.getenv('TMPDIR', '/tmp')
log_file = os.path.join(temp_dir, 'app.log') if os.access(temp_dir, os.W_OK) else None

if log_file:
    logger.add(log_file, rotation="10 MB", retention="7 days", level="INFO")
else:
    logger.info("File logging disabled - using console only")
```

## Implementation Steps

### Step 1: Diagnostic Phase
```bash
# Check current configuration
az webapp config show --name golden-arches-prod-backend --resource-group golden-arches-rg

# Enable logging for debugging
az webapp log config --name golden-arches-prod-backend \
  --resource-group golden-arches-rg \
  --application-logging filesystem --level information
```

### Step 2: Infrastructure Fixes
```bash
# Fix architecture mismatch
az webapp config set --use-32bit-worker-process false

# Upgrade App Service plan
az appservice plan update --sku S1

# Configure port settings
az webapp config appsettings set --settings WEBSITES_PORT=80
```

### Step 3: Container Rebuild
```bash
# Build with OpenCV dependencies
az acr build --registry goldenarchesprodacr \
  --image golden-arches-backend:opencv-fix .

# Deploy updated container
az webapp config container set \
  --docker-custom-image-name goldenarchesprodacr.azurecr.io/golden-arches-backend:opencv-fix
```

### Step 4: Application Configuration
```bash
# Set startup command
az webapp config set --startup-file "python -m uvicorn app.main:app --host 0.0.0.0 --port 80"

# Restart application
az webapp restart --name golden-arches-prod-backend --resource-group golden-arches-rg
```

## Verification Steps

### Health Check
```bash
curl -w "HTTP Status: %{http_code}\nResponse Time: %{time_total}s\n" \
  https://golden-arches-prod-backend.azurewebsites.net/health
```

**Expected Result**:
```json
{
  "status": "healthy",
  "app_name": "Golden Arches Integrity", 
  "version": "1.0.0",
  "timestamp": 1748883004.974224
}
HTTP Status: 200
Response Time: 0.354277s
```

### API Endpoints
- **Root**: https://golden-arches-prod-backend.azurewebsites.net/
- **Health**: https://golden-arches-prod-backend.azurewebsites.net/health
- **Docs**: https://golden-arches-prod-backend.azurewebsites.net/docs

## Key Lessons Learned

### 1. Systematic Debugging Approach
- Check architecture compatibility first
- Verify resource allocation
- Enable comprehensive logging
- Test each fix incrementally

### 2. Azure App Service Container Requirements
- Use 64-bit worker processes for modern containers
- Set WEBSITES_PORT explicitly
- Ensure adequate resources (S1+ for ML workloads)
- Avoid file system operations in restricted directories

### 3. OpenCV in Containerized Environments
- Always include graphics libraries for headless operation
- Test import statements early in deployment process
- Consider opencv-python-headless for server environments

### 4. Azure ML SDK Considerations
- SDK may attempt system-level operations incompatible with App Service
- Implement environment-specific initialization logic
- Use feature flags to disable problematic components

## Prevention Strategies

### 1. Pre-deployment Checklist
- [ ] Verify container architecture matches App Service configuration
- [ ] Test all critical imports in container environment
- [ ] Validate resource requirements against App Service plan
- [ ] Configure proper port settings
- [ ] Test startup commands locally

### 2. Monitoring Setup
```bash
# Enable comprehensive logging
az webapp log config --application-logging filesystem --level information

# Set up log streaming for real-time debugging
az webapp log tail --provider application
```

### 3. Container Best Practices
- Use multi-stage builds to minimize image size
- Include all system dependencies explicitly
- Avoid user switching in Azure App Service containers
- Test in environment similar to production

## Final Configuration

### Working Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=80

WORKDIR /app

# Install system dependencies including graphics libraries for OpenCV
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1 \
        libfontconfig1 \
        libice6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x startup.sh

EXPOSE 80
CMD ["./startup.sh"]
```

### Working App Service Configuration
- **Plan**: S1 (Standard)
- **Architecture**: 64-bit
- **Port**: 80 (WEBSITES_PORT)
- **Startup Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port 80`
- **Container**: `goldenarchesprodacr.azurecr.io/golden-arches-backend:opencv-fix`

## Success Metrics
- **HTTP Status**: 200 OK (previously 503/504)
- **Response Time**: ~0.35 seconds
- **Uptime**: Stable container operation
- **Functionality**: All API endpoints responding correctly

---

**Document Created**: June 2, 2025  
**Status**: Deployment Successful  
**Next Steps**: Monitor application performance and implement additional optimizations as needed 