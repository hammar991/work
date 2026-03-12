import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter }  from 'vue-router'

import type {
  CreateRequireDTO,
  CreateProjectDTO,
  CreateTaskDTO,
  RequireEntity,
  ProjectEntity,
  TaskEntity,
  UpdateTaskStatusDTO
 } from '@/types/dto'


export const useClient = defineStore('client', () => {
  const router = useRouter()

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

  // token清除
  const removeLocalToken = () => {
    localStorage.removeItem('token')
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

  // 通用请求处理函数,处理401错误
  const fetchWithAuth = async (url: string, option: RequestInit = {}) => {
    const headers = {
      'Content-Type': 'application/json',
      ...option.headers,
      'Authorization': `Bearer ${getLocalToken()}`,
    }
    const response = await fetch(url, {
      ...option,
      headers,
    })

    if (response.status == 401){
      removeLocalToken()
      router.push({path:'/login'})
      throw new Error('401 token已过期,请重新登录!')
    }
    return response
  }

  const submitRequire = async (payload: CreateRequireDTO) => {
    const response = await fetchWithAuth('/api/require/create/', {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: getHeaders(),
    })
    const data = await response.json()
    return data
  }

  const listRequire = async () => {
    const response = await fetchWithAuth('/api/require/list/')
    const data = await response.json()
    return data as Array<RequireEntity>
  }

  const listTask = async () => {
    const response = await fetchWithAuth('/api/task/list/')
    const data = await response.json()
    return data as Array<TaskEntity>
  }

  const listProject = async () => {
    const response = await fetchWithAuth('/api/project/list/')
    const data = await response.json()
    return data as Array<ProjectEntity>
  }

  const searchDetailBySerial = async (serial: number, type: string) => {
    const url = `/api/detail/${serial}?type_str=${type}`

    const response = await fetchWithAuth(url, {
      method: 'GET',
      headers: getHeaders(),
    })

    const data = await response.json()
    return data
  }

  const searchProjectByLink = async (link: number) => {
    const response = await fetchWithAuth(`/api/project/search/link/${link}/`)
    const data = await response.json()
    return data
  }

  const searchProjectByTitle = async (project: string) => {
    const response = await fetchWithAuth(`/api/project/search/${project}/`)
    const data = await response.json()
    return data as Array<ProjectEntity>
  }

  const searchRequireBySerial = async (serial: number) => {
    const response = await fetchWithAuth(`/api/require/search/serial/${serial}/`)
    const data = await response.json()
    return data as RequireEntity
  }

  const searchRequireByTitle = async (require: string) => {
    const response = await fetchWithAuth(`/api/require/search/${require}/`)
    const data = await response.json()
    return data as Array<RequireEntity>
  }

  const searchTasktByLink = async (link: number) => {
    const response = await fetchWithAuth(`/api/task/search/link/${link}/`)
    const data = await response.json()
    return data as Array<TaskEntity>
  }

  const searchTaskByTitle = async (task: string) => {
    const response = await fetchWithAuth(`/api/task/search/${task}/`)
    const data = await response.json()
    return data as Array<TaskEntity>
  }

  const updateTaskStatus = async (payload: UpdateTaskStatusDTO) => {
    const response = await fetchWithAuth(`/api/task/update/status/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(payload),
    })
    const data = await response.json()
    return data
  }

  const createProject = async (payload: CreateProjectDTO) => {
      const response = await fetchWithAuth('/api/project/create/', {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: getHeaders(),
      })
      const data = await response.json()
      return data
    }

  const createTask = async (payload: CreateTaskDTO) => {
      const response = await fetchWithAuth('/api/task/create/', {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: getHeaders(),
      })
      const data = await response.json()
      console.log("data:", data)
      return data
    }

  return {
    loginOIDC,
    submitRequire,
    listRequire,
    listTask,
    listProject,
    callbackOIDC,
    setOidcProvider,
    isAuthenticated,
    searchDetailBySerial,
    searchProjectByLink,
    searchProjectByTitle,
    searchRequireBySerial,
    searchRequireByTitle,
    searchTasktByLink,
    searchTaskByTitle,
    updateTaskStatus,
    createProject,
    createTask
  }
})
