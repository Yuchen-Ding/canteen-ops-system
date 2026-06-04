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

export async function fetchRecords(endpoint, { keyword = '', status = '', page = 1, pageSize = 20 } = {}) {
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
  return request(`${endpoint}?${params.toString()}`);
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
