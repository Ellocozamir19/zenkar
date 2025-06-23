// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth'

const routes = [
  {
    path: '/',
    name: 'Comparador',
    component: () => import('../views/Comparador.vue')
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: () => import('../views/AdminPanel.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'admin_mayor'] }
  },
  {
    path: '/admin-mayor',
    name: 'AdminMayorPanel',
    component: () => import('../views/AdminMayorPanel.vue'),
    meta: { requiresAuth: true, roles: ['admin_mayor'] }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginForm.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterForm.vue')
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  auth.loadUser()
  if (to.meta.requiresAuth) {
    if (!auth.user) {
      return next('/login')
    }
    // Leer tipo desde localStorage y objeto user, y normalizar
    let tipo = auth.user.tipo || auth.user.tipo_usuario
    if (!tipo) {
      try {
        const u = JSON.parse(localStorage.getItem('user') || '{}')
        tipo = u.tipo || u.tipo_usuario
      } catch {}
    }
    tipo = (tipo || '').toLowerCase().replace(/\s+/g, '_')
    // Si la ruta tiene roles permitidos
    if (to.meta.roles && Array.isArray(to.meta.roles)) {
      // Si eres admin_mayor y navegas a /admin, redirige a /admin-mayor
      if (to.path === '/admin' && tipo === 'admin_mayor') {
        return next('/admin-mayor')
      }
      if (!to.meta.roles.includes(tipo)) {
        // Redirigir al panel correcto
        if (tipo === 'admin_mayor') return next('/admin-mayor')
        if (tipo === 'admin') return next('/admin')
        return next('/')
      }
    }
  }
  next()
})

export default router;
