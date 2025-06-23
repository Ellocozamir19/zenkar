<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <h1 class="hero-title">¡Encuentra tu <span class="highlight">auto ideal</span>!</h1>
        <p class="hero-subtitle">Compara coches nuevos, usados, eléctricos y mucho más en segundos.</p>
        <div class="search-container">
          <div class="search-box fullwidth">
            <input
              v-model="search"
              @input="fetchSugerencias"
              @focus="showSugerencias = true"
              @blur="onBlur"
              @keydown.enter="buscar"
              type="text"
              class="search-input"
              placeholder="Buscar marca o modelo..."
              autocomplete="off"
            />
            <ul v-if="showSugerencias && sugerencias.length" class="sugerencias-list">
              <li v-for="(s, i) in sugerencias" :key="i">
                <div class="sugerencia-label" @mousedown.prevent="selectSugerencia(s.label)">
                  {{ s.label }}
                </div>
                <ul v-if="s.modelos && s.modelos.length" class="sugerencia-modelos">
                  <li v-for="(m, j) in s.modelos" :key="j" @mousedown.prevent="selectSugerencia(m.marca + ' ' + m.modelo + (m.version ? ' ' + m.version : ''))">
                    {{ m.marca }} {{ m.modelo }}<span v-if="m.version"> {{ m.version }}</span>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
          <button class="search-btn small" @click="buscar">Comparar</button>
        </div>
        <div class="comparisons-section">
          <p class="comparisons-label">Comparaciones populares</p>
          <div class="quick-comparisons">
            <a href="#" class="comparison-btn" @click.prevent="comparar('Toyota vs Honda')">Toyota vs Honda</a>
            <a href="#" class="comparison-btn" @click.prevent="comparar('BMW vs Audi')">BMW vs Audi</a>
            <a href="#" class="comparison-btn" @click.prevent="comparar('Tesla vs BYD')">Tesla vs BYD</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '../api/axios'
const search = ref('')
const sugerencias = ref<any[]>([])
const showSugerencias = ref(false)

function fetchSugerencias() {
  if (!search.value.trim()) {
    sugerencias.value = []
    return
  }
  api.get('vehiculos/sugerencias/', { params: { q: search.value } })
    .then(res => {
      sugerencias.value = res.data
    })
    .catch(() => {
      sugerencias.value = []
    })
}
function selectSugerencia(s: string) {
  search.value = s
  showSugerencias.value = false
}
function onBlur() {
  setTimeout(() => { showSugerencias.value = false }, 100)
}
function buscar() {
  if (search.value.trim()) {
    alert('Buscando: ' + search.value)
    showSugerencias.value = false
  }
}
function comparar(comparacion: string) {
  alert('Comparación rápida: ' + comparacion)
}
</script>

<style scoped>
@import '../styles/Comparador.css';
@import '../styles/Sugerencias.css';
</style>
