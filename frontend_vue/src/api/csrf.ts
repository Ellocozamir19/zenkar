// src/api/csrf.ts
import axios from 'axios';

export async function getCSRFToken() {
  // Django por defecto expone el token en esta ruta
  const response = await axios.get('/api/csrf/');
  return response.data.csrfToken || response.data.csrf_token || response.data.token || '';
}
