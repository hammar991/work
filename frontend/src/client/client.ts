import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

interface CreateRequireDTO {
  title: string
  content: string
}

interface CreateProjectDTO {
  title: string
  link: number
  content: string
}

interface RequireEntity {
  content: string
  create_by: string
  create_time: string
  serial: number
  title: string
}


interface UniOptionsEntity {
  label: number | string
  value: number | string
}

export const useClient = defineStore('client', () => {

  const getHeaders = () => {
    return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getLocalToken()}`,
  }
  }

  const oidcProvider = ref('Authentik')

  const setOidcProvider = (provider: string) => {
    oidcProvider.value = provider
  }

  const getLocalToken = () => {
    return localStorage.getItem('token') || ""
  }

  const setLocalToken = (token: string) => {
    localStorage.setItem('token', token)
  }

  const isAuthenticated = () => {
    const resp = "" != getLocalToken()
    console.log(resp, getLocalToken())
    return resp
  }

  const loginOIDC = async () => {
    window.location.href=`/api/auth/login/${oidcProvider.value}`
  }

  const callbackOIDC = async (code: string, status: string) => {
    const response = await fetch(`/api/auth/callback/${oidcProvider.value}?code=${code}&state=${status}`)
    const data = await response.json()
    setLocalToken(data.access_token)
    return data
  }

  const submitRequire = async (payload: CreateRequireDTO) => {
    const response = await fetch('/api/require/create/', {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: getHeaders(),
    })
    const data = await response.json()
    return data
  }

  const listRequire = async () => {
    const response = await fetch('/api/require/list/')
    const data = await response.json()
    return data as Array<RequireEntity>
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

  const createProject = async (payload: CreateProjectDTO) => {
    const response = await fetch('/api/project/create/', {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: getHeaders(),
    })
    const data = await response.json()
    return data
  }

  return { loginOIDC,submitRequire, listRequire, searchRequire, listTask, callbackOIDC, setOidcProvider, isAuthenticated, createProject }
})

export type { RequireEntity, UniOptionsEntity }
