import { createPinia } from 'pinia';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './styles/VendedorForm.css';
import { useLoaderStore } from './store/loader';

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount('#app');

// Opcional: Exponer el loaderStore globalmente para pruebas manuales en consola
if (import.meta.env.DEV) {
  window.loaderStore = useLoaderStore();
}
