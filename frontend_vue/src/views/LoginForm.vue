<template>
  <LoginForm @success="handleLogin" :error="error" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import LoginForm from '../components/LoginForm.vue'

const router = useRouter()
const auth = useAuthStore()
const error = ref('')

const handleLogin = async (data: any) => {
  // data puede ser el usuario completo o un objeto con user
  let user = data.user || data
  // Normalizar tipo_usuario
  if (user.tipo_usuario) {
    user.tipo = (user.tipo_usuario + '').toLowerCase().replace(/\s+/g, '_')
  } else if (user.tipo) {
    user.tipo = (user.tipo + '').toLowerCase().replace(/\s+/g, '_')
  }
  auth.setUser(user)
  // Redirección automática según tipo de usuario
  if (user.tipo === 'admin_mayor') {
    router.push('/admin-mayor')
  } else if (user.tipo === 'admin') {
    router.push('/admin')
  } else {
    router.push('/')
  }
}
</script>
