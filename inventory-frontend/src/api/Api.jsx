const BASE_URL = 'http://localhost:8000';

// ── Token helpers ─────────────────────────────────────────────
export function getToken() {
  return localStorage.getItem('access_token');
}

export function saveToken(token) {
  localStorage.setItem('access_token', token);
}

export function clearToken() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('token_type');
}

export function getUserFromToken() {
  const token = getToken();
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return { username: payload.sub, role: payload.role };
  } catch {
    return null;
  }
}

export function isLoggedIn() {
  return !!getToken();
}

// ── Auth headers ──────────────────────────────────────────────
function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getToken()}`
  };
}

function formHeaders() {
  return {
    'Content-Type': 'application/x-www-form-urlencoded'
  };
}

// ── Auth ──────────────────────────────────────────────────────
export async function loginUser(username, password) {
  const body = new URLSearchParams();
  body.append('username', username);
  body.append('password', password);

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: formHeaders(),
    body: body.toString()
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Login failed');
  return data; // { access_token, token_type }
}

export async function registerUser(username, email, password, role) {
  const res = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email: email || null, password, role })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Registration failed');
  return data;
}

// ── Items ─────────────────────────────────────────────────────
export async function fetchItems() {
  const res = await fetch(`${BASE_URL}/items/`, { headers: authHeaders() });
  if (res.status === 401) throw new Error('UNAUTHORIZED');
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to fetch items');
  return data.data || [];
}

export async function createItem(payload) {
  const res = await fetch(`${BASE_URL}/item/create`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to create item');
  return data;
}

export async function updateItem(id, payload) {
  const res = await fetch(`${BASE_URL}/item/${id}`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to update item');
  return data;
}

export async function deleteItem(id) {
  const res = await fetch(`${BASE_URL}/item/${id}`, {
    method: 'DELETE',
    headers: authHeaders()
  });
  if (res.status === 204) return;
  if (res.status === 403) throw new Error('Only admins can delete items');
  const data = await res.json().catch(() => ({}));
  throw new Error(data.detail || 'Failed to delete item');
}

// ── Suppliers ─────────────────────────────────────────────────
export async function fetchSuppliers() {
  const res = await fetch(`${BASE_URL}/suppliers/`, { headers: authHeaders() });
  if (res.status === 401) throw new Error('UNAUTHORIZED');
  if (res.status === 404) return [];
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to fetch suppliers');
  return data.data || [];
}

export async function createSupplier(payload) {
  const res = await fetch(`${BASE_URL}/supplier/create`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to create supplier');
  return data;
}

export async function updateSupplier(id, payload) {
  const res = await fetch(`${BASE_URL}/supplier/${id}`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to update supplier');
  return data;
}

export async function deleteSupplier(id) {
  const res = await fetch(`${BASE_URL}/supplier/${id}`, {
    method: 'DELETE',
    headers: authHeaders()
  });
  if (res.status === 204) return;
  const data = await res.json().catch(() => ({}));
  throw new Error(data.detail || 'Failed to delete supplier');
}

// ── Inwards ───────────────────────────────────────────────────
export async function fetchInwards() {
  const res = await fetch(`${BASE_URL}/inwards/`, { headers: authHeaders() });
  if (res.status === 401) throw new Error('UNAUTHORIZED');
  if (res.status === 404) return [];
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to fetch inwards');
  return data.data || [];
}

export async function createInward(payload) {
  const res = await fetch(`${BASE_URL}/inward/create`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to create inward');
  return data;
}

export async function updateInward(id, payload) {
  const res = await fetch(`${BASE_URL}/inward/${id}`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to update inward');
  return data;
}

export async function deleteInward(id) {
  const res = await fetch(`${BASE_URL}/inward/${id}`, {
    method: 'DELETE',
    headers: authHeaders()
  });
  if (res.status === 204) return;
  const text = await res.text();
  if (text.includes('outward barcode')) {
    throw new Error('Cannot delete — an outward barcode exists for this entry');
  }
  throw new Error('Failed to delete inward');
}