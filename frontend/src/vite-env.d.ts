/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_NAME: string
  readonly VITE_APP_VERSION: string
  readonly VITE_ENVIRONMENT: string
  readonly VITE_APPLICATIONINSIGHTS_CONNECTION_STRING: string
  readonly VITE_ENABLE_ANALYTICS: string
  readonly VITE_ENABLE_ERROR_REPORTING: string
  readonly VITE_DEBUG_MODE: string
  readonly VITE_MAX_FILE_SIZE: string
  readonly VITE_MAX_FILES_PER_BATCH: string
  readonly VITE_BRAND_PRIMARY_COLOR: string
  readonly VITE_BRAND_SECONDARY_COLOR: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
} 