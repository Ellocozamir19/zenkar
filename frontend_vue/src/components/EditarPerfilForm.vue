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
        <template v-if="peticionPendiente">
          <div class="peticion-pendiente-msg" style="margin:2rem 0;text-align:center;font-size:1.1rem;color:#b7791f;font-weight:600;">
            <span>
              Ya has solicitado editar tu
              <span v-if="peticionPendiente.datos_nuevos.username">nombre (<b>{{ peticionPendiente.datos_nuevos.username }}</b>)</span>
              <span v-if="peticionPendiente.datos_nuevos.username && peticionPendiente.datos_nuevos.email"> y </span>
              <span v-if="peticionPendiente.datos_nuevos.email">email (<b>{{ peticionPendiente.datos_nuevos.email }}</b>)</span>.
              <br>
              Estado: <b>{{ peticionPendiente.estado }}</b>. Espera la aprobación de un administrador.
            </span>
          </div>
        </template>
        <form v-else @submit.prevent="handleSubmit">
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
              Enviar
            </button>
          </div>
        </form>
        <div v-if="peticionEnviada" class="peticion-msg">
          <span>Tu petición de cambio de perfil fue enviada. Un administrador la aprobará o rechazará pronto.</span>
        </div>
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

const peticionEnviada = ref(false)
const peticionPendiente = ref<any>(null)

onMounted(async () => {
  form.value.username = props.user.username
  form.value.email = props.user.email
  // Consultar si hay petición pendiente
  try {
    const res = await api.get('/api/usuarios/mis_peticiones_cambio/')
    const pendientes = res.data.filter((p: any) => p.usuario === props.user.id && p.estado === 'pendiente')
    if (pendientes.length) peticionPendiente.value = pendientes[0]
  } catch {}
})

async function handleSubmit() {
  // Solo enviar campos que realmente cambiaron
  const datos_cambio: any = {}
  if (form.value.username !== props.user.username) datos_cambio.username = form.value.username
  if (form.value.email !== props.user.email) datos_cambio.email = form.value.email
  if (form.value.password) {
    datos_cambio.password = form.value.password
    datos_cambio.old_password = form.value.old_password
  }
  if (Object.keys(datos_cambio).length === 0) {
    alert('No realizaste ningún cambio en tu perfil.')
    return
  }
  try {
    await api.post('/api/usuarios/peticion_cambio/', {
      usuario: props.user.id,
      datos_nuevos: datos_cambio
    })
    peticionEnviada.value = true
    peticionPendiente.value = null
    setTimeout(() => {
      peticionEnviada.value = false
      emit('close')
    }, 1800)
    // Opcional: emitir evento para refrescar perfil
    // emit('success', { ...props.user, ...datos_cambio })
  } catch (e: any) {
    alert('Error enviando petición: ' + (e.response?.data?.detail || e.message))
  }
}
</script>

<style scoped src="../styles/EditarPerfilForm.css"></style>
