<template>
  <div class="loader-overlay">
    <div class="loader-spinner car-compare-loader">
      <div class="car-container">
        <img
          class="car-img car-left"
          :class="{ arrive: animate }"
          :src="carro1"
          alt="Carro 1"
        />
        <div class="vs-label">VS</div>
        <img
          class="car-img car-right"
          :class="{ arrive: animate }"
          :src="carro2"
          alt="Carro 2"
        />
      </div>
      <div class="loader-text">Comparando vehículos...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLoaderStore } from '../store/loader'
import carro1 from '../assets/carro1-loader.png'
import carro2 from '../assets/carro2-loader.png'
const animate = ref(false)
const loader = useLoaderStore()

onMounted(() => {
  loader.show(10000) // muestra el loader por 10 segundos
  setTimeout(() => { animate.value = true }, 600)
  setInterval(() => {
    animate.value = false
    setTimeout(() => { animate.value = true }, 600)
  }, 30000)
})
</script>

<style src="../styles/Loader.css"></style>
