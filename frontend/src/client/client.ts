import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

interface CreateRequireDTO {
  title: string
  content: string
}

const JSON_HEADER = {
  'Content-Type': 'application/json',
}

export const useClient = defineStore('client', () => {
  const submitRequire = async (payload: CreateRequireDTO) => {
    const response = await fetch('/api/require/create/', {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: JSON_HEADER,
    })
    const data = await response.json()
    return data
  }

  const listRequire = async () => {
    const response = await fetch('/api/require/list/')
    const data = await response.json()
    return data
  }

  const searchRequire = async (require: string) => {
    const response = await fetch(`/api/require/search/${require}`)
    const data = await response.json()
    return data
  }

  return { submitRequire, listRequire, searchRequire }
})
