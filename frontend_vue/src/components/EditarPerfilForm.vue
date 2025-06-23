<template>
  <div class="modal-overlay">
    <div class="modal-container">
      <!-- Close Button -->
      <button class="close-btn" type="button" @click="$emit('close')">
        <span class="icon-close"></span>
      </button>
      <!-- Header -->
      <div class="modal-header">
        <h2 class="modal-title">Editar Perfil</h2>
      </div>
      <!-- Body -->
      <div class="modal-body">
        <form @submit.prevent="handleSubmit">
          <!-- Título sección datos -->
          <div class="data-section-title">Editar Datos</div>
          <!-- Username -->
          <div class="form-group">
            <label class="form-label" for="username">Usuario</label>
            <input 
              type="text" 
              id="username" 
              class="form-input" 
              placeholder="Nombre de usuario"
              v-model="form.username"
              required
            >
          </div>
          <!-- Email -->
          <div class="form-group">
            <label class="form-label" for="email">Email</label>
            <input 
              type="email" 
              id="email" 
              class="form-input" 
              placeholder="correo@ejemplo.com"
              v-model="form.email"
              required
            >
          </div>
          <!-- Título sección contraseña -->
          <div class="password-section-title">Editar Contraseña</div>
          <!-- Old Password -->
          <div class="form-group">
            <label class="form-label" for="old_password">Contraseña actual</label>
            <div class="input-icon-wrapper">
              <input 
                :type="showOldPassword ? 'text' : 'password'" 
                id="old_password" 
                class="form-input" 
                placeholder="Ingresa tu contraseña actual para cambiar la nueva"
                v-model="form.old_password"
              >
              <img
                :src="showOldPassword ? openDoor : openClosed"
                :alt="showOldPassword ? 'Mostrar contraseña' : 'Ocultar contraseña'"
                @click="showOldPassword = !showOldPassword"
                class="password-toggle-icon"
              />
            </div>
          </div>
          <!-- New Password -->
          <div class="form-group">
            <label class="form-label" for="password">Nueva contraseña</label>
            <div class="input-icon-wrapper">
              <input 
                :type="showNewPassword ? 'text' : 'password'" 
                id="password" 
                class="form-input" 
                placeholder="Nueva contraseña (opcional)"
                v-model="form.password"
              >
              <img
                :src="showNewPassword ? openDoor : openClosed"
                :alt="showNewPassword ? 'Mostrar contraseña' : 'Ocultar contraseña'"
                @click="showNewPassword = !showNewPassword"
                class="password-toggle-icon"
              />
            </div>
            <p class="password-note">Dejar vacío para mantener la actual</p>
          </div>
          <!-- Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="$emit('close')">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api/axios'
import openDoor from '../svg/open-door.svg?url'
import openClosed from '../svg/open-closed.svg?url'

const props = defineProps<{ user: { id: number, username: string, email: string } }>()
const emit = defineEmits(['close', 'success'])

const form = ref({
  username: '',
  email: '',
  password: '',
  old_password: ''
})

const showOldPassword = ref(false)
const showNewPassword = ref(false)

onMounted(() => {
  form.value.username = props.user.username
  form.value.email = props.user.email
})

async function handleSubmit() {
  try {
    const payload: any = {
      username: form.value.username,
      email: form.value.email
    }
    if (form.value.password) {
      payload.password = form.value.password
      payload.old_password = form.value.old_password
    }
    await api.put(`/api/usuarios/${props.user.id}/editar/`, payload)
    emit('success', { ...props.user, ...payload })
    emit('close')
  } catch (e: any) {
    alert('Error actualizando perfil: ' + (e.response?.data?.detail || e.message))
  }
}
</script>

<style scoped src="../styles/EditarPerfilForm.css"></style>
