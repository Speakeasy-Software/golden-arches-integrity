# GitHub Secrets Setup Guide

This guide will help you configure the GitHub secrets required for the CI/CD pipeline.

## 🔐 Required GitHub Secrets

Go to your GitHub repository: `https://github.com/Speakeasy-Software/golden-arches-integrity`

Navigate to: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### 1. Azure Container Registry Secrets

**AZURE_REGISTRY_LOGIN_SERVER**
```
goldenarchesprodacr.azurecr.io
```

**AZURE_REGISTRY_USERNAME**
```
goldenarchesprodacr
```

**AZURE_REGISTRY_PASSWORD**
```
eU9IubsoVUr2X3RepOYcvF1hkAx4QCz3W2CV0kmNpk+ACRAnn0xy
```

### 2. Azure App Service Secret

**AZURE_WEBAPP_PUBLISH_PROFILE**
```xml
<publishData><publishProfile profileName="golden-arches-prod-backend - Web Deploy" publishMethod="MSDeploy" publishUrl="golden-arches-prod-backend.scm.azurewebsites.net:443" msdeploySite="golden-arches-prod-backend" userName="$golden-arches-prod-backend" userPWD="27y7NFFj9mHsNakb0Zz2YnggeFyaimr2rkq2dGmu5yX4riNdikwKgX9bivQt" destinationAppUrl="https://golden-arches-prod-backend.azurewebsites.net" SQLServerDBConnectionString="" mySQLDBConnectionString="" hostingProviderForumLink="" controlPanelLink="https://portal.azure.com" webSystem="WebSites"><databases /></publishProfile><publishProfile profileName="golden-arches-prod-backend - FTP" publishMethod="FTP" publishUrl="ftps://waws-prod-mwh-129.ftp.azurewebsites.windows.net/site/wwwroot" ftpPassiveMode="True" userName="golden-arches-prod-backend\$golden-arches-prod-backend" userPWD="27y7NFFj9mHsNakb0Zz2YnggeFyaimr2rkq2dGmu5yX4riNdikwKgX9bivQt" destinationAppUrl="https://golden-arches-prod-backend.azurewebsites.net" SQLServerDBConnectionString="" mySQLDBConnectionString="" hostingProviderForumLink="" controlPanelLink="https://portal.azure.com" webSystem="WebSites"><databases /></publishProfile><publishProfile profileName="golden-arches-prod-backend - Zip Deploy" publishMethod="ZipDeploy" publishUrl="golden-arches-prod-backend.scm.azurewebsites.net:443" userName="$golden-arches-prod-backend" userPWD="27y7NFFj9mHsNakb0Zz2YnggeFyaimr2rkq2dGmu5yX4riNdikwKgX9bivQt" destinationAppUrl="https://golden-arches-prod-backend.azurewebsites.net" SQLServerDBConnectionString="" mySQLDBConnectionString="" hostingProviderForumLink="" controlPanelLink="https://portal.azure.com" webSystem="WebSites"><databases /></publishProfile></publishData>
```

### 3. Azure Static Web Apps Secret

**AZURE_STATIC_WEB_APPS_API_TOKEN**
```
9cff09f9559a76d47aa381f2bd5f6a7351a382990fdd61391110930fee7fc15e06-8fdd163b-01cf-486a-b73b-cf386478ebcd01e041201f996d1e
```

## 🚀 Deployment URLs

After setting up the secrets, your application will be available at:

- **Backend API**: https://golden-arches-prod-backend.azurewebsites.net
- **Frontend**: https://green-glacier-01f996d1e.6.azurestaticapps.net
- **API Documentation**: https://golden-arches-prod-backend.azurewebsites.net/docs

## 🔄 Testing the CI/CD Pipeline

1. **Automatic Deployment**: Push any changes to the `main` branch
2. **Manual Deployment**: Go to Actions tab → "Deploy Backend to Azure App Service" → "Run workflow"

### Backend Deployment Triggers:
- Push to `main` branch with changes in `backend/` folder
- Manual workflow dispatch

### Frontend Deployment Triggers:
- Push to `main` branch (any changes)
- Automatic deployment via Static Web Apps

## 📊 Monitoring Deployments

### GitHub Actions
- Go to the **Actions** tab in your repository
- Monitor workflow runs and deployment status
- View logs for troubleshooting

### Azure Portal
- **App Service**: Monitor backend deployment and logs
- **Static Web Apps**: Monitor frontend deployment
- **Application Insights**: View application metrics and logs

## 🛠️ Local Development

### Backend
```bash
cd backend
source venv/bin/activate
export AZURE_MOCK_MODE="true"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Environment Variables

### Production Backend (Azure App Service)
These are automatically configured via the ARM template:
- `AZURE_STORAGE_CONNECTION_STRING`
- `AZURE_ML_WORKSPACE_NAME`
- `AZURE_ML_RESOURCE_GROUP`
- `AZURE_ML_SUBSCRIPTION_ID`
- `APPLICATIONINSIGHTS_CONNECTION_STRING`

### Production Frontend (Build-time)
Set in GitHub Actions workflow:
- `VITE_API_BASE_URL`: https://golden-arches-prod-backend.azurewebsites.net

## 🎯 Next Steps

1. **Set up the GitHub secrets** using the values above
2. **Push a change** to trigger the first deployment
3. **Monitor the deployment** in GitHub Actions
4. **Test the deployed application** using the URLs above
5. **Configure Azure ML workspace** for model training
6. **Set up monitoring and alerts** in Azure Portal

## 🆘 Troubleshooting

### Common Issues

**GitHub Actions failing:**
- Check that all secrets are correctly set
- Verify the secret values match exactly (no extra spaces)

**Backend not starting:**
- Check Azure App Service logs in Azure Portal
- Verify environment variables are set correctly

**Frontend build failing:**
- Check that `VITE_API_BASE_URL` is set in the workflow
- Verify Node.js version compatibility

### Getting Help

1. Check the deployment logs in GitHub Actions
2. Review Azure App Service logs in Azure Portal
3. Check the `DEPLOYMENT.md` file for detailed troubleshooting
4. Create an issue in the repository for support

---

**🎉 Once all secrets are configured, your Golden Arches Integrity application will be fully deployed and ready for production use!** 