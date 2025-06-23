<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal" :class="{ 'vendedor-modal': tipoUsuario === 'vendedor' }">
      <h2>Registrarse</h2>
      <form @submit.prevent="handleRegister" :class="['register-form-flex', tipoUsuario === 'vendedor' ? 'vendedor' : '']">
        <div class="register-main-form">
          <div class="form-group">
            <label for="username">Usuario</label>
            <input v-model="username" id="username" required />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input v-model="email" id="email" type="email" required />
          </div>
          <div class="form-group">
            <label for="password">Contraseña</label>
            <div style="position:relative;display:flex;align-items:center;">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                id="password"
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
          <div class="form-group">
            <label for="tipo_usuario">Tipo de cuenta</label>
            <select v-model="tipoUsuario" id="tipo_usuario" required>
              <option value="usuario">Usuario</option>
              <option value="vendedor">Vendedor</option>
            </select>
          </div>
          <div v-if="error" class="form-error">{{ error }}</div>
          <button type="submit">Registrarse</button>
          <div class="preferencias-legal-box">
            <div class="form-section-title preferencias-title">Preferencias y Legal</div>
            <div class="preferencias-checkboxes">
              <label class="checkbox-label">
                <input type="checkbox" v-model="recibirNovedades" id="recibir_novedades" />
                ¿Desea recibir novedades?
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="mostrarContacto" id="mostrar_contacto" />
                ¿Mostrar datos de contacto?
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="aceptaPolitica" id="acepta_politica" required />
                <span>Acepto política de privacidad*</span>
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="aceptaTerminos" id="acepta_terminos" required />
                <span>Acepto términos y condiciones*</span>
              </label>
            </div>
          </div>
        </div>
        <div v-if="tipoUsuario === 'vendedor'" class="vendedor-extra-form">
          <div class="form-section-title">Datos Personales</div>
          <div class="form-row">
            <div class="form-group">
              <label for="tipo_documento">Tipo de documento*</label>
              <select v-model="tipoDocumento" id="tipo_documento" required>
                <option v-for="tipo in tiposDocumento" :key="tipo.value" :value="tipo.value">
                  {{ tipo.label }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="numero_documento">Número de documento*</label>
              <input v-model="numeroDocumento" id="numero_documento" required />
            </div>
          </div>
          <div class="form-row" v-if="personaNatural === 'empresa'">
            <div class="form-group">
              <label for="nombre_empresa">Nombre de la empresa*</label>
              <input v-model="nombreEmpresa" id="nombre_empresa" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="fecha_nacimiento">Fecha de nacimiento</label>
              <input v-model="fechaNacimiento" id="fecha_nacimiento" type="date" />
            </div>
            <div class="form-group">
              <label for="genero">Género</label>
              <input v-model="genero" id="genero" />
            </div>
          </div>
          <div class="form-section-title">Contacto</div>
          <div class="form-row">
            <div class="form-group">
              <label for="celular">Celular*</label>
              <input v-model="celular" id="celular" required />
            </div>
            <div class="form-group">
              <label for="telefono_fijo">Teléfono fijo</label>
              <input v-model="telefonoFijo" id="telefono_fijo" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="direccion">Dirección</label>
              <input v-model="direccion" id="direccion" />
            </div>
            <div class="form-group">
              <label for="ciudad">Ciudad*</label>
              <input v-model="ciudad" id="ciudad" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="departamento">Departamento*</label>
              <input v-model="departamento" id="departamento" required />
            </div>
            <div class="form-group">
              <label for="pais">País*</label>
              <input v-model="pais" id="pais" required />
            </div>
          </div>
          <div class="form-section-title">Perfil Profesional</div>
          <div class="form-row">
            <div class="form-group" style="position:relative;">
              <label for="persona_natural" style="display:flex;align-items:center;gap:0.4rem;">
                Tipo de persona*
                <img
                  src="/src/svg/duda.svg"
                  alt="Ayuda tipo de persona"
                  class="duda-icon"
                  tabindex="0"
                  @mouseover="showTooltip($event, 'Selecciona si eres una persona natural o una empresa. Esto determinará los campos a completar.')"
                  @mouseleave="hideTooltip"
                  @focus="showTooltip($event, 'Selecciona si eres una persona natural o una empresa. Esto determinará los campos a completar.')"
                  @blur="hideTooltip"
                />
              </label>
              <select v-model="personaNatural" id="persona_natural" required>
                <option value="">Selecciona tipo de persona</option>
                <option value="natural">Persona natural</option>
                <option value="empresa">Empresa</option>
              </select>
            </div>
            <div v-if="personaNatural" class="form-group" style="position:relative;">
              <label for="anios_experiencia" style="display:flex;align-items:center;gap:0.4rem;">
                Años de experiencia
                <img
                  src="/src/svg/duda.svg"
                  alt="Ayuda años de experiencia"
                  class="duda-icon"
                  tabindex="0"
                  @mouseover="showTooltip($event, 'Indica cuántos años llevas trabajando en el sector automotriz. Escribe ninguno si no tienes experiencia.')"
                  @mouseleave="hideTooltip"
                  @focus="showTooltip($event, 'Indica cuántos años llevas trabajando en el sector automotriz. Escribe ninguno si no tienes experiencia.')"
                  @blur="hideTooltip"
                />
              </label>
              <input v-model="aniosExperiencia" id="anios_experiencia" placeholder="Ej: 5, ninguno" />
            </div>
          </div>
          <transition name="fade-slide">
            <div v-if="personaNatural === 'natural'">
              <div class="form-group" style="position:relative;">
                <label for="experiencia_ventas" style="display:flex;align-items:center;gap:0.4rem;">
                  ¿Tiene experiencia en ventas?
                  <img
                    src="/src/svg/duda.svg"
                    alt="Ayuda experiencia ventas"
                    class="duda-icon"
                    tabindex="0"
                    @mouseover="showTooltip($event, 'Indique si ha trabajado previamente en ventas de vehículos.')"
                    @mouseleave="hideTooltip"
                    @focus="showTooltip($event, 'Indique si ha trabajado previamente en ventas de vehículos.')"
                    @blur="hideTooltip"
                  />
                </label>
                <select v-model="experienciaVentas" id="experiencia_ventas" required>
                  <option value="">Seleccione</option>
                  <option value="si">Sí</option>
                  <option value="no">No</option>
                </select>
              </div>
              <div class="form-group" style="position:relative;">
                <label for="tipo_vehiculos" style="display:flex;align-items:center;gap:0.4rem;">
                  ¿Qué tipos de vehículos está interesado en vender?
                  <img
                    src="/src/svg/duda.svg"
                    alt="Ayuda tipo de vehículos"
                    class="duda-icon"
                    tabindex="0"
                    @mouseover="showTooltip($event, 'Ejemplo: autos, motos, camiones, etc.')"
                    @mouseleave="hideTooltip"
                    @focus="showTooltip($event, 'Ejemplo: autos, motos, camiones, etc.')"
                    @blur="hideTooltip"
                  />
                </label>
                <input v-model="tipoVehiculos" id="tipo_vehiculos" placeholder="Ej: autos, motos, camiones" />
              </div>
              <div class="form-group" style="position:relative;">
                <label for="cantidad_vehiculos_mes" style="display:flex;align-items:center;gap:0.4rem;">
                  ¿Cuántos vehículos espera vender al mes?
                  <img
                    src="/src/svg/duda.svg"
                    alt="Ayuda cantidad vehículos"
                    class="duda-icon"
                    tabindex="0"
                    @mouseover="showTooltip($event, 'Indique un número estimado o 0 si no sabe.')"
                    @mouseleave="hideTooltip"
                    @focus="showTooltip($event, 'Indique un número estimado o 0 si no sabe.')"
                    @blur="hideTooltip"
                  />
                </label>
                <input v-model="cantidadVehiculosMes" id="cantidad_vehiculos_mes" type="number" min="0" />
              </div>
            </div>
            <div v-else-if="personaNatural === 'empresa'">
              <div class="form-row">
                <div class="form-group" style="position:relative;">
                  <label for="licencia_vendedor" style="display:flex;align-items:center;gap:0.4rem;">
                    ¿Licencia de vendedor?
                    <img
                      src="/src/svg/duda.svg"
                      alt="Ayuda licencia vendedor"
                      class="duda-icon"
                      tabindex="0"
                      @mouseover="showTooltip($event, 'Si cuentas con una licencia o registro especial para vender vehículos, indícalo aquí.')"
                      @mouseleave="hideTooltip"
                      @focus="showTooltip($event, 'Si cuentas con una licencia o registro especial para vender vehículos, indícalo aquí.')"
                      @blur="hideTooltip"
                    />
                  </label>
                  <input v-model="licenciaVendedor" id="licencia_vendedor" />
                </div>
                <div class="form-group" style="position:relative;">
                  <label for="asociacion_sector" style="display:flex;align-items:center;gap:0.4rem;">
                    Asociación del sector
                    <img
                      src="/src/svg/duda.svg"
                      alt="Ayuda asociación sector"
                      class="duda-icon"
                      tabindex="0"
                      @mouseover="showTooltip($event, 'Si perteneces a alguna asociación o gremio del sector automotriz, escríbelo aquí.')"
                      @mouseleave="hideTooltip"
                      @focus="showTooltip($event, 'Si perteneces a alguna asociación o gremio del sector automotriz, escríbelo aquí.')"
                      @blur="hideTooltip"
                    />
                  </label>
                  <input v-model="asociacionSector" id="asociacion_sector" />
                </div>
              </div>
              <div class="form-row">
                <div class="form-group" style="position:relative;">
                  <label for="tipo_vehiculos" style="display:flex;align-items:center;gap:0.4rem;">
                    Tipo de vehículos
                    <img
                      src="/src/svg/duda.svg"
                      alt="Ayuda tipo de vehículos"
                      class="duda-icon"
                      tabindex="0"
                      @mouseover="showTooltip($event, 'Especifica el tipo de vehículos que comercializas (ej: autos, motos, camiones).')"
                      @mouseleave="hideTooltip"
                      @focus="showTooltip($event, 'Especifica el tipo de vehículos que comercializas (ej: autos, motos, camiones).')"
                      @blur="hideTooltip"
                    />
                  </label>
                  <input v-model="tipoVehiculos" id="tipo_vehiculos" />
                </div>
                <div class="form-group" style="position:relative;">
                  <label for="cantidad_vehiculos_mes" style="display:flex;align-items:center;gap:0.4rem;">
                    Cantidad vehículos/mes
                    <img
                      src="/src/svg/duda.svg"
                      alt="Ayuda cantidad vehículos"
                      class="duda-icon"
                      tabindex="0"
                      @mouseover="showTooltip($event, '¿Cuántos vehículos vendes o gestionas en promedio cada mes?')"
                      @mouseleave="hideTooltip"
                      @focus="showTooltip($event, '¿Cuántos vehículos vendes o gestionas en promedio cada mes?')"
                      @blur="hideTooltip"
                    />
                  </label>
                  <input v-model="cantidadVehiculosMes" id="cantidad_vehiculos_mes" type="number" min="0" />
                </div>
              </div>
            </div>
          </transition>
          <div class="form-section-title" style="display:flex;align-items:center;gap:0.4rem;position:relative;">
            Presencia Online (opcional)
            <img
              src="/src/svg/duda.svg"
              alt="Ayuda presencia online"
              class="duda-icon"
              tabindex="0"
              @mouseover="showTooltip($event, 'Si deseas, puedes agregar tus redes sociales o página web para que los usuarios puedan conocerte mejor.')"
              @mouseleave="hideTooltip"
              @focus="showTooltip($event, 'Si deseas, puedes agregar tus redes sociales o página web para que los usuarios puedan conocerte mejor.')"
              @blur="hideTooltip"
            />
          </div>
          <div class="form-group" style="flex-direction: row; align-items: center; gap: 0.5rem;">
            <input type="checkbox" v-model="mostrarRedes" id="mostrar_redes" style="width:auto;" />
            <label for="mostrar_redes" style="margin-bottom:0;">¿Desea poner redes?</label>
          </div>
          <transition name="fade-slide">
            <div v-if="mostrarRedes">
              <div class="form-row">
                <div class="form-group">
                  <label for="facebook">Facebook</label>
                  <input v-model="facebook" id="facebook" />
                </div>
                <div class="form-group">
                  <label for="instagram">Instagram</label>
                  <input v-model="instagram" id="instagram" />
                </div>
                <div class="form-group">
                  <label for="web">Página web</label>
                  <input v-model="web" id="web" />
                </div>
              </div>
            </div>
          </transition>
        </div>
        <div v-if="tooltipPos.visible" :style="{position:'fixed',left:tooltipPos.x+'px',top:tooltipPos.y+'px'}" class="tooltip-ayuda">
          {{ tooltipPos.text }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import '../styles/AuthModal.css'
import '../styles/VendedorForm.css'
import openDoor from '../svg/open-door.svg'
import openClosed from '../svg/open-closed.svg'
const emit = defineEmits(['success', 'close'])
const username = ref('')
const email = ref('')
const password = ref('')
const tipoUsuario = ref('usuario')
const error = ref('')
const showPassword = ref(false)
const tipoDocumento = ref('CC') // Por defecto 'Cédula de ciudadanía'
const tiposDocumento = [
  { value: 'CC', label: 'Cédula de ciudadanía' },
  { value: 'CE', label: 'Cédula de extranjería' },
  { value: 'NIT', label: 'NIT' },
  { value: 'TI', label: 'Tarjeta de identidad' },
  { value: 'PAS', label: 'Pasaporte' }
]
const numeroDocumento = ref('')
const fechaNacimiento = ref('')
const genero = ref('')
const celular = ref('')
const telefonoFijo = ref('')
const direccion = ref('')
const ciudad = ref('')
const departamento = ref('')
const pais = ref('')
const personaNatural = ref('')
const aniosExperiencia = ref('')
const tipoVehiculos = ref('')
const cantidadVehiculosMes = ref('')
const licenciaVendedor = ref('')
const asociacionSector = ref('')
const mostrarRedes = ref(false)
const facebook = ref('')
const instagram = ref('')
const web = ref('')
const recibirNovedades = ref(false)
const mostrarContacto = ref(true)
const aceptaPolitica = ref(false)
const aceptaTerminos = ref(false)
const showTipoPersonaHelp = ref(false)
const showAniosExpHelp = ref(false)
const showTipoVehiculosHelp = ref(false)
const showCantidadVehiculosHelp = ref(false)
const showLicenciaVendedorHelp = ref(false)
const showAsociacionSectorHelp = ref(false)
const showPresenciaOnlineHelp = ref(false)
const experienciaVentas = ref('')
const nombreEmpresa = ref('')

// Tooltip helpers
const tooltipPos = ref({ x: 0, y: 0, visible: false, text: '' })
let tooltipTimeout: any = null
function showTooltip(event: MouseEvent | FocusEvent, text: string) {
  if (tooltipTimeout) clearTimeout(tooltipTimeout)
  const icon = event.currentTarget as HTMLElement
  const rect = icon.getBoundingClientRect()
  // Por defecto, a la derecha
  let x = rect.right + 10
  let y = rect.top + rect.height / 2
  // Si se sale del viewport, mostrar a la izquierda
  if (x + 320 > window.innerWidth) x = rect.left - 320 - 10
  // Si tampoco cabe a la izquierda, ponerlo encima
  if (x < 0) x = 10
  if (y + 60 > window.innerHeight) y = window.innerHeight - 70
  tooltipPos.value = { x, y, visible: true, text }
}
function hideTooltip() {
  tooltipTimeout = setTimeout(() => { tooltipPos.value.visible = false }, 80)
}
onBeforeUnmount(() => { if (tooltipTimeout) clearTimeout(tooltipTimeout) })

function getCookie(name: string) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

async function handleRegister() {
  error.value = ''
  try {
    // Realiza un GET para obtener el CSRF token antes de registrar
    await fetch('/api/usuarios/register/', { method: 'GET', credentials: 'include' });
    const csrftoken = getCookie('csrftoken');
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };
    if (csrftoken) headers['X-CSRFToken'] = csrftoken;
    const res = await fetch('/api/usuarios/register/', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        username: username.value.trim(),
        email: email.value.trim(),
        password: password.value,
        tipo_usuario: tipoUsuario.value,
        tipo_documento: tipoDocumento.value,
        numero_documento: numeroDocumento.value,
        fecha_nacimiento: fechaNacimiento.value || null,
        genero: genero.value,
        celular: celular.value,
        telefono_fijo: telefonoFijo.value,
        direccion: direccion.value,
        ciudad: ciudad.value,
        departamento: departamento.value,
        pais: pais.value,
        persona_natural: personaNatural.value,
        anios_experiencia: aniosExperiencia.value ? parseInt(aniosExperiencia.value) : null,
        tipo_vehiculos: tipoVehiculos.value,
        cantidad_vehiculos_mes: cantidadVehiculosMes.value ? parseInt(cantidadVehiculosMes.value) : null,
        licencia_vendedor: licenciaVendedor.value,
        asociacion_sector: asociacionSector.value,
        mostrar_redes: mostrarRedes.value,
        facebook: facebook.value,
        instagram: instagram.value,
        web: web.value,
        recibir_novedades: recibirNovedades.value,
        mostrar_contacto: mostrarContacto.value,
        acepta_politica: aceptaPolitica.value,
        acepta_terminos: aceptaTerminos.value,
        experiencia_ventas: experienciaVentas.value,
        nombre_empresa: nombreEmpresa.value
      }),
      credentials: 'include'
    })
    console.log('Status:', res.status)
    const text = await res.text()
    console.log('Raw response:', text)
    let data
    try {
      data = JSON.parse(text)
    } catch (e) {
      data = { username: ['Respuesta no válida del servidor'] }
    }
    if (res.ok) {
      // Hacer login automático tras registro exitoso
      try {
        // Obtener CSRF para login si el backend lo requiere
        await fetch('/api/usuarios/login/', { method: 'GET', credentials: 'include' });
        const loginCsrftoken = getCookie('csrftoken');
        const loginHeaders: Record<string, string> = {
          'Content-Type': 'application/json'
        };
        if (loginCsrftoken) loginHeaders['X-CSRFToken'] = loginCsrftoken;
        const loginRes = await fetch('/api/usuarios/login/', {
          method: 'POST',
          headers: loginHeaders,
          body: JSON.stringify({
            username: username.value.trim(),
            password: password.value
          }),
          credentials: 'include'
        })
        const loginText = await loginRes.text()
        let loginData
        try {
          loginData = JSON.parse(loginText)
        } catch (e) {
          loginData = { non_field_errors: ['Respuesta no válida del servidor'] }
        }
        if (loginRes.ok) {
          localStorage.setItem('user', JSON.stringify(loginData))
          emit('success', loginData)
          emit('close')
        } else {
          error.value = loginData.non_field_errors?.[0] || loginData.username?.[0] || loginData.password?.[0] || 'Error al iniciar sesión tras registro'
        }
      } catch (e) {
        error.value = 'Error de red al iniciar sesión tras registro'
      }
    } else {
      // Traducción de errores comunes
      if (data.username?.[0]?.includes('already exists') || data.username?.[0]?.includes('ya existe')) {
        error.value = 'El usuario ya existe. Por favor elige otro nombre de usuario.'
      } else if (data.email?.[0]?.includes('already exists') || data.email?.[0]?.includes('ya existe')) {
        error.value = 'El correo electrónico ya está registrado.'
      } else if (data.persona_natural?.[0]) {
        error.value = 'Selecciona si eres persona natural o empresa.'
      } else if (data.facebook?.[0] || data.instagram?.[0] || data.web?.[0]) {
        error.value = 'Las redes sociales y la web deben ser URLs válidas (ejemplo: https://facebook.com/usuario)';
      } else {
        error.value = data.username?.[0] || data.email?.[0] || data.password?.[0] || 'Error de registro'
      }
    }
  } catch (e) {
    error.value = 'Error de red'
  }
}
</script>

<style>
.vendedor-extra-form, .register-main-form {
  background: #fafbfc;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  padding: 1.5rem 2rem 1.2rem 2rem;
  margin-bottom: 1.2rem;
}
.form-section-title {
  font-size: 1.08rem;
  font-weight: 600;
  color: #2d3748;
  margin: 1.2rem 0 0.7rem 0;
  letter-spacing: 0.01em;
  border-left: 3px solid #e53e3e;
  padding-left: 0.7rem;
  background: none;
}
.form-row {
  display: flex;
  gap: 1.2rem;
  margin-bottom: 0.7rem;
}
.form-group label {
  font-weight: 500;
  color: #444;
  margin-bottom: 0.2rem;
}
.form-group input {
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  padding: 0.45rem 0.8rem;
  font-size: 1rem;
  background: #fff;
  transition: border 0.2s;
}
.form-group input:focus {
  border: 1.5px solid #e53e3e;
  outline: none;
}
button[type="submit"] {
  background: linear-gradient(90deg, #e53e3e 0%, #f56565 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 1.5rem;
  font-size: 1.08rem;
  font-weight: 600;
  margin-top: 1.2rem;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(229,62,62,0.08);
  transition: background 0.2s;
}
button[type="submit"]:hover {
  background: linear-gradient(90deg, #c53030 0%, #e53e3e 100%);
}
.form-group select,
select {
  background: #fff !important;
  color: #111 !important;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  padding: 0.45rem 0.8rem;
  font-size: 1rem;
  transition: border 0.2s;
  box-shadow: none !important;
}
.form-group select:focus,
select:focus {
  border: 1.5px solid #e53e3e;
  outline: none;
  background: #fff !important;
  color: #111 !important;
}
select:-webkit-autofill,
select:-webkit-autofill:focus {
  box-shadow: 0 0 0 1000px #fff inset !important;
  -webkit-text-fill-color: #111 !important;
}
select:-internal-autofill-selected {
  background-color: #fff !important;
  color: #111 !important;
}
.preferencias-legal-box {
  background: #f7fafc;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  margin-top: 1.2rem;
  margin-bottom: 1.2rem;
  padding: 1.1rem 1.5rem 0.7rem 1.5rem;
  box-shadow: 0 1px 6px rgba(229,62,62,0.04);
}
.preferencias-title {
  border: none;
  font-size: 1.08rem;
  font-weight: 600;
  color: #c00;
  margin-bottom: 0.7rem;
  padding-left: 0;
  background: none;
}
.preferencias-checkboxes {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 1.04rem;
  color: #333;
  font-weight: 500;
  cursor: pointer;
  user-select: none;
}
.checkbox-label input[type="checkbox"] {
  accent-color: #c00;
  width: 1.15em;
  height: 1.15em;
  margin-right: 0.3em;
  border-radius: 4px;
  border: 1.5px solid #c00;
  background: #fff;
  transition: border 0.2s;
}
.checkbox-label input[type="checkbox"]:focus {
  outline: 2px solid #c00;
}
</style>
