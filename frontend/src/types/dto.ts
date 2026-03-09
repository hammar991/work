
// 任务状态 枚举
const TaskStatus ={
  PLANNED :'planned',
  PROGRESS : 'progress',
  COMPLETED : 'completed',
  HALTED : 'halted'
}

type TaskStatusType = typeof TaskStatus[keyof typeof TaskStatus]


interface CreateRequireDTO {
  title: string
  content: string
}

interface CreateProjectDTO {
  title: string
  content: string
  link: number
}

interface CreateTaskDTO {
  title: string
  content: string
  link:number
}

interface UniOptionsEntity {
  label: number | string
  value: number | string
}

interface UpdateTaskStatusDTO {
  serial: number
  status: TaskStatusType
}

interface UserEntity {
  serial: number
  alias: string
  unique_id: number
  oidc_id: string
}

interface RequireEntity {
  serial: number
  title: string
  content: string
  create_by: string
  create_time: string
}

interface ProjectEntity {
  serial: number
  link:number
  title: string
  content: string
  create_by: string
  create_time: string
}

interface TaskEntity {
  serial: number
  link: number
  owner :string
  title: string
  content: string
  create_by: string
  create_time: string
  start_time: string
  end_time: string
  current_status: TaskStatusType
}


export {
  TaskStatus
}

export type {
  TaskStatusType,
  CreateRequireDTO,
  CreateProjectDTO,
  CreateTaskDTO,
  UniOptionsEntity,
  UpdateTaskStatusDTO,
  UserEntity,
  RequireEntity,
  ProjectEntity,
  TaskEntity
}
