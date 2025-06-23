<script setup lang="ts">
import Header from './components/Header.vue';
import Loader from './components/Loader.vue';
import { useLoaderStore } from './store/loader';
import { storeToRefs } from 'pinia';

const loaderStore = useLoaderStore();
const { loading } = storeToRefs(loaderStore);
</script>

<template>
  <Header />
  <Loader v-if="loading" />
  <router-view />
</template>
