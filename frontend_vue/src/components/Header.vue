<template>
  <header class="header">
    <div class="header-container">
      <!-- Logo y Saludo -->
      <div class="logo-greeting">
        <router-link to="/" class="logo" style="text-decoration:none; color:inherit;" @click="closeAdminPanels">
          zenkar
        </router-link>
        <p class="greeting" v-if="user">Hola, {{ user.username }}</p>
      </div>
      <!-- Navegación -->
      <div class="nav-container">
        <nav>
          <ul class="nav-links">
            <li>
              <router-link
                to="/"
                class="nav-link"
                :class="{'active': route.path === '/' && !showAdminPanel}"
                @click.native="closeAdminPanels"
              >
                Inicio
              </router-link>
            </li>
            <li>
              <router-link
                to="/"
                class="nav-link"
                :class="{'active': route.path === '/' && !showAdminPanel}"
                @click.native="closeAdminPanels"
              >
                Comparar
              </router-link>
            </li>
          </ul>
        </nav>
        <div v-if="isAuthenticated" class="user-area" @click.stop="toggleUserPanel">
          <button class="user-button">
            <div class="user-avatar">{{ userInitials }}</div>
            <span>{{ user.username }}</span>
            <svg class="chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </button>
          <!-- Panel de Usuario -->
          <div class="user-panel" :class="{ show: userPanelOpen }" ref="userPanel" @click.stop>
            <div class="user-panel-header">
              <div class="user-panel-name">{{ user.username }}</div>
              <div class="user-panel-email">{{ user.email }}</div>
              <div v-if="user.tipo_usuario" class="user-type-badge">
                <span class="user-type-icon">
                  <template v-if="user.tipo_usuario === 'admin_mayor'">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15 8.5 22 9.3 17 14.1 18.2 21 12 17.8 5.8 21 7 14.1 2 9.3 9 8.5 12 2"/></svg>
                  </template>
                  <template v-else-if="user.tipo_usuario === 'admin'">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                  </template>
                  <template v-else-if="user.tipo_usuario === 'vendedor'">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 3v4M8 3v4M2 11h20"/></svg>
                  </template>
                  <template v-else>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a8.38 8.38 0 0 1 13 0"/></svg>
                  </template>
                </span>
                <span class="user-type-text">{{ tipoUsuarioLabel }}</span>
              </div>
            </div>
            <div class="user-panel-section">
              <div class="section-title">Cuenta</div>
              <a href="#perfil" class="panel-link" @click.prevent="showEditarPerfil = true">
                <svg class="panel-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                Editar Perfil
              </a>
            </div>
            <div class="user-panel-section" v-if="isAdmin">
              <div class="section-title">Panel Admin</div>
              <a href="#admin" class="panel-link" @click.prevent="showAdminPanel = true">
                <svg class="panel-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v4a1 1 0 001 1h3m10-5v4a1 1 0 01-1 1h-3m-6 4v4a1 1 0 001 1h3m10-5v4a1 1 0 01-1 1h-3"></path>
                </svg>
                Tablas
              </a>
            </div>
            <div class="user-panel-section">
              <div class="section-title">Configuración</div>
              <a v-if="user && (user.tipo_usuario === undefined || user.tipo_usuario === 'usuario')" class="panel-link" @click.prevent="showVendedorForm = true">
                <svg class="panel-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
                Ser Vendedor
              </a>
              <a href="#configuracion" class="panel-link">
                <svg class="panel-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                Preferencias
              </a>
            </div>
            <a href="#logout" class="panel-link logout" @click.prevent="logout">
              <svg class="panel-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
              </svg>
              Cerrar Sesión
            </a>
          </div>
        </div>
        <div v-else class="auth-links">
          <a href="#" class="nav-link" @click.prevent="showLogin = true">Iniciar Sesión</a>
          <a href="#" class="nav-link" style="margin-left: 1rem;" @click.prevent="showRegister = true">Registrarse</a>
        </div>
      </div>
    </div>
  </header>
  <LoginForm v-if="showLogin" @close="showLogin = false" @success="onAuthSuccess" />
  <RegisterForm v-if="showRegister" @close="showRegister = false" @success="onAuthSuccess" />
  <AdminPanel v-if="showAdminPanel && user && user.tipo_usuario === 'admin'" @close="showAdminPanel = false" />
  <AdminMayorPanel v-if="showAdminPanel && user && user.tipo_usuario === 'admin_mayor'" @close="showAdminPanel = false" />
  <VendedorForm v-if="showVendedorForm && user && user.id" :user-id="user.id" @close="showVendedorForm = false" @success="onVendedorSuccess" />
  <EditarPerfilForm
    v-if="showEditarPerfil && user"
    @close="showEditarPerfil = false"
    :user="user"
    @success="onAuthSuccess"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'
import AdminMayorPanel from './AdminMayorPanel.vue'
import AdminPanel from './AdminPanel.vue'
import VendedorForm from './VendedorForm.vue'
import EditarPerfilForm from './EditarPerfilForm.vue'

// Define la interfaz para el usuario
interface Usuario {
  id: number
  username: string
  email: string
  tipo_usuario?: string
}

const user = ref<Usuario | null>(null)
const isAuthenticated = computed(() => !!user.value)
const isAdmin = computed(() => user.value && (user.value.tipo_usuario === 'admin_mayor' || user.value.tipo_usuario === 'admin'))
const userInitials = computed(() =>
  user.value && user.value.username
    ? user.value.username.slice(0, 2).toUpperCase()
    : ''
)

// Exponer variables para el template
const showLogin = ref(false)
const showRegister = ref(false)
const showAdminPanel = ref(false)
const showVendedorForm = ref(false)
const showEditarPerfil = ref(false)

function onAuthSuccess(data: Usuario) {
  user.value = data
  localStorage.setItem('user', JSON.stringify(data))
  showLogin.value = false
  showRegister.value = false
}

function logout() {
  user.value = null
  localStorage.removeItem('user')
  showLogin.value = false
  showRegister.value = false
}

const userPanelOpen = ref(false)
const userPanel = ref<HTMLElement | null>(null)

function toggleUserPanel() {
  userPanelOpen.value = !userPanelOpen.value
}

function handleClickOutside(event: MouseEvent) {
  if (userPanel.value && !userPanel.value.contains(event.target as Node)) {
    userPanelOpen.value = false
  }
}

onMounted(() => {
  // Cargar usuario desde localStorage si existe
  const stored = localStorage.getItem('user')
  if (stored) {
    const parsed = JSON.parse(stored)
    if (parsed && typeof parsed.id === 'number') {
      user.value = parsed
    }
  }
  document.addEventListener('click', handleClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const tipoUsuarioLabel = computed(() => {
  if (!user.value || !user.value.tipo_usuario) return ''
  switch (user.value.tipo_usuario) {
    case 'admin_mayor': return 'Admin Mayor'
    case 'admin': return 'Admin'
    case 'vendedor': return 'Vendedor'
    default: return 'Usuario'
  }
})

function closeAdminPanels() {
  showAdminPanel.value = false;
}

const route = useRoute()

onMounted(() => {
  updateBodyClass(route.path)
})

watch(() => route.path, (newPath) => {
  updateBodyClass(newPath)
})

function updateBodyClass(path: string) {
  document.body.classList.remove('admin-panel-active', 'admin-mayor-panel-active')
  if (path.startsWith('/admin-mayor')) {
    document.body.classList.add('admin-mayor-panel-active')
  } else if (path.startsWith('/admin')) {
    document.body.classList.add('admin-panel-active')
  }
}

function onVendedorSuccess() {
  if (user.value) {
    user.value.tipo_usuario = 'vendedor'
    localStorage.setItem('user', JSON.stringify(user.value))
    showVendedorForm.value = false
  }
}

const emit = defineEmits(['open-admin'])
</script>

<style scoped src="../styles/Header.css"></style>
