import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as null | { id: number; tipo: string; email: string; username: string },
  }),
  actions: {
    setUser(user: any) {
      this.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    loadUser() {
      const u = localStorage.getItem('user')
      if (u) this.user = JSON.parse(u)
    },
    logout() {
      this.user = null
      localStorage.removeItem('user')
    }
  },
})
