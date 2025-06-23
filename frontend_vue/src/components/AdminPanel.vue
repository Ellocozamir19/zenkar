<template>
  <div v-if="hasPermission" class="admin-panel-full">
    <!-- Header del panel admin (NO el global de la app) -->
    <header class="admin-header">
      <h1>Panel de Administración - Admin</h1>
    </header>
    <!-- Tabs y Add Button en la misma fila -->
    <div class="admin-tabs-row">
      <nav class="admin-tabs">
        <button :class="{active: activeTab==='usuarios'}" @click="activeTab='usuarios'">
          <span class="tab-icon" style="margin-right:0.5em;">
            <img :class="{ 'tab-icon-active': activeTab==='usuarios' }" src="../svg/panel-usuarios.svg" alt="Usuarios" style="width:22px;height:22px;" />
          </span>
          Usuarios
        </button>
        <button :class="{active: activeTab==='vehiculos'}" @click="activeTab='vehiculos'">
          <span class="tab-icon" style="margin-right:0.5em;">
            <img :class="{ 'tab-icon-active': activeTab==='vehiculos' }" src="../svg/panel-vehiculos.svg" alt="Vehículos" style="width:22px;height:22px;" />
          </span>
          Vehículos
        </button>
        <button :class="{active: activeTab==='peticiones'}" @click="activeTab='peticiones'">
          <span class="tab-icon" style="margin-right:0.5em;">
            <img class="peticiones-icon" src="../svg/peticiones.svg" alt="Peticiones" style="width:22px;height:22px;" />
          </span>
          Peticiones
        </button>
      </nav>
      <div class="admin-add-btn" v-if="activeTab!=='peticiones'">
        <button @click="openModal(activeTab==='usuarios' ? 'usuario' : 'vehiculo')">
          <span class="tab-icon"><img :class="{ 'tab-icon-active': true }" src="../svg/panel-agregar.svg" alt="Agregar" style="width:20px;height:20px;" /></span>
          Agregar {{ activeTab==='usuarios' ? 'Usuario' : 'Vehículo' }}
        </button>
      </div>
    </div>
    <!-- Content -->
    <div class="admin-content">
      <div v-if="activeTab==='usuarios'" class="admin-search-row">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por usuario o email..."
          class="admin-search-input"
          autocomplete="off"
        />
      </div>
      <table v-if="activeTab==='usuarios'">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Email</th>
            <th>Tipo</th>
            <th class="actions-col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="usuario in filteredUsuarios" :key="usuario.id">
            <td>
              <div class="user-cell">
                <div class="user-avatar-sm">{{ usuario.usuario.charAt(0) }}</div>
                <span>{{ usuario.usuario }}</span>
              </div>
            </td>
            <td>{{ usuario.email }}</td>
            <td>
              <span :class="['user-type-chip', usuario.tipo==='Admin' ? 'admin' : '', usuario.tipo==='Admin Mayor' ? 'admin-mayor' : '']">{{ usuario.tipo }}</span>
            </td>
            <td class="actions-col">
              <div class="action-buttons">
                <button v-if="canEditUser(usuario)" @click="openModal('usuario', usuario)" title="Editar" class="action-btn-edit">
                  <img :src="editIcon" alt="Editar" class="action-icon" />
                </button>
                <button v-if="canChangeRole(usuario)" @click="toggleAdmin(usuario.id)" title="Cambiar rol" class="action-btn-role">
                  <img :src="roleIcon" alt="Cambiar rol" class="action-icon" />
                </button>
                <button v-if="canDeleteUser(usuario)" @click="deleteItem(usuario.id, 'usuario')" title="Eliminar" class="action-btn-delete">
                  <img :src="deleteIcon" alt="Eliminar" class="action-icon" />
                </button>
                <button @click="openUserDetails(usuario)" title="Ver detalles" class="action-btn-details">
                  <img :src="detallarIcon" alt="Detalles" class="action-icon" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="activeTab==='vehiculos'" class="admin-search-row">
        <input
          v-model="searchVehiculo"
          type="text"
          placeholder="Buscar por marca, modelo o año..."
          class="admin-search-input"
          autocomplete="off"
        />
      </div>
      <table v-if="activeTab==='vehiculos'">
        <thead>
          <tr>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Año</th>
            <th class="actions-col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vehiculo in filteredVehiculos" :key="vehiculo.id">
            <td>
              <div class="user-cell">
                <div class="user-avatar-sm">{{ vehiculo.marca?.charAt(0) }}</div>
                <span>{{ vehiculo.marca }}</span>
              </div>
            </td>
            <td>{{ vehiculo.modelo }}</td>
            <td>{{ vehiculo.anio }}</td>
            <td class="actions-col">
              <div class="action-buttons">
                <button @click="openModal('vehiculo', vehiculo)" title="Editar">
                  <img :src="editarCarroIcon" alt="Editar" class="action-icon" />
                </button>
                <button @click="deleteItem(vehiculo.id, 'vehiculo')" title="Eliminar">
                  <img :src="deleteIcon" alt="Eliminar" class="action-icon" />
                </button>
                <button @click="openVehiculoInfo(vehiculo)" title="Ver detalles">
                  <img :src="infoIcon" alt="Detalles" class="action-icon" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="activeTab==='peticiones'">
        <h2 style="margin-bottom:1rem;">Peticiones de Cambio de Perfil</h2>
        <table v-if="peticiones.length">
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Datos Solicitados</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pet in peticiones" :key="pet.id">
              <td>{{ pet.id }}</td>
              <td>{{ pet.usuario_username }}</td>
              <td>
                <ul v-if="pet.datos_nuevos && Object.keys(pet.datos_nuevos).length" style="margin:0;padding:0 0 0 1.1em;list-style:square inside;font-size:1em;">
                  <li v-for="(valor, campo) in pet.datos_nuevos" :key="campo">
                    <b>{{ campo === 'username' ? 'Usuario' : campo === 'email' ? 'Email' : campo === 'password' ? 'Contraseña' : campo }}:</b>
                    <span v-if="campo !== 'password'">{{ valor }}</span>
                    <span v-else>••••••••</span>
                  </li>
                </ul>
                <span v-else style="color:#b91c1c;font-weight:600;">Sin datos solicitados</span>
              </td>
              <td>
                <span :style="{color: pet.estado==='pendiente' ? '#b7791f' : pet.estado==='aprobada' ? '#38a169' : '#e53e3e', fontWeight:'bold'}">{{ pet.estado }}</span>
                <div v-if="pet.estado==='rechazada' && pet.razon_rechazo" style="font-size:0.95em;color:#b91c1c;">Motivo: {{ pet.razon_rechazo }}</div>
              </td>
              <td>
                <div v-if="pet.estado==='pendiente'" style="display:flex;gap:0.5rem;align-items:center;">
                  <button @click="aprobarPeticion(pet.id)" class="peticion-aprobar-btn">Aprobar</button>
                  <button @click="rechazarPeticion(pet.id)" class="peticion-rechazar-btn">Rechazar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else style="color:#b91c1c;font-weight:600;">No hay peticiones registradas.</div>
      </div>
    </div>
    <!-- Modal -->
    <div v-if="showModal" class="admin-modal-overlay">
      <div class="admin-modal" style="max-width:520px; max-height:90vh; min-width:350px; overflow-y:auto; display:flex; flex-direction:column; justify-content:flex-start; align-items:center; margin-top:40px;">
        <div class="admin-modal-header" style="position:relative;height:56px;padding:0;width:100%;min-width:350px;">
          <div style="position:absolute;left:0;top:50%;transform:translateY(-50%);width:100%;text-align:center;font-weight:700;font-size:1.2rem;color:var(--rojo);pointer-events:none;z-index:1;">
            {{ editingItem ? 'Editar' : 'Agregar' }} {{ modalType==='usuario' ? 'Usuario' : 'Vehículo' }}
          </div>
        </div>
        <form @submit.prevent="handleSubmit" style="width:100%;display:flex;flex-direction:column;flex:1;">
          <div class="admin-modal-body" style="overflow-y:auto;max-height:60vh;width:100%;padding-bottom:1rem;">
            <div v-if="modalType==='usuario'">
              <label>Nombre completo</label>
              <input v-model="formData.usuario" required placeholder="Ingrese el nombre completo" />
              <label>Email</label>
              <input v-model="formData.email" type="email" required placeholder="correo@ejemplo.com" />
              <label>Contraseña</label>
              <div style="position:relative;display:flex;align-items:center;">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="formData.password"
                  :required="!editingItem"
                  placeholder="Contraseña"
                  style="padding-right:2.5rem;width:100%;box-sizing:border-box;"
                />
                <img
                  :src="showPassword ? openDoor : openClosed"
                  :alt="showPassword ? 'Mostrar contraseña' : 'Ocultar contraseña'"
                  @click="showPassword = !showPassword"
                  style="position:absolute;right:0.7rem;top:39%;transform:translateY(-50%);width:22px;height:22px;cursor:pointer;user-select:none;background:#f3f4f6;border-radius:50%;pointer-events:auto;box-shadow:0 1px 2px rgba(0,0,0,0.04);"
                />
              </div>
              <label>Tipo de usuario</label>
              <select v-model="formData.tipo" required>
                <option value="">Seleccione un tipo</option>
                <option value="Usuario">Usuario</option>
                <option value="Vendedor">Vendedor</option>
              </select>
              <template v-if="formData.tipo === 'Vendedor'">
                <label>Tipo de documento</label>
                <input v-model="formData.tipo_documento" placeholder="CC, CE, NIT..." />
                <label>Número de documento</label>
                <input v-model="formData.numero_documento" placeholder="Número de documento" />
                <label>Fecha de nacimiento</label>
                <input v-model="formData.fecha_nacimiento" type="date" />
                <label>Género</label>
                <input v-model="formData.genero" placeholder="Masculino, Femenino, Otro..." />
                <label>Celular</label>
                <input v-model="formData.celular" placeholder="Celular" />
                <label>Teléfono fijo</label>
                <input v-model="formData.telefono_fijo" placeholder="Teléfono fijo" />
                <label>Dirección</label>
                <input v-model="formData.direccion" placeholder="Dirección" />
                <label>Ciudad</label>
                <input v-model="formData.ciudad" placeholder="Ciudad" />
                <label>Departamento</label>
                <input v-model="formData.departamento" placeholder="Departamento" />
                <label>País</label>
                <input v-model="formData.pais" placeholder="País" />
                <label>Tipo de persona</label>
                <input v-model="formData.persona_natural" placeholder="natural o empresa" />
                <label>Nombre empresa</label>
                <input v-model="formData.nombre_empresa" placeholder="Nombre empresa" />
                <label>Años de experiencia</label>
                <input v-model.number="formData.anios_experiencia" type="number" min="0" placeholder="Años de experiencia" />
                <label>Tipo de vehículos</label>
                <input v-model="formData.tipo_vehiculos" placeholder="Autos, motos, camiones..." />
                <label>Cantidad vehículos/mes</label>
                <input v-model.number="formData.cantidad_vehiculos_mes" type="number" min="0" placeholder="Cantidad vehículos/mes" />
                <label>Licencia vendedor</label>
                <input v-model="formData.licencia_vendedor" placeholder="Licencia vendedor" />
                <label>Asociación sector</label>
                <input v-model="formData.asociacion_sector" placeholder="Asociación sector" />
                <label>Facebook</label>
                <input v-model="formData.facebook" placeholder="Facebook" />
                <label>Instagram</label>
                <input v-model="formData.instagram" placeholder="Instagram" />
                <label>Página web</label>
                <input v-model="formData.web" placeholder="Página web" />
                <label>Recibir novedades</label>
                <select v-model="formData.recibir_novedades">
                  <option :value="true">Sí</option>
                  <option :value="false">No</option>
                </select>
                <label>Mostrar contacto</label>
                <select v-model="formData.mostrar_contacto">
                  <option :value="true">Sí</option>
                  <option :value="false">No</option>
                </select>
              </template>
            </div>
            <div v-else>
              <label style="margin-top:18px;display:block;">Marca</label>
              <input v-model="formData.marca" required placeholder="Toyota, Honda, Ford..." />
              <label>Modelo</label>
              <input v-model="formData.modelo" required placeholder="Corolla, Civic, Focus..." />
              <label>Año</label>
              <input v-model.number="formData.anio" type="number" min="1900" max="2025" required placeholder="2023" />
              <label>Versión</label>
              <input v-model="formData.version" placeholder="LE, XLE, Sport..." />
              <label>Categoría</label>
              <input v-model="formData.categoria" placeholder="Sedán, SUV, Hatchback..." />
              <label>Transmisión</label>
              <input v-model="formData.transmision" placeholder="Manual, Automática..." />
              <label>Combustible</label>
              <input v-model="formData.combustible" placeholder="Gasolina, Diesel, Híbrido..." />
              <label>Motor</label>
              <input v-model="formData.motor" placeholder="1.8L, 2.0L Turbo..." />
              <label>Puertas</label>
              <input v-model.number="formData.puertas" type="number" min="2" max="6" placeholder="4" />
              <label>Cilindraje</label>
              <input v-model="formData.cilindraje" placeholder="1798cc, 2000cc..." />
              <label>Potencia HP</label>
              <input v-model.number="formData.potencia_hp" type="number" placeholder="140" />
              <label>Torque</label>
              <input v-model="formData.torque" placeholder="175 Nm..." />
              <label>Alimentación</label>
              <input v-model="formData.alimentacion" placeholder="Inyección, Turbo..." />
              <label>Árbol de levas</label>
              <input v-model="formData.arbol_levas" placeholder="SOHC, DOHC..." />
              <label>Válvulas</label>
              <input v-model.number="formData.valvulas" type="number" placeholder="16" />
              <label>Largo (mm)</label>
              <input v-model.number="formData.largo" type="number" placeholder="4500" />
              <label>Ancho (mm)</label>
              <input v-model.number="formData.ancho" type="number" placeholder="1750" />
              <label>Alto (mm)</label>
              <input v-model.number="formData.alto" type="number" placeholder="1450" />
              <label>Peso (kg)</label>
              <input v-model.number="formData.peso" type="number" placeholder="1200" />
              <label>Volumen baúl (L)</label>
              <input v-model.number="formData.volumen_baul" type="number" placeholder="400" />
              <label>Tracción</label>
              <input v-model="formData.traccion" placeholder="Delantera, Trasera..." />
              <label>Capacidad tanque (L)</label>
              <input v-model.number="formData.capacidad_tanque" type="number" placeholder="50" />
              <label>Airbags</label>
              <input v-model.number="formData.airbags" type="number" placeholder="2" />
              <label>ABS</label>
              <select v-model="formData.abs"><option :value="true">Sí</option><option :value="false">No</option></select>
              <label>Frenos delanteros</label>
              <input v-model="formData.frenos_delanteros" placeholder="Disco, Tambor..." />
              <label>Frenos traseros</label>
              <input v-model="formData.frenos_traseros" placeholder="Disco, Tambor..." />
              <label>Bloqueo central</label>
              <select v-model="formData.bloqueo_central"><option :value="true">Sí</option><option :value="false">No</option></select>
              <label>Cinturones</label>
              <input v-model.number="formData.cinturones" type="number" placeholder="5" />
              <label>Aire acondicionado</label>
              <select v-model="formData.aire_acondicionado"><option :value="true">Sí</option><option :value="false">No</option></select>
              <label>Vidrios eléctricos</label>
              <select v-model="formData.vidrios_electricos"><option :value="true">Sí</option><option :value="false">No</option></select>
              <label>Bluetooth</label>
              <select v-model="formData.bluetooth"><option :value="true">Sí</option><option :value="false">No</option></select>
              <label>USB</label>
              <select v-model="formData.usb"><option :value="true">Sí</option><option :value="false">No</option></select>
              <label>Radio</label>
              <select v-model="formData.radio"><option :value="true">Sí</option><option :value="false">No</option></select>
              <label>Dirección</label>
              <input v-model="formData.direccion" placeholder="Hidráulica, Eléctrica..." />
              <label>Suspensión delantera</label>
              <input v-model="formData.suspension_delantera" placeholder="McPherson..." />
              <label>Suspensión trasera</label>
              <input v-model="formData.suspension_trasera" placeholder="Barra de torsión..." />
              <label>Imagen</label>
              <div style="display:flex;gap:1rem;align-items:center;flex-wrap:wrap;">
                <label style="font-weight:400;">
                  <input type="radio" value="url" v-model="formData.imagenTipo" /> URL
                </label>
                <label style="font-weight:400;">
                  <input type="radio" value="archivo" v-model="formData.imagenTipo" /> Archivo
                </label>
              </div>
              <div v-if="formData.imagenTipo === 'url' || !formData.imagenTipo">
                <input v-model="formData.imagen" placeholder="https://..." />
              </div>
              <div v-else>
                <input type="file" @change="onFileChange" accept="image/*" />
                <div v-if="formData.imagenPreview">
                  <img :src="formData.imagenPreview" alt="Vista previa" style="max-width:100%;max-height:120px;margin-top:0.5rem;" />
                </div>
              </div>
            </div>
          </div>
          <div class="admin-modal-actions" style="background:#fff;z-index:2;display:flex;gap:1rem;justify-content:center;align-items:center;width:100%;padding:1.2rem 0 0.5rem 0;box-shadow:0 -2px 8px rgba(0,0,0,0.04);">
            <button type="button" @click="closeModal" style="background:#e2e8f0;color:#222;border:none;border-radius:7px;padding:0.48rem 1.25rem;font-size:1rem;font-weight:500;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,0.04);transition:background 0.2s;min-width:110px;max-width:140px;">Cancelar</button>
            <button type="submit" style="background:#e53e3e;color:#fff;border:none;border-radius:7px;padding:0.48rem 1.25rem;font-size:1rem;font-weight:500;cursor:pointer;box-shadow:0 1px 4px rgba(229,62,62,0.08);transition:background 0.2s;min-width:110px;max-width:140px;">{{ editingItem ? 'Actualizar' : 'Crear' }}</button>
          </div>
        </form>
      </div>
    </div>
    <!-- Modal de información de vehículo -->
    <div v-if="showVehiculoInfo" class="admin-modal-overlay">
      <div class="admin-modal vehiculo-info-modal">
        <div class="admin-modal-header vehiculo-info-header">
          <div style="display:flex;align-items:center;gap:0.7rem;">
            <img :src="infoIcon" alt="Detalles" />
            <h3>Detalles del Vehículo</h3>
          </div>
        </div>
        <div class="admin-modal-body vehiculo-info-body">
          <template v-if="vehiculoInfo">
            <div v-for="key in [
              'marca','modelo','anio','version','categoria','transmision','combustible','motor','puertas','cilindraje','potencia_hp','torque','alimentacion','arbol_levas','valvulas','largo','ancho','alto','peso','volumen_baul','traccion','capacidad_tanque','airbags','abs','frenos_delanteros','frenos_traseros','bloqueo_central','cinturones','aire_acondicionado','vidrios_electricos','bluetooth','usb','radio','direccion','suspension_delantera','suspension_trasera','imagen']" :key="key" style="margin-bottom:0.7rem;">
              <template v-if="key === 'imagen' && typeof vehiculoInfo[key] === 'string' && vehiculoInfo[key]">
                <div class="vehiculo-img">
                  <img :src="vehiculoInfo[key]" alt="Imagen del vehículo" />
                </div>
              </template>
              <template v-else>
                <div style="display:flex;align-items:center;gap:0.7rem;">
                  <span class="vehiculo-label">{{ key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) }}:</span>
                  <span class="vehiculo-value">{{ vehiculoInfo[key] === true ? 'Sí' : vehiculoInfo[key] === false ? 'No' : (vehiculoInfo[key] ?? '-') }}</span>
                </div>
              </template>
            </div>
          </template>
          <div v-else style="color:#b91c1c;font-weight:600;">No hay información disponible.</div>
        </div>
        <div class="admin-modal-actions vehiculo-info-actions">
          <button type="button" @click="closeVehiculoInfo">Cerrar</button>
        </div>
      </div>
    </div>
    <!-- Modal de detalles de usuario (mejorado, sin emojis y más minimalista) -->
    <div v-if="showUserDetails" class="admin-modal-overlay">
      <div class="admin-modal user-details-modal" style="max-width:440px;min-width:300px;background:#fff;border-radius:16px;box-shadow:0 4px 32px rgba(0,0,0,0.09);padding:0;overflow:hidden;">
        <div class="admin-modal-header user-details-header" style="display:flex;align-items:center;gap:0.7rem;padding:1.2rem 1.5rem 0.5rem 1.5rem;background:#fafbfc;border-bottom:1px solid #f1f1f1;">
          <img :src="detallarIcon" alt="Detalles" style="width:24px;height:24px;object-fit:contain;opacity:0.85;" />
          <h3 style="margin:0;font-size:1.13rem;font-weight:600;color:#2d3748;">Detalles del Usuario</h3>
        </div>
        <div class="admin-modal-body user-details-body" style="padding:1.2rem 1.5rem;max-height:60vh;overflow-y:auto;">
          <template v-if="userDetails">
            <div v-if="userDetails.tipo_usuario === 'vendedor'">
              <div class="form-section-title">Datos Personales</div>
              <div class="user-details-row" v-if="userDetails.username"><b>Usuario:</b> <span>{{ userDetails.username || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.email"><b>Email:</b> <span>{{ userDetails.email || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.tipo_documento"><b>Tipo de documento:</b> <span>{{ userDetails.tipo_documento || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.numero_documento"><b>Número de documento:</b> <span>{{ userDetails.numero_documento || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.fecha_nacimiento"><b>Fecha de nacimiento:</b> <span>{{ userDetails.fecha_nacimiento || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.genero"><b>Género:</b> <span>{{ userDetails.genero || 'No registrado' }}</span></div>
              <div class="form-section-title">Contacto</div>
              <div class="user-details-row" v-if="userDetails.celular"><b>Celular:</b> <span>{{ userDetails.celular || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.telefono_fijo"><b>Teléfono fijo:</b> <span>{{ userDetails.telefono_fijo || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.direccion"><b>Dirección:</b> <span>{{ userDetails.direccion || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.ciudad"><b>Ciudad:</b> <span>{{ userDetails.ciudad || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.departamento"><b>Departamento:</b> <span>{{ userDetails.departamento || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.pais"><b>País:</b> <span>{{ userDetails.pais || 'No registrado' }}</span></div>
              <div class="form-section-title">Perfil Profesional</div>
              <div class="user-details-row" v-if="userDetails.persona_natural"><b>Tipo de persona:</b> <span>{{ userDetails.persona_natural || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.nombre_empresa"><b>Nombre empresa:</b> <span>{{ userDetails.nombre_empresa || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.anios_experiencia !== undefined"><b>Años de experiencia:</b> <span>{{ userDetails.anios_experiencia ?? 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.tipo_vehiculos"><b>Tipo de vehículos:</b> <span>{{ userDetails.tipo_vehiculos || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.cantidad_vehiculos_mes !== undefined"><b>Cantidad vehículos/mes:</b> <span>{{ userDetails.cantidad_vehiculos_mes ?? 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.licencia_vendedor"><b>Licencia vendedor:</b> <span>{{ userDetails.licencia_vendedor || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.asociacion_sector"><b>Asociación sector:</b> <span>{{ userDetails.asociacion_sector || 'No registrado' }}</span></div>
              <div class="form-section-title">Presencia Online</div>
              <div class="user-details-row" v-if="userDetails.facebook"><b>Facebook:</b> <span>{{ userDetails.facebook || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.instagram"><b>Instagram:</b> <span>{{ userDetails.instagram || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.web"><b>Página web:</b> <span>{{ userDetails.web || 'No registrado' }}</span></div>
              <div class="form-section-title">Preferencias y Legal</div>
              <div class="user-details-row" v-if="userDetails.recibir_novedades !== undefined"><b>Recibir novedades:</b> <span>{{ userDetails.recibir_novedades ? 'Sí' : 'No' }}</span></div>
              <div class="user-details-row" v-if="userDetails.mostrar_contacto !== undefined"><b>Mostrar contacto:</b> <span>{{ userDetails.mostrar_contacto ? 'Sí' : 'No' }}</span></div>
            </div>
            <div v-else>
              <div class="form-section-title">Datos Básicos</div>
              <div class="user-details-row" v-if="userDetails.username"><b>Usuario:</b> <span>{{ userDetails.username || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.email"><b>Email:</b> <span>{{ userDetails.email || 'No registrado' }}</span></div>
              <div class="user-details-row" v-if="userDetails.tipo_usuario"><b>Tipo:</b> <span>{{ userDetails.tipo_usuario || 'No registrado' }}</span></div>
            </div>
          </template>
          <div v-else style="color:#b91c1c;font-weight:600;">No hay información disponible.</div>
        </div>
        <div class="admin-modal-actions user-details-actions" style="padding:1rem 0 0.5rem 0;display:flex;justify-content:center;align-items:center;background:#fafbfc;border-top:1px solid #f1f1f1;">
          <button type="button" @click="closeUserDetails" style="background:#e53e3e;color:#fff;border:none;border-radius:7px;padding:0.38rem 1.05rem;font-size:0.97rem;font-weight:500;cursor:pointer;box-shadow:0 1px 4px rgba(229,62,62,0.08);transition:background 0.2s;min-width:90px;max-width:120px;">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else style="padding:2rem;text-align:center;color:#b91c1c;font-weight:bold;">
    No tienes permisos para acceder a este panel.
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '../api/axios'
import { useLoaderStore } from '../store/loader'
import '../styles/AdminPanel.css'
import openDoor from '../svg/open-door.svg?url'
import openClosed from '../svg/open-closed.svg?url'
import editIcon from '../svg/edit.svg?url'
import roleIcon from '../svg/role.svg?url'
import deleteIcon from '../svg/delete.svg?url'
import infoIcon from '../svg/info.svg?url'
import editarCarroIcon from '../svg/editar_carro.svg?url'
import detallarIcon from '../svg/detallar.svg.svg?url'

const activeTab = ref<'usuarios'|'vehiculos'|'peticiones'>('usuarios')
const showModal = ref(false)
const modalType = ref<'usuario'|'vehiculo'>('usuario')
const editingItem = ref<any>(null)
const formData = ref<any>({})
const showPassword = ref(false)

const usuarios = ref<any[]>([])
const vehiculos = ref<any[]>([])
const peticiones = ref<any[]>([])

const currentUser = ref({
  id: 100,
  tipo: 'admin'
})
const hasPermission = computed(() => ["admin", "admin_mayor"].includes(currentUser.value.tipo))
const loader = useLoaderStore();

onMounted(async () => {
  loader.show();
  try {
    await fetchUsuarios();
    await fetchVehiculos();
    await fetchPeticiones();
  } finally {
    loader.hide();
  }
})

function mapTipoUsuario(tipo_usuario: string) {
  switch ((tipo_usuario || '').toLowerCase()) {
    case 'admin_mayor':
      return 'Admin Mayor'
    case 'admin':
      return 'Admin'
    case 'vendedor':
      return 'Vendedor'
    default:
      return 'Usuario'
  }
}

function openModal(type: 'usuario'|'vehiculo', item: any = null) {
  if (
    type === 'usuario' &&
    currentUser.value.tipo === 'admin' &&
    item && (item.tipo === 'Admin' || item.tipo === 'Admin Mayor')
  ) {
    return
  }
  modalType.value = type
  editingItem.value = item
  if (type === 'vehiculo' && item) {
    formData.value = { ...item, imagenTipo: item.imagen ? 'url' : '', imagenPreview: '' }
  } else {
    formData.value = item ? { ...item } : {}
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  modalType.value = 'usuario'
  editingItem.value = null
  formData.value = {}
}
const onFileChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    formData.value.imagenArchivo = file
    formData.value.imagenPreview = URL.createObjectURL(file)
  } else {
    formData.value.imagenArchivo = null
    formData.value.imagenPreview = null
  }
}
async function handleSubmit() {
  if (modalType.value === 'usuario') {
    if (!formData.value.usuario || !formData.value.email || !formData.value.tipo) return
    if (
      currentUser.value.tipo === 'admin' &&
      (formData.value.tipo === 'Admin' || formData.value.tipo === 'Admin Mayor')
    ) {
      alert('No tienes permisos para asignar este tipo de usuario.')
      return
    }
    let tipo_usuario = formData.value.tipo
    if (tipo_usuario === 'Admin Mayor') tipo_usuario = 'admin_mayor'
    if (tipo_usuario === 'Admin') tipo_usuario = 'admin'
    if (tipo_usuario === 'Vendedor') tipo_usuario = 'vendedor'
    if (tipo_usuario === 'Usuario') tipo_usuario = 'usuario'
    try {
      if (editingItem.value) {
        const payload: { username: string; email: string; tipo_usuario: string; password?: string } = {
          username: formData.value.usuario,
          email: formData.value.email,
          tipo_usuario: tipo_usuario
        }
        if (formData.value.password && formData.value.password !== '') payload.password = formData.value.password
        await api.put(`/api/usuarios/${editingItem.value.id}/editar/`, payload)
        const res = await api.get('/api/usuarios/listar/')
        usuarios.value = res.data.map((u: any) => ({
          id: u.id,
          usuario: u.username,
          email: u.email,
          tipo: mapTipoUsuario(u.tipo_usuario)
        }))
      } else {
        const payload = {
          username: formData.value.usuario,
          email: formData.value.email,
          tipo_usuario: tipo_usuario,
          password: formData.value.password
        }
        await api.post('/api/usuarios/register/', payload)
        const res = await api.get('/api/usuarios/listar/')
        usuarios.value = res.data.map((u: any) => ({
          id: u.id,
          usuario: u.username,
          email: u.email,
          tipo: mapTipoUsuario(u.tipo_usuario)
        }))
      }
    } catch (e: any) {
      if (e.response && e.response.data && e.response.data.detail) {
        alert('Error: ' + e.response.data.detail)
      } else if (e.response && e.response.data) {
        alert('Error: ' + JSON.stringify(e.response.data))
      } else {
        alert('Error actualizando el usuario')
      }
      return
    }
  } else {
    if (!formData.value.marca || !formData.value.modelo || !formData.value.anio) return
    try {
      let payload: any = { ...formData.value }
      // Si la imagen es por archivo, primero la subimos y guardamos la URL en 'imagen'
      if (formData.value.imagenTipo === 'archivo' && formData.value.imagenArchivo) {
        const imgData = new FormData()
        imgData.append('imagen', formData.value.imagenArchivo)
        const resImg = await api.post('/api/vehiculos/upload_imagen/', imgData, { headers: { 'Content-Type': 'multipart/form-data' } })
        payload.imagen = resImg.data.url || resImg.data.imagen || ''
      }
      // Siempre eliminar los campos auxiliares y NUNCA enviar imagen_archivo
      delete payload.imagenArchivo
      delete payload.imagenPreview
      delete payload.imagenTipo
      // Nunca enviar imagen_archivo (por si acaso)
      delete payload.imagen_archivo
      if (editingItem.value) {
        await api.put(`/api/vehiculos/${editingItem.value.id}/editar/`, payload)
      } else {
        await api.post('/api/vehiculos/crear/', payload)
      }
      const resVehiculos = await api.get('/api/vehiculos/listar/')
      vehiculos.value = resVehiculos.data.map((v: any) => ({
        ...v,
        anio: v.anio || v.año || v.year
      }))
    } catch (e: any) {
      alert('Error al guardar el vehículo')
      return
    }
  }
  closeModal()
}
function deleteItem(id: number, type: 'usuario'|'vehiculo') {
  if (type === 'usuario') {
    usuarios.value = usuarios.value.filter(u => u.id !== id)
    api.delete(`/api/usuarios/${id}/eliminar/`).catch(() => {})
  } else {
    vehiculos.value = vehiculos.value.filter(v => v.id !== id)
    api.delete(`/api/vehiculos/${id}/eliminar/`).catch(() => {})
  }
}
async function toggleAdmin(id: number) {
  const usuario = usuarios.value.find(u => u.id === id)
  if (!usuario) return
  let nuevoTipo = ''
  let tipo_usuario = ''
  if (usuario.tipo === 'Admin') {
    nuevoTipo = 'Usuario'
    tipo_usuario = 'usuario'
  } else if (usuario.tipo === 'Usuario' || usuario.tipo === 'Vendedor') {
    nuevoTipo = 'Admin'
    tipo_usuario = 'admin'
  } else if (usuario.tipo === 'Admin Mayor') return
  try {
    await api.put(`/api/usuarios/${id}/editar/`, {
      username: usuario.usuario,
      email: usuario.email,
      tipo_usuario
    })
    usuarios.value = usuarios.value.map(u =>
      u.id === id ? { ...u, tipo: nuevoTipo } : u
    )
  } catch (e: any) {
    if (e.response && e.response.data && e.response.data.detail) {
      alert('Error: ' + e.response.data.detail)
    } else if (e.response && e.response.data) {
      const data = e.response.data
      let msg = ''
      if (typeof data === 'object') {
        for (const key in data) {
          msg += `${key}: ${data[key]}\n`
        }
      } else {
        msg = JSON.stringify(data)
      }
      alert('Error: ' + msg)
    } else {
      alert('Error actualizando el tipo de usuario')
    }
  }
}
const canEditUser = (usuario: any) => {
  return usuario.tipo === 'Usuario' || usuario.tipo === 'Vendedor'
}
const canDeleteUser = (usuario: any) => {
  return usuario.tipo === 'Usuario' || usuario.tipo === 'Vendedor'
}
const canChangeRole = (usuario: any) => {
  if (currentUser.value.tipo === 'admin') return false
  return usuario.tipo === 'Usuario' || usuario.tipo === 'Vendedor'
}
const searchQuery = ref('')
function filterUsuarios() {
  if (!searchQuery.value) {
    return usuarios.value
  }
  const query = searchQuery.value.toLowerCase()
  return usuarios.value.filter(u =>
    u.usuario.toLowerCase().includes(query) ||
    u.email.toLowerCase().includes(query)
  )
}
const filteredUsuarios = computed(() => filterUsuarios())
const searchVehiculo = ref('')
const filteredVehiculos = computed(() => {
  const q = searchVehiculo.value.trim().toLowerCase()
  if (!q) return vehiculos.value
  return vehiculos.value.filter(v =>
    (v.marca?.toLowerCase?.().includes(q) || false) ||
    (v.modelo?.toLowerCase?.().includes(q) || false) ||
    ((v.anio + '').includes(q))
  )
})
const showVehiculoInfo = ref(false)
const vehiculoInfo = ref<any>(null)
function openVehiculoInfo(vehiculo: any) {
  vehiculoInfo.value = vehiculo
  showVehiculoInfo.value = true
}
function closeVehiculoInfo() {
  showVehiculoInfo.value = false
  vehiculoInfo.value = null
}
const showUserDetails = ref(false)
const userDetails = ref<any>(null)
// Reemplazar openUserDetails para obtener todos los datos extendidos del usuario
async function openUserDetails(usuario: any) {
  try {
    // Obtener datos completos del usuario desde la API
    const res = await api.get(`/api/usuarios/${usuario.id}/detalle/`)
    userDetails.value = res.data
  } catch (e) {
    userDetails.value = { ...usuario }
  }
  showUserDetails.value = true
}
function closeUserDetails() {
  showUserDetails.value = false
  userDetails.value = null
}

// Nuevas funciones y estados para peticiones
function pretty(obj: any) {
  try {
    return JSON.stringify(obj, null, 2)
  } catch {
    return obj
  }
}

function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchUsuarios() {
  loader.show();
  try {
    const res = await api.get('/api/usuarios/');
    await delay(1000);
    usuarios.value = res.data;
  } catch (e) {
    usuarios.value = [];
  } finally {
    loader.hide();
  }
}

async function fetchVehiculos() {
  loader.show();
  try {
    const res = await api.get('/api/vehiculos/');
    await delay(1000);
    vehiculos.value = res.data;
  } catch (e) {
    vehiculos.value = [];
  } finally {
    loader.hide();
  }
}

async function fetchPeticiones() {
  loader.show();
  try {
    const res = await api.get('/api/usuarios/peticiones_cambio/');
    await delay(1000);
    peticiones.value = res.data;
  } catch (e) {
    peticiones.value = [];
  } finally {
    loader.hide();
  }
}

async function aprobarPeticion(id: number) {
  try {
    await api.post(`/api/usuarios/peticion_cambio/${id}/aprobar/`)
    await fetchPeticiones()
  } catch (e) {
    alert('Error al aprobar la petición')
  }
}

async function rechazarPeticion(id: number) {
  const razon = prompt('Motivo del rechazo:')
  try {
    await api.post(`/api/usuarios/peticion_cambio/${id}/rechazar/`, { razon_rechazo: razon })
    await fetchPeticiones()
  } catch (e) {
    alert('Error al rechazar la petición')
  }
}

// Filtro para mostrar JSON bonito en tabla
const app = { config: { globalProperties: {} } } as any
if (typeof app.config.globalProperties.$filters === 'undefined') app.config.globalProperties.$filters = {}
app.config.globalProperties.$filters.pretty = pretty
</script>
