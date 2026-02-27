import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useClient = defineStore('client', () => {
  const submitRequire = async (require: string) => {
    const response = await fetch('/api/require', {
      method: 'POST',
      body: require,
    })
    const data = await response.json()
    return data
  }

  return { submitRequire }
})
