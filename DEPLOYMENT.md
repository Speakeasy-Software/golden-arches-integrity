# Golden Arches Integrity - Deployment Guide

This guide covers the deployment of the Golden Arches Integrity application to Azure.

## 🏗️ Architecture Overview

The application consists of:

- **Frontend**: React SPA deployed to Azure Static Web Apps
- **Backend**: FastAPI application deployed to Azure App Service (containerized)
- **Storage**: Azure Blob Storage for images and annotations
- **ML Workspace**: Azure Machine Learning for model training and inference
- **Monitoring**: Application Insights for logging and metrics
- **Registry**: Azure Container Registry for Docker images

## 📋 Prerequisites

1. **Azure CLI** installed and configured
2. **Docker** installed for building images
3. **Node.js 18+** for frontend builds
4. **Python 3.11+** for backend development
5. **Azure subscription** with appropriate permissions

## 🚀 Quick Deployment

### Option 1: Automated Deployment Script

```bash
# Clone the repository
git clone https://github.com/Speakeasy-Software/golden-arches-integrity.git
cd golden-arches-integrity

# Login to Azure
az login

# Run the deployment script
./scripts/deploy.sh
```

### Option 2: Manual Deployment

#### Step 1: Deploy Infrastructure

```bash
# Create resource group
az group create --name golden-arches-rg --location westus2

# Deploy ARM template
az deployment group create \
  --resource-group golden-arches-rg \
  --template-file infrastructure/azure-resources.json \
  --parameters appName=golden-arches environment=prod
```

#### Step 2: Build and Deploy Backend

```bash
cd backend

# Build Docker image
docker build -t golden-arches-backend .

# Tag and push to Azure Container Registry
az acr login --name goldenarchesprodacr
docker tag golden-arches-backend goldenarchesprodacr.azurecr.io/golden-arches-backend:latest
docker push goldenarchesprodacr.azurecr.io/golden-arches-backend:latest

# Update App Service
az webapp config container set \
  --name golden-arches-prod-backend \
  --resource-group golden-arches-rg \
  --docker-custom-image-name goldenarchesprodacr.azurecr.io/golden-arches-backend:latest
```

#### Step 3: Deploy Frontend

```bash
cd frontend

# Install dependencies
npm install

# Build for production
VITE_API_BASE_URL=https://golden-arches-prod-backend.azurewebsites.net npm run build

# Deploy to Static Web Apps (automated via GitHub Actions)
```

## 🔧 Configuration

### Environment Variables

#### Backend (Azure App Service Application Settings)

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Storage connection string | `DefaultEndpointsProtocol=https;AccountName=...` |
| `AZURE_ML_WORKSPACE_NAME` | Azure ML workspace name | `golden-arches-prod-ml` |
| `AZURE_ML_RESOURCE_GROUP` | Resource group name | `golden-arches-rg` |
| `AZURE_ML_SUBSCRIPTION_ID` | Azure subscription ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `SECRET_KEY` | Application secret key | `your-secret-key-here` |
| `DEBUG` | Debug mode | `false` |

#### Frontend (Build-time Environment Variables)

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `https://golden-arches-prod-backend.azurewebsites.net` |
| `VITE_APP_NAME` | Application name | `Golden Arches Integrity` |
| `VITE_ENVIRONMENT` | Environment name | `production` |

### GitHub Secrets (for CI/CD)

| Secret | Description | How to Get |
|--------|-------------|------------|
| `AZURE_REGISTRY_LOGIN_SERVER` | Container registry URL | From ARM template output |
| `AZURE_REGISTRY_USERNAME` | Registry username | From Azure Portal |
| `AZURE_REGISTRY_PASSWORD` | Registry password | From Azure Portal |
| `AZURE_WEBAPP_PUBLISH_PROFILE` | App Service publish profile | Download from Azure Portal |
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | Static Web Apps deployment token | From Azure Portal |

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy-backend.yml`) automatically:

1. **Tests** the backend on every PR
2. **Builds** and pushes Docker images on main branch
3. **Deploys** to Azure App Service
4. **Deploys** frontend to Static Web Apps

### Triggering Deployments

- **Backend**: Push to `main` branch with changes in `backend/` folder
- **Frontend**: Push to `main` branch with changes in `frontend/` folder
- **Manual**: Use GitHub Actions "workflow_dispatch" trigger

## 🏥 Health Checks and Monitoring

### Health Endpoints

- **Backend Health**: `https://golden-arches-prod-backend.azurewebsites.net/health`
- **API Documentation**: `https://golden-arches-prod-backend.azurewebsites.net/docs`

### Monitoring

- **Application Insights**: Automatic logging and metrics
- **Container Logs**: Available in Azure Portal
- **Performance Metrics**: CPU, memory, response times

### Alerts

Configure alerts for:
- High error rates (>5%)
- Slow response times (>2s)
- High CPU usage (>80%)
- Storage quota exceeded

## 🔒 Security

### Authentication

- **Azure AD**: Integrated authentication for admin access
- **API Keys**: For programmatic access
- **RBAC**: Role-based access control

### Network Security

- **HTTPS Only**: All traffic encrypted
- **CORS**: Configured for frontend domain only
- **Private Endpoints**: For storage and ML workspace (optional)

### Data Protection

- **Encryption at Rest**: Azure Storage encryption
- **Encryption in Transit**: TLS 1.2+
- **Access Logs**: All API access logged

## 🧪 Testing Deployment

### Automated Tests

```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

### Manual Testing

1. **Upload Test**: Upload a sample image
2. **Analysis Test**: Run compliance analysis
3. **Annotation Test**: Create and edit annotations
4. **Dashboard Test**: Verify statistics display

## 🐛 Troubleshooting

### Common Issues

#### Backend Not Starting

```bash
# Check application logs
az webapp log tail --name golden-arches-prod-backend --resource-group golden-arches-rg

# Check container logs
az webapp log download --name golden-arches-prod-backend --resource-group golden-arches-rg
```

#### Frontend Build Failures

```bash
# Check environment variables
echo $VITE_API_BASE_URL

# Verify API connectivity
curl https://golden-arches-prod-backend.azurewebsites.net/health
```

#### Azure ML Issues

```bash
# Verify workspace access
az ml workspace show --name golden-arches-prod-ml --resource-group golden-arches-rg
```

### Performance Issues

- **Scale Up**: Increase App Service plan size
- **Scale Out**: Add more instances
- **CDN**: Enable Azure CDN for static assets
- **Caching**: Implement Redis cache for API responses

## 📊 Cost Optimization

### Resource Sizing

- **Development**: F1 App Service plan, Basic storage
- **Production**: B1+ App Service plan, Standard storage
- **Enterprise**: P1+ App Service plan, Premium storage

### Cost Monitoring

- Set up budget alerts
- Use Azure Cost Management
- Monitor resource utilization

## 🔄 Updates and Maintenance

### Regular Updates

- **Dependencies**: Update monthly
- **Security Patches**: Apply immediately
- **Azure Services**: Follow Azure update schedule

### Backup Strategy

- **Code**: Git repository (GitHub)
- **Data**: Azure Blob Storage geo-replication
- **Configuration**: ARM templates and scripts

### Disaster Recovery

- **Multi-region**: Deploy to secondary region
- **Database Backup**: Regular automated backups
- **Monitoring**: Health checks and alerts

## 📞 Support

For deployment issues:

1. Check this documentation
2. Review Azure Portal logs
3. Check GitHub Issues
4. Contact the development team

---

**Last Updated**: June 2025  
**Version**: 1.0.0 