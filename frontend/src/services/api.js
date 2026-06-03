const defaultApiBaseUrl = 'http://localhost:8100';

export const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || defaultApiBaseUrl;

export async function fetchSystemInfo() {
  const response = await fetch(`${apiBaseUrl}/api/v1/system/info`);
  if (!response.ok) {
    throw new Error('Failed to fetch system info');
  }
  return response.json();
}
