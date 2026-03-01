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

  const oidcProvider = ref('Authentik')
  const token = ref(localStorage.getItem('token') || '')

  const setOidcProvider = (provider: string) => {
    oidcProvider.value = provider
  }

  const isAuthenticated = () => {
    return token.value != ''
  }

  const loginOIDC = async () => {
    window.location.href=`/api/auth/login/${oidcProvider.value}`
    // const response = await fetch('/api/auth/login/')
    // console.log(response)
  }

  const callbackOIDC = async (code: string, status: string) => {
    const response = await fetch(`/api/auth/callback/${oidcProvider.value}?code=${code}&state=${status}`)
    const data = await response.json()
    token.value = data.access_token
    localStorage.setItem('token', token.value)
    return data
  }

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

  const listTask = async () => {
    const response = await fetch('/api/task/list/')
    const data = await response.json()
    return data
  }


  const searchRequire = async (require: string) => {
    const response = await fetch(`/api/require/search/${require}`)
    const data = await response.json()
    return data
  }

  return { loginOIDC,submitRequire, listRequire, searchRequire, listTask, callbackOIDC, setOidcProvider, isAuthenticated }
})
