/**
 * Utility Functions
 * 
 * Common utility functions used throughout the application
 */

import { type ClassValue, clsx } from 'clsx';
import { format, formatDistanceToNow, parseISO } from 'date-fns';

/**
 * Merge class names conditionally
 */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

/**
 * Format file size in human-readable format
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Format date string
 */
export function formatDate(dateString: string, formatString: string = 'PPP'): string {
  try {
    const date = parseISO(dateString);
    return format(date, formatString);
  } catch (error) {
    return dateString;
  }
}

/**
 * Format date as relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(dateString: string): string {
  try {
    const date = parseISO(dateString);
    return formatDistanceToNow(date, { addSuffix: true });
  } catch (error) {
    return dateString;
  }
}

/**
 * Truncate text to specified length
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

/**
 * Get file extension from filename
 */
export function getFileExtension(filename: string): string {
  return '.' + filename.split('.').pop()?.toLowerCase() || '';
}

/**
 * Get file type icon name based on extension
 */
export function getFileTypeIcon(filename: string): string {
  const extension = getFileExtension(filename);
  
  switch (extension) {
    case '.pdf':
      return 'FileText';
    case '.txt':
      return 'FileText';
    case '.doc':
    case '.docx':
      return 'FileText';
    default:
      return 'File';
  }
}

/**
 * Highlight search query in text
 */
export function highlightText(text: string, query: string): string {
  if (!query) return text;
  
  const regex = new RegExp(`(${query})`, 'gi');
  return text.replace(regex, '<mark class="bg-yellow-200">$1</mark>');
}

/**
 * Debounce function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null;
      func(...args);
    };

    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  };
}

/**
 * Copy text to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
}

/**
 * Download text as file
 */
export function downloadTextFile(content: string, filename: string): void {
  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Parse error message from API error
 */
export function parseErrorMessage(error: any): string {
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (error.message) {
    return error.message;
  }
  return 'An unexpected error occurred';
}

/**
 * Generate a random ID
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2, 15);
}

/**
 * Sleep for specified milliseconds
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Check if string is valid JSON
 */
export function isValidJSON(str: string): boolean {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Format number with thousand separators
 */
export function formatNumber(num: number): string {
  return num.toLocaleString();
}

/**
 * Calculate percentage
 */
export function calculatePercentage(value: number, total: number): number {
  if (total === 0) return 0;
  return Math.round((value / total) * 100);
}
