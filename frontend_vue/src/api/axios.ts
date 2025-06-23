// src/api/axios.ts
import axios from 'axios';

// Interceptor para añadir el token de autenticación a cada request
axios.interceptors.request.use(
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
      let csrfToken = localStorage.getItem('csrftoken');
      if (!csrfToken) {
        try {
          const resp = await axios.get('/api/usuarios/csrf/');
          csrfToken = resp.data.csrfToken;
          if (csrfToken) localStorage.setItem('csrftoken', csrfToken);
        } catch (e) {}
      }
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

const api = axios.create({
  baseURL: '', // <--- Cambiado: baseURL vacío para evitar doble /api/api
  timeout: 10000,
  withCredentials: true, // <--- Importante para enviar cookies de sesión
});

export default api;
