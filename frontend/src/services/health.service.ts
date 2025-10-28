/**
 * Health Service
 * 
 * Service for checking system health and API status
 */

import { apiService } from './api.service';
import type { HealthResponse, APIStatusResponse, RAGHealthResponse } from '@/types';

class HealthService {
  /**
   * Check basic API health
   */
  async checkHealth(): Promise<HealthResponse> {
    return apiService.get<HealthResponse>('/health');
  }

  /**
   * Get detailed API status
   */
  async getAPIStatus(): Promise<APIStatusResponse> {
    return apiService.get<APIStatusResponse>('/api/v1/status');
  }

  /**
   * Check RAG system health
   */
  async checkRAGHealth(): Promise<RAGHealthResponse> {
    return apiService.get<RAGHealthResponse>('/api/v1/rag/health');
  }

  /**
   * Check if the API is reachable
   */
  async isAPIReachable(): Promise<boolean> {
    try {
      await this.checkHealth();
      return true;
    } catch (error) {
      return false;
    }
  }
}

export const healthService = new HealthService();
export default healthService;
