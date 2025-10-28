/**
 * Environment Configuration
 * 
 * This file contains all environment-specific configuration.
 * In production, these should be set via environment variables.
 */

export const config = {
  // API Configuration
  api: {
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    timeout: 30000, // 30 seconds
  },

  // Application Configuration
  app: {
    name: 'RAG System',
    version: '1.0.0',
    environment: import.meta.env.MODE || 'development',
  },

  // Feature Flags
  features: {
    enableDebugMode: import.meta.env.DEV,
  },

  // Upload Configuration
  upload: {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedFileTypes: ['.txt', '.pdf'],
    allowedMimeTypes: ['text/plain', 'application/pdf'],
  },

  // Search Configuration
  search: {
    defaultTopK: 5,
    maxTopK: 20,
  },

  // Chat Configuration
  chat: {
    defaultTemperature: 0.7,
    defaultMaxTokens: 500,
    maxMessageLength: 4000,
  },
} as const;

export type Config = typeof config;
