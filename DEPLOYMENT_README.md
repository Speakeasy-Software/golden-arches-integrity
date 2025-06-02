# Golden Arches Integrity - Complete Deployment Guide

## 🏗️ **Architecture Overview**

The Golden Arches Integrity application uses a modern cloud-native architecture deployed on Azure:

- **Frontend**: React SPA → Azure Static Web Apps
- **Backend**: FastAPI (containerized) → Azure App Service
- **Storage**: Azure Blob Storage for images and annotations
- **Registry**: Azure Container Registry for Docker images
- **CI/CD**: GitHub Actions for automated deployment
- **Authentication**: Session-based with HTTP-only cookies
- **ML Workspace**: Azure Machine Learning (Phase 2+)

## 🚀 **Automated Deployment Pipeline**

### **GitHub Actions Workflow**

The deployment is fully automated via `.github/workflows/deploy-backend.yml`:

```yaml
name: Deploy Backend and Frontend

on:
  push:
    branches: [ master ]
  workflow_dispatch:  # Manual trigger capability

jobs:
  deploy-backend:     # Containerized FastAPI to Azure App Service
  deploy-frontend:    # React SPA to Azure Static Web Apps  
  verify-deployment:  # Automated health checks and endpoint testing
```

### **Deployment Triggers**

- **Automatic**: Push to `master` branch
- **Manual**: GitHub Actions → "Run workflow" button
- **Webhook**: Can be configured for external triggers

## 🔧 **Backend Deployment (Azure App Service)**

### **Container Build Process**

1. **Docker Build**: Multi-stage build with Python 3.11-slim
2. **Dependencies**: Includes OpenCV graphics libraries (fixes 503 errors)
3. **Platform**: `linux/amd64` (64-bit architecture)
4. **Registry**: Push to Azure Container Registry
5. **Deployment**: Azure App Service pulls and runs container

### **Critical Configuration**

```bash
# 64-bit worker process (prevents 503 errors)
az webapp config set --use-32bit-worker-process false

# Explicit port configuration
az webapp config appsettings set --settings WEBSITES_PORT=80

# Startup command
az webapp config set --startup-file "./startup.sh"
```

### **Environment Variables**

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_STORAGE_CONNECTION_STRING` | Blob storage connection | ✅ |
| `SECRET_KEY` | Application secret key | ✅ |
| `SKIP_AZURE_ML_CLIENT` | Skip ML client in App Service | ✅ |
| `WEBSITES_PORT` | Application port (80) | ✅ |

### **Health Monitoring**

- **Endpoint**: `https://golden-arches-prod-backend.azurewebsites.net/health`
- **Response**: `{"status":"healthy","app_name":"Golden Arches Integrity","version":"1.0.0"}`
- **Monitoring**: Automated health checks in GitHub Actions

## 🌐 **Frontend Deployment (Azure Static Web Apps)**

### **Build Process**

1. **Node.js Setup**: Version 18 with npm caching
2. **Dependencies**: `npm ci` for clean install
3. **Build**: Vite production build with environment variables
4. **Optimization**: Only deploy `dist/` contents (4-5 files vs thousands)

### **File Structure**

```
deployment-temp/
├── index.html                    # Main SPA entry point
├── assets/
│   ├── index-[hash].js          # Bundled JavaScript
│   └── index-[hash].css         # Bundled CSS
└── .staticwebapp.config.json    # SPA routing configuration
```

### **SPA Routing Configuration**

```json
{
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["anonymous"]
    },
    {
      "route": "/*",
      "serve": "/index.html",
      "statusCode": 200
    }
  ],
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/assets/*", "*.{css,scss,js,png,gif,ico,jpg,svg}"]
  }
}
```

### **Environment Variables**

| Variable | Description | Value |
|----------|-------------|-------|
| `VITE_API_BASE_URL` | Backend API URL | `https://golden-arches-prod-backend.azurewebsites.net` |
| `NODE_ENV` | Build environment | `production` |

## 🔐 **Authentication System**

### **Session-Based Authentication**

- **Method**: HTTP-only cookies with 8-hour expiration
- **Security**: Secure, SameSite, HttpOnly flags
- **Storage**: Server-side session management
- **CSRF**: Built-in protection via session tokens

### **User Roles & Permissions**

| Role | Username | Permissions |
|------|----------|-------------|
| **Training Authority** | `sven` | Full control, training decisions |
| **Senior Reviewer** | `huan`, `george` | Full access, approval authority |
| **Guest Reviewer** | `guest` | Limited access, requires approval |

### **Authentication Endpoints**

```bash
# Login
POST /auth/login
Content-Type: application/json
{"username": "sven", "password": "password123"}

# Logout  
POST /auth/logout

# Session check
GET /auth/me

# User management
GET /auth/users
```

## 💾 **Storage Configuration**

### **Azure Blob Storage**

- **Container**: `uploads` for asset storage
- **Access**: Private with SAS tokens
- **File Types**: PNG, JPG, JPEG, WebP, SVG, AI, PSD, PDF, DOC, DOCX, ZIP
- **Size Limit**: 100MB per file

### **Storage Structure**

```
uploads/
├── assets/
│   ├── [asset-id]/
│   │   ├── original.[ext]
│   │   ├── processed.[ext]
│   │   └── metadata.json
├── heritage-marks/
│   └── [converted PNG files]
└── annotations/
    └── [asset-id].json
```

### **Connection Configuration**

```python
# Environment variable
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"

# Usage in application
from app.core.azure_client import azure_client
blob_url = azure_client.upload_file(file_data, filename)
```

## 🔑 **Required GitHub Secrets**

### **Azure Container Registry**

```bash
AZURE_REGISTRY_LOGIN_SERVER=goldenarchesprodacr.azurecr.io
AZURE_REGISTRY_USERNAME=[from Azure Portal]
AZURE_REGISTRY_PASSWORD=[from Azure Portal]
```

### **Azure App Service**

```bash
AZURE_WEBAPP_PUBLISH_PROFILE=[download from Azure Portal]
```

### **Azure Static Web Apps**

```bash
AZURE_STATIC_WEB_APPS_API_TOKEN=[from Azure Portal]
```

### **How to Obtain Secrets**

1. **Container Registry Credentials**:
   ```bash
   az acr credential show --name goldenarchesprodacr
   ```

2. **App Service Publish Profile**:
   - Azure Portal → App Service → Get publish profile

3. **Static Web Apps Token**:
   - Azure Portal → Static Web App → Manage deployment token

## 🧪 **Testing & Verification**

### **Automated Health Checks**

The deployment includes automated verification:

```bash
# Backend health
curl https://golden-arches-prod-backend.azurewebsites.net/health

# Frontend accessibility  
curl https://green-glacier-01f996d1e.6.azurestaticapps.net/

# API documentation
curl https://golden-arches-prod-backend.azurewebsites.net/docs
```

### **QA Portal Testing**

```bash
# Authentication test
curl -X POST https://golden-arches-prod-backend.azurewebsites.net/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"sven","password":"password123"}' \
  -c cookies.txt

# Workload management test
curl https://golden-arches-prod-backend.azurewebsites.net/api/v1/review/workloads \
  -b cookies.txt

# Frontend QA Portal access
# Visit: https://green-glacier-01f996d1e.6.azurestaticapps.net/login
```

### **Manual Testing Checklist**

- [ ] Backend health endpoint responds
- [ ] Frontend loads without errors
- [ ] Login functionality works
- [ ] QA Portal dashboard accessible
- [ ] File upload functionality
- [ ] API documentation available
- [ ] Session management working
- [ ] Role-based permissions enforced

## 🐛 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **503 Application Error (Backend)**

```bash
# Check worker process architecture
az webapp config show --name golden-arches-prod-backend --query "use32BitWorkerProcess"

# Fix: Ensure 64-bit
az webapp config set --name golden-arches-prod-backend --use-32bit-worker-process false
```

#### **"Too Many Static Files" (Frontend)**

- **Cause**: Deploying `node_modules` instead of `dist/`
- **Fix**: Use clean deployment directory (implemented in workflow)
- **Verification**: Check file count in deployment logs

#### **Container Startup Issues**

```bash
# Check container logs
az webapp log tail --name golden-arches-prod-backend

# Common fixes
az webapp config appsettings set --settings WEBSITES_PORT=80
az webapp config set --startup-file "./startup.sh"
```

#### **Authentication Issues**

- **CORS**: Ensure frontend domain is in CORS settings
- **Cookies**: Check Secure/SameSite flags
- **Sessions**: Verify session storage configuration

### **Deployment Monitoring**

```bash
# GitHub Actions status
gh run list --limit 5

# Real-time logs
gh run view --log

# Azure App Service logs
az webapp log tail --name golden-arches-prod-backend
```

## 📊 **Performance & Scaling**

### **Current Configuration**

- **App Service Plan**: S1 (1 CPU, 1.75GB RAM)
- **Static Web Apps**: Global CDN distribution
- **Container Registry**: Standard tier
- **Storage**: Standard performance tier

### **Scaling Considerations**

- **Horizontal**: Multiple App Service instances
- **Vertical**: Upgrade to S2/S3 for more resources
- **CDN**: Already included with Static Web Apps
- **Database**: Consider Azure SQL for production scale

## 🔄 **Deployment Best Practices**

### **Pre-Deployment**

1. **Test Locally**: Ensure all tests pass
2. **Environment Variables**: Verify all secrets configured
3. **Dependencies**: Check for security vulnerabilities
4. **Build**: Confirm clean build without errors

### **During Deployment**

1. **Monitor**: Watch GitHub Actions progress
2. **Health Checks**: Verify automated checks pass
3. **Rollback Plan**: Keep previous version ready
4. **Communication**: Notify team of deployment

### **Post-Deployment**

1. **Verification**: Run full test suite
2. **Monitoring**: Check application metrics
3. **Documentation**: Update deployment notes
4. **Backup**: Ensure data backup completed

## 🚨 **Emergency Procedures**

### **Rollback Process**

```bash
# Redeploy previous container version
az webapp config container set \
  --name golden-arches-prod-backend \
  --docker-custom-image-name goldenarchesprodacr.azurecr.io/golden-arches-backend:[previous-sha]

# Restart application
az webapp restart --name golden-arches-prod-backend
```

### **Quick Health Check**

```bash
#!/bin/bash
echo "🔍 Health Check Starting..."

# Backend
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://golden-arches-prod-backend.azurewebsites.net/health)
echo "Backend: $BACKEND_STATUS"

# Frontend  
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://green-glacier-01f996d1e.6.azurestaticapps.net/)
echo "Frontend: $FRONTEND_STATUS"

if [ "$BACKEND_STATUS" = "200" ] && [ "$FRONTEND_STATUS" = "200" ]; then
  echo "✅ All systems operational"
else
  echo "❌ Issues detected - check logs"
fi
```

## 📚 **Additional Resources**

- **Azure App Service**: [Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- **Azure Static Web Apps**: [Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- **GitHub Actions**: [Documentation](https://docs.github.com/en/actions)
- **FastAPI Deployment**: [Guide](https://fastapi.tiangolo.com/deployment/)
- **React Deployment**: [Guide](https://create-react-app.dev/docs/deployment/)

---

**📝 Last Updated**: Phase 1.2 QA Portal Implementation
**🔄 Next Review**: Phase 2 ML Pipeline Integration 