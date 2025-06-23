<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Usuario</label>
          <input v-model="username" id="username" name="username" required />
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <div style="position:relative;display:flex;align-items:center;">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              id="password"
              name="password"
              required
              style="padding-right:2.5rem;width:100%;box-sizing:border-box;"
            />
            <img
              :src="showPassword ? openDoor : openClosed"
              :alt="showPassword ? 'Mostrar contraseña' : 'Ocultar contraseña'"
              @click="showPassword = !showPassword"
              style="position:absolute;right:0.7rem;top:48%;transform:translateY(-50%);width:22px;height:22px;cursor:pointer;user-select:none;background:#f3f4f6;border-radius:50%;pointer-events:auto;box-shadow:0 1px 2px rgba(0,0,0,0.04);"
            />
          </div>
        </div>
        <div v-if="error" class="form-error">{{ error }}</div>
        <button type="submit">Entrar</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import '../styles/AuthModal.css'
import openDoor from '../svg/open-door.svg?url'
import openClosed from '../svg/open-closed.svg?url'
const emit = defineEmits(['success', 'close'])
const username = ref('')
const password = ref('')
const error = ref('')
const showPassword = ref(false)

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

async function handleLogin() {
  error.value = ''
  // 1. Asegúrate de tener el CSRF token (haz un GET antes si es necesario)
  await fetch('/api/usuarios/login/', { method: 'GET', credentials: 'include' });
  const csrftoken = getCookie('csrftoken');
  try {
    const res = await fetch('/api/usuarios/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({ username: username.value.trim(), password: password.value }),
      credentials: 'include' // <--- Importante para que la cookie de sesión se guarde
    })
    // Debug: mostrar respuesta cruda en consola
    console.log('Status:', res.status)
    const text = await res.text()
    console.log('Raw response:', text)
    let data
    try {
      data = JSON.parse(text)
    } catch (e) {
      data = { non_field_errors: ['Respuesta no válida del servidor'] }
    }
    if (res.ok) {
      // Normalizar tipo_usuario a tipo (minúsculas y guion bajo)
      if (data.tipo_usuario) {
        data.tipo = (data.tipo_usuario + '').toLowerCase().replace(/\s+/g, '_')
      }
      localStorage.setItem('user', JSON.stringify(data))
      emit('success', data)
      emit('close')
    } else {
      error.value = data.non_field_errors?.[0] || data.username?.[0] || data.password?.[0] || 'Error de autenticación'
    }
  } catch (e) {
    error.value = 'Error de red'
  }
}
</script>
