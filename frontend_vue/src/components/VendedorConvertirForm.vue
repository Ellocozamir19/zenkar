<template>
  <form class="vendedor-convertir-scroll" @submit.prevent="handleSubmit">
    <div class="vendedor-convertir-section-title">Datos Personales</div>
    <div class="vendedor-convertir-group">
      <label>Tipo de documento</label>
      <select v-model="form.tipo_documento" required>
        <option disabled value="">Seleccionar</option>
        <option value="CC">Cédula de ciudadanía</option>
        <option value="CE">Cédula de extranjería</option>
        <option value="NIT">NIT</option>
        <option value="TI">Tarjeta de identidad</option>
        <option value="PAS">Pasaporte</option>
      </select>
    </div>
    <div class="vendedor-convertir-group">
      <label>Número de documento</label>
      <input v-model="form.numero_documento" placeholder="Número de documento" required />
    </div>
    <div class="vendedor-convertir-row">
      <div class="vendedor-convertir-group">
        <label>Fecha de nacimiento</label>
        <input v-model="form.fecha_nacimiento" type="date" required />
      </div>
      <div class="vendedor-convertir-group">
        <label>Género</label>
        <select v-model="form.genero" required>
          <option disabled value="">Seleccionar</option>
          <option value="Masculino">Masculino</option>
          <option value="Femenino">Femenino</option>
          <option value="Otro">Otro</option>
          <option value="Prefiero no decir">Prefiero no decir</option>
        </select>
      </div>
    </div>
    <div class="vendedor-convertir-row">
      <div class="vendedor-convertir-group">
        <label>Celular</label>
        <input v-model="form.celular" placeholder="Celular" />
      </div>
      <div class="vendedor-convertir-group">
        <label>Teléfono fijo</label>
        <input v-model="form.telefono_fijo" placeholder="Teléfono fijo" />
      </div>
    </div>
    <div class="vendedor-convertir-group">
      <label>Dirección</label>
      <input v-model="form.direccion" placeholder="Dirección" />
    </div>
    <div class="vendedor-convertir-row">
      <div class="vendedor-convertir-group">
        <label>Ciudad</label>
        <input v-model="form.ciudad" placeholder="Ciudad" />
      </div>
      <div class="vendedor-convertir-group">
        <label>Departamento</label>
        <input v-model="form.departamento" placeholder="Departamento" />
      </div>
      <div class="vendedor-convertir-group">
        <label>País</label>
        <input v-model="form.pais" placeholder="País" />
      </div>
    </div>
    <div class="vendedor-convertir-section-title">Perfil Profesional</div>
    <div class="vendedor-convertir-group">
      <label>Tipo de persona</label>
      <select v-model="form.persona_natural">
        <option disabled value="">Seleccionar</option>
        <option value="natural">Persona natural</option>
        <option value="empresa">Empresa</option>
      </select>
    </div>
    <transition name="fade">
      <div v-if="form.persona_natural === 'empresa'" class="vendedor-convertir-group">
        <label>Nombre empresa</label>
        <input v-model="form.nombre_empresa" placeholder="Nombre empresa" required />
      </div>
    </transition>
    <transition name="fade">
      <div v-if="form.persona_natural" class="vendedor-convertir-row">
        <div class="vendedor-convertir-group">
          <label>Años de experiencia</label>
          <input v-model.number="form.anios_experiencia" type="number" min="0" placeholder="Años de experiencia" />
        </div>
        <div class="vendedor-convertir-group">
          <label>Tipo de vehículos</label>
          <input v-model="form.tipo_vehiculos" placeholder="Autos, motos, camiones..." />
        </div>
        <div class="vendedor-convertir-group">
          <label>Cantidad vehículos/mes</label>
          <input v-model.number="form.cantidad_vehiculos_mes" type="number" min="0" placeholder="Cantidad vehículos/mes" />
        </div>
      </div>
    </transition>
    <transition name="fade">
      <div v-if="form.persona_natural" class="vendedor-convertir-row">
        <div class="vendedor-convertir-group">
          <label>Licencia vendedor</label>
          <input v-model="form.licencia_vendedor" placeholder="Licencia vendedor" />
        </div>
        <div class="vendedor-convertir-group">
          <label>Asociación sector</label>
          <input v-model="form.asociacion_sector" placeholder="Asociación sector" />
        </div>
      </div>
    </transition>
    <div class="vendedor-convertir-section-title">Redes y Preferencias</div>
    <div class="vendedor-convertir-group">
      <label>¿Desea añadir redes de contacto?</label>
      <select v-model="form.mostrar_redes" style="margin-bottom:1.1rem;max-width:220px;">
        <option :value="false">No</option>
        <option :value="true">Sí</option>
      </select>
      <transition name="fade-slide">
        <div v-if="form.mostrar_redes === true || form.mostrar_redes === 'true'" class="vendedor-convertir-row" style="margin-top:0.7rem;">
          <div class="vendedor-convertir-group">
            <label>Facebook</label>
            <input v-model="form.facebook" placeholder="Facebook" />
          </div>
          <div class="vendedor-convertir-group">
            <label>Instagram</label>
            <input v-model="form.instagram" placeholder="Instagram" />
          </div>
          <div class="vendedor-convertir-group">
            <label>Página web</label>
            <input v-model="form.web" placeholder="Página web" />
          </div>
        </div>
      </transition>
    </div>
    <div class="vendedor-convertir-group" style="margin-bottom:0.5rem;">
      <label>¿Qué te gustaría mostrar en tu perfil público? <span style="font-weight:400; color:#888; font-size:0.97em;">(opcional)</span></label>
      <input v-model="form.descripcion_perfil" placeholder="Ej: Experiencia, servicios, mensaje de bienvenida..." />
    </div>
    <div class="vendedor-convertir-row">
      <div class="vendedor-convertir-group">
        <label>Recibir novedades</label>
        <select v-model="form.recibir_novedades">
          <option :value="true">Sí</option>
          <option :value="false">No</option>
        </select>
      </div>
      <div class="vendedor-convertir-group">
        <label>Mostrar contacto</label>
        <select v-model="form.mostrar_contacto">
          <option :value="true">Sí</option>
          <option :value="false">No</option>
        </select>
      </div>
    </div>
    <div class="vendedor-convertir-actions">
      <button type="button" @click="$emit('close')">Cancelar</button>
      <button type="submit">Guardar</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
const props = defineProps<{ userId: number }>()
const emit = defineEmits(['close', 'success'])
const form = ref<any>({ persona_natural: '', mostrar_redes: false })

watch(() => form.value.persona_natural, (val) => {
  if (val !== 'empresa') form.value.nombre_empresa = ''
})

function isValidDate(dateString: string) {
  const regex = /^\d{4}-\d{2}-\d{2}$/
  if (!regex.test(dateString)) return false
  const date = new Date(dateString)
  return !isNaN(date.getTime()) && dateString === date.toISOString().slice(0, 10)
}

async function handleSubmit() {
  try {
    if (!isValidDate(form.value.fecha_nacimiento)) {
      alert('Por favor ingresa una fecha de nacimiento válida (YYYY-MM-DD)')
      return
    }
    await axios.post(`/api/usuarios/${props.userId}/convertir_vendedor/`, form.value)
    emit('success')
    emit('close')
  } catch (e: any) {
    if (e.response && e.response.data) {
      alert('Error al guardar los datos de vendedor: ' + JSON.stringify(e.response.data, null, 2))
    } else {
      alert('Error al guardar los datos de vendedor')
    }
  }
}
</script>

<style scoped>
@import '../styles/VendedorConvertirForm.css';
</style>

<!-- Este archivo ha sido fusionado en VendedorForm.vue y ya no es necesario. Puedes eliminarlo de tu proyecto. -->
