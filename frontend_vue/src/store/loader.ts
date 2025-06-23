import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useLoaderStore = defineStore('loader', () => {
  const loading = ref(false);
  let timeoutId: number | null = null;

  function show(duration = 0) {
    loading.value = true;
    if (timeoutId) clearTimeout(timeoutId);
    if (duration > 0) {
      timeoutId = setTimeout(() => {
        loading.value = false;
        timeoutId = null;
      }, duration);
    }
  }

  function hide() {
    loading.value = false;
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  }

  return { loading, show, hide };
});
