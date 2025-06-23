import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Cambiado a 127.0.0.1 para evitar problemas de localhost/::1
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
