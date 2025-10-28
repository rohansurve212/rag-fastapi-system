/**
 * API Service Base
 * 
 * Configures axios instance with interceptors for:
 * - Request/response logging
 * - Error handling
 * - Authentication (future)
 */

import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import { config } from '@/config';
import type { ErrorResponse } from '@/types';

class APIService {
  private api: AxiosInstance;

  constructor() {
    // Create axios instance with base configuration
    this.api = axios.create({
      baseURL: config.api.baseUrl,
      timeout: config.api.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Setup interceptors
    this.setupInterceptors();
  }

  /**
   * Setup request and response interceptors
   */
  private setupInterceptors(): void {
    // Request interceptor
    this.api.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        // Log request in development
        if (import.meta.env.DEV) {
          console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, {
            params: config.params,
            data: config.data,
          });
        }

        // Add authentication token if available (future implementation)
        // const token = getAuthToken();
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`;
        // }

        return config;
      },
      (error: AxiosError) => {
        console.error('[API Request Error]', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response: AxiosResponse) => {
        // Log response in development
        if (import.meta.env.DEV) {
          console.log(`[API Response] ${response.config.method?.toUpperCase()} ${response.config.url}`, {
            status: response.status,
            data: response.data,
          });
        }

        return response;
      },
      (error: AxiosError<ErrorResponse>) => {
        // Handle different error types
        if (error.response) {
          // Server responded with error status
          const errorData = error.response.data;
          console.error('[API Error Response]', {
            status: error.response.status,
            error: errorData?.error || 'Unknown error',
            message: errorData?.message || error.message,
            detail: errorData?.detail,
          });
        } else if (error.request) {
          // Request made but no response received
          console.error('[API No Response]', error.message);
        } else {
          // Error in request setup
          console.error('[API Request Setup Error]', error.message);
        }

        return Promise.reject(error);
      }
    );
  }

  /**
   * Get the axios instance
   */
  public getInstance(): AxiosInstance {
    return this.api;
  }

  /**
   * GET request
   */
  public async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.api.get<T>(url, { params });
    return response.data;
  }

  /**
   * POST request
   */
  public async post<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.api.post<T>(url, data, config);
    return response.data;
  }

  /**
   * PUT request
   */
  public async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.api.put<T>(url, data);
    return response.data;
  }

  /**
   * DELETE request
   */
  public async delete<T>(url: string): Promise<T> {
    const response = await this.api.delete<T>(url);
    return response.data;
  }

  /**
   * PATCH request
   */
  public async patch<T>(url: string, data?: any): Promise<T> {
    const response = await this.api.patch<T>(url, data);
    return response.data;
  }
}

// Export singleton instance
export const apiService = new APIService();
export default apiService;
