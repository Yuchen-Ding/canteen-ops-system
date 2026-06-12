const defaultApiBaseUrl = 'http://localhost:8100';

export const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || defaultApiBaseUrl;

async function request(path, options = {}) {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new Error(detail?.detail || `Request failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchSystemInfo() {
  return request('/api/v1/system/info');
}

export async function fetchRecords(endpoint, { keyword = '', status = '', page = 1, pageSize = 20, ...filters } = {}) {
  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
  });
  if (keyword) {
    params.set('keyword', keyword);
  }
  if (status) {
    params.set('status', status);
  }
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) {
      params.set(key, String(value));
    }
  });
  return request(`${endpoint}?${params.toString()}`);
}

export async function fetchRecordDetail(endpoint, id) {
  return request(`${endpoint}/${id}`);
}

export async function fetchReport(endpoint, params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) {
      searchParams.set(key, String(value));
    }
  });
  const query = searchParams.toString();
  return request(`${endpoint}${query ? `?${query}` : ''}`);
}

export async function getCanteenMonitoringOverview() {
  return request('/api/v1/monitoring/canteen-overview');
}

export async function getYearlyReport(year) {
  return fetchReport('/api/v1/reports/yearly', { year });
}

export async function getLatestAiSession() {
  return request('/api/v1/ai/sessions/latest');
}

export async function sendAiChatMessage(sessionId, message) {
  return request('/api/v1/ai/chat', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId, message }),
  });
}

export async function createRecord(endpoint, payload) {
  return request(endpoint, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateRecord(endpoint, id, payload) {
  return request(`${endpoint}/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export async function updateRecordStatus(endpoint, id, status) {
  return request(`${endpoint}/${id}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
}
