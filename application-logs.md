# Golden Arches Backend Application Logs

## Log Download Status
- Downloaded logs from Azure App Service: `golden-arches-prod-backend`
- Timestamp: June 2, 2025, 01:33 UTC
- Log files extracted from: `current-logs.zip`

## Available Log Files
```
LogFiles/2025_06_02_lw0sdlwk0004EJ_docker.log  (Docker container logs - Permission denied)
LogFiles/kudu/trace/*.xml                      (Kudu trace files)
LogFiles/kudu/trace/*.txt                      (Kudu trace text files)
LogFiles/webssh/.log                           (WebSSH logs - empty)
LogFiles/__lastCheckTime.txt                   (Last check timestamp)
```

## Issue
The main Docker container log file (`2025_06_02_lw0sdlwk0004EJ_docker.log`) cannot be read due to permission restrictions.

## Current Status
- App Service: Running
- Container Image: `goldenarchesprodacr.azurecr.io/golden-arches-backend:manual-deploy`
- Authentication: ✅ Managed Identity configured with AcrPull role
- Environment Variables: ✅ Azure settings configured
- Health Check Response: ❌ 503 Application Error

## Kudu Trace Activity
Recent trace files show:
- Multiple startup/shutdown cycles
- GET requests to `/dump` and `/logstream` endpoints
- Timestamps indicating container restart attempts

## Next Steps Needed
To diagnose the container startup issue, we need access to the Docker container logs which contain the actual application startup output and any error messages from the FastAPI application.

**Recommendation**: Use Azure Portal to access the log stream directly, or use alternative methods to view the container logs that bypass the permission restrictions. 