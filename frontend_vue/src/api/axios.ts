// src/api/axios.ts
import axios from 'axios';

// Función para obtener el valor de una cookie por nombre
function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()!.split(';').shift() || null;
  return null;
}

const api = axios.create({
  baseURL: '', // <--- Cambiado: baseURL vacío para evitar doble /api/api
  timeout: 10000,
  withCredentials: true, // <--- Importante para enviar cookies de sesión
});

// Interceptor SOLO en la instancia api
api.interceptors.request.use(
  async (config) => {
    // Busca el token en localStorage (ajusta si lo guardas en otro lado)
    const user = localStorage.getItem('user');
    let token = null;
    if (user) {
      try {
        const userObj = JSON.parse(user);
        token = userObj.token || userObj.access || userObj.access_token;
      } catch (e) {}
    }
    if (token) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    // CSRF: solo para métodos que lo requieran
    const method = config.method ? config.method.toUpperCase() : '';
    if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
      let csrfToken = getCookie('csrftoken');
      if (!csrfToken) {
        // Haz un GET para obtener la cookie CSRF si no existe
        try {
          await api.get('/api/csrf/', { withCredentials: true });
        } catch (e) {}
        csrfToken = getCookie('csrftoken');
      }
      if (csrfToken) {
        config.headers = config.headers || {};
        config.headers['X-CSRFToken'] = csrfToken;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
