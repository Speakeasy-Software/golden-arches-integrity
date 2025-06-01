#!/bin/bash

# Golden Arches Integrity - Azure Deployment Script
# This script deploys the infrastructure and application to Azure

set -e

# Configuration
RESOURCE_GROUP="golden-arches-rg"
LOCATION="westus2"
ENVIRONMENT="prod"
APP_NAME="golden-arches"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo_error "Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo_error "Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

echo_info "Starting deployment to Azure..."

# Create resource group if it doesn't exist
echo_info "Creating resource group: $RESOURCE_GROUP"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

# Deploy infrastructure using ARM template
echo_info "Deploying infrastructure..."
DEPLOYMENT_OUTPUT=$(az deployment group create \
    --resource-group $RESOURCE_GROUP \
    --template-file infrastructure/azure-resources.json \
    --parameters appName=$APP_NAME environment=$ENVIRONMENT \
    --output json)

# Extract outputs
WEB_APP_URL=$(echo $DEPLOYMENT_OUTPUT | jq -r '.properties.outputs.webAppUrl.value')
STATIC_WEB_APP_URL=$(echo $DEPLOYMENT_OUTPUT | jq -r '.properties.outputs.staticWebAppUrl.value')
STORAGE_ACCOUNT=$(echo $DEPLOYMENT_OUTPUT | jq -r '.properties.outputs.storageAccountName.value')
CONTAINER_REGISTRY=$(echo $DEPLOYMENT_OUTPUT | jq -r '.properties.outputs.containerRegistryLoginServer.value')
ML_WORKSPACE=$(echo $DEPLOYMENT_OUTPUT | jq -r '.properties.outputs.mlWorkspaceName.value')

echo_info "Infrastructure deployed successfully!"
echo_info "Web App URL: $WEB_APP_URL"
echo_info "Static Web App URL: $STATIC_WEB_APP_URL"
echo_info "Storage Account: $STORAGE_ACCOUNT"
echo_info "Container Registry: $CONTAINER_REGISTRY"
echo_info "ML Workspace: $ML_WORKSPACE"

# Build and push Docker image
echo_info "Building and pushing Docker image..."
cd backend

# Login to Azure Container Registry
az acr login --name ${CONTAINER_REGISTRY%%.azurecr.io}

# Build and push image
docker build -t $CONTAINER_REGISTRY/golden-arches-backend:latest .
docker push $CONTAINER_REGISTRY/golden-arches-backend:latest

echo_info "Docker image pushed successfully!"

# Update App Service to use the new image
echo_info "Updating App Service..."
az webapp config container set \
    --name "${APP_NAME}-${ENVIRONMENT}-backend" \
    --resource-group $RESOURCE_GROUP \
    --docker-custom-image-name "$CONTAINER_REGISTRY/golden-arches-backend:latest"

# Restart the web app
az webapp restart \
    --name "${APP_NAME}-${ENVIRONMENT}-backend" \
    --resource-group $RESOURCE_GROUP

echo_info "App Service updated successfully!"

# Test the deployment
echo_info "Testing deployment..."
sleep 30  # Wait for app to start

HEALTH_CHECK_URL="${WEB_APP_URL}/health"
if curl -f -s "$HEALTH_CHECK_URL" > /dev/null; then
    echo_info "Health check passed! ✅"
    echo_info "Backend is running at: $WEB_APP_URL"
    echo_info "API Documentation: ${WEB_APP_URL}/docs"
else
    echo_error "Health check failed! ❌"
    echo_error "Please check the application logs in Azure Portal"
    exit 1
fi

echo_info "Deployment completed successfully! 🚀"
echo_info ""
echo_info "Next steps:"
echo_info "1. Configure GitHub secrets for CI/CD:"
echo_info "   - AZURE_REGISTRY_LOGIN_SERVER: $CONTAINER_REGISTRY"
echo_info "   - AZURE_WEBAPP_PUBLISH_PROFILE: (download from Azure Portal)"
echo_info "   - AZURE_STATIC_WEB_APPS_API_TOKEN: (get from Static Web App)"
echo_info ""
echo_info "2. Update frontend environment variables:"
echo_info "   - VITE_API_BASE_URL: $WEB_APP_URL"
echo_info ""
echo_info "3. Configure Azure ML workspace and upload initial models" 