<template>
  <div class="detail-container">
    <h1>详情页</h1>

    <!-- 加载状态 -->
    <n-skeleton v-if="loading" text :rows="10" />

    <!-- 错误提示 -->
    <n-alert v-else-if="error" type="error" title="加载失败" :content="error" />

    <!-- 需求信息 -->
    <div v-else-if="requireData" class="require-info">
      <h3>需求信息:</h3>
      <n-card class="require-card">
        <template #header>
          <n-text type="primary" strong>{{ requireData.title }}</n-text>
        </template>
        <n-text>{{ requireData.content }}</n-text>
        <div class="require-meta">
          <n-text>创建人: {{ requireData.create_by }}</n-text>
          <n-text>创建时间: {{ formatDate(requireData.create_time) }}</n-text>
        </div>
      </n-card>

      <!-- 项目列表 -->
      <div class="project-section">
        <n-divider title="关联项目" />
        <h3>项目信息</h3>
        <div v-if="projectList.length === 0" class="empty-state">
          <n-empty description="未找到关联项目" />
        </div>

        <!-- 项目卡片列表 -->
        <div v-else class="project-card-list">
          <n-card
            v-for="project in paginatedProjects"
            :key="project.serial"
            class="project-card"
            hoverable
          >
            <template #header>
              <div class="project-card-header">
                <n-text type="primary" strong>{{ project.title }}</n-text>
                <n-tag size="small">ID: {{ project.serial }}</n-tag>
              </div>
            </template>

            <div class="project-card-content">
              <n-text>{{ project.content }}</n-text>
              <div class="project-meta">
                <n-text>创建人: {{ project.create_by }}</n-text>
                <n-text>创建时间: {{ formatDate(project.create_time) }}</n-text>
              </div>

              <!-- 任务展开按钮 -->
              <div class="task-toggle">
                <n-button
                  type="primary"
                  text
                  @click="toggleTaskPanel(project.serial)"
                >
                  {{ showTaskPanel[project.serial] ? '收起任务' : '展开任务' }}
                </n-button>
              </div>

              <!-- 任务表格 -->
              <div v-if="showTaskPanel[project.serial]" class="task-panel">
                <n-skeleton v-if="loadingTasks[project.serial]" text :rows="3" />
                <div v-else class="task-table-wrapper">
                  <n-data-table
                    :columns="taskColumns"
                    :data="getPaginatedTasks(project.serial)"
                    :pagination="false"
                    :bordered="false"
                  />
                  <!-- 任务翻页 -->
                  <div class="task-pagination">
                    <n-pagination
                      v-model:page="taskPageMap[project.serial]"
                      :page-count="getTaskPageCount(project.serial)"
                      :page-slot="5"
                      @update:page="(page: number) => handleTaskPageChange(project.serial, page)"
                    />
                  </div>
                </div>
              </div>
            </div>
          </n-card>
        </div>

        <!-- 项目翻页 -->
        <div v-if="projectList.length > 0" class="project-pagination">
          <n-pagination
            v-model:page="projectPage"
            :page-count="projectPageCount"
            :page-slot="5"
            @update:page="handleProjectPageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { useClient } from '@/client/client'
import { useRoute } from 'vue-router'
import { useMessage, NPopover, NButton, NSelect, NTag, NEmpty } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'

import { TaskStatus } from '@/types/dto'
import type { TaskStatusType } from '@/types/dto'
import type { RequireEntity, ProjectEntity, TaskEntity, UpdateTaskStatusDTO } from '@/types/dto'
import { MdPreview } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
const route = useRoute()
const client = useClient()
const message = useMessage()

const loading = ref(true)
const error = ref('')
const requireData = ref<RequireEntity | null>(null)
const projectList = ref<ProjectEntity[]>([])
const projectTaskMap = ref<Record<number, TaskEntity[]>>({})
const loadingTasks = ref<Record<number, boolean>>({})
const showTaskPanel = ref<Record<number, boolean>>({})

const projectPage = ref(1)
const projectPageSize = 5
const taskPageMap = ref<Record<number, number>>({})
const taskPageSize = 5
const updatingTask = ref<number | null>(null)

const projectPageCount = computed(() => Math.ceil(projectList.value.length / projectPageSize))

const paginatedProjects = computed(() => {
  const start = (projectPage.value - 1) * projectPageSize
  const end = start + projectPageSize
  return projectList.value.slice(start, end)
})

const getTaskPageCount = (projectSerial: number) => {
  const tasks = projectTaskMap.value[projectSerial] || []
  return Math.ceil(tasks.length / taskPageSize) || 1
}

const getPaginatedTasks = (projectSerial: number) => {
  const tasks = projectTaskMap.value[projectSerial] || []
  const page = taskPageMap.value[projectSerial] || 1
  const start = (page - 1) * taskPageSize
  const end = start + taskPageSize
  return tasks.slice(start, end)
}

const handleProjectPageChange = (page: number) => {
  projectPage.value = page
  // 重置所有任务面板状态
  showTaskPanel.value = {}
}

const handleTaskPageChange = (projectSerial: number, page: number) => {
  taskPageMap.value[projectSerial] = page
}

const toggleTaskPanel = (projectSerial: number) => {
  showTaskPanel.value[projectSerial] = !showTaskPanel.value[projectSerial]
  if (showTaskPanel.value[projectSerial] && !projectTaskMap.value[projectSerial]) {
    loadProjectTasks(projectSerial)
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const getStatusType = (status: string) => {
  const statusMap: Record<string, 'info' | 'warning' | 'success' | 'error'> = {
    planned: 'info',
    progress: 'warning',
    completed: 'success',
    halted: 'error'
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status: string) => {
  // 直接返回英文状态
  return status
}

const updateTaskStatus = async (task: TaskEntity, newStatus: TaskStatusType) => {
  if (updatingTask.value === task.serial) return

  updatingTask.value = task.serial
  try {
    const payload: UpdateTaskStatusDTO = {
      serial: task.serial,
      status: newStatus
    }
    await client.updateTaskStatus(payload)

    if (projectTaskMap.value[task.link]) {
      const taskList = projectTaskMap.value[task.link]
      const taskIndex = taskList.findIndex(t => t.serial === task.serial)
      if (taskIndex !== -1) {
        taskList[taskIndex] = {
          ...task,
          current_status: newStatus
        }
      }
    }

    message.success('任务状态更新成功')
  } catch (err) {
    console.error('更新任务状态失败:', err)
    message.error('任务状态更新失败')
  } finally {
    updatingTask.value = null
  }
}

const createTaskColumns = (): DataTableColumns<TaskEntity> => [
  {
    title: 'ID',
    key: 'serial',
    width: 80
  },
  {
    title: '任务名称',
    key: 'title',
    width: 80
  },
  {
    title: "任务描述",
    key: 'content',
    width: 250,
    render: (row: TaskEntity) => {
      return h(MdPreview, {
        modelValue: row.content,
        theme: "dark",
        previewOnly: true
      })
    }
  },
  {
    title: '负责人',
    key: 'owner',
    width: 100
  },
  {
    title: '状态',
    key: 'current_status',
    width: 120,
    render: (row: TaskEntity) => {
      return h(NTag, {
        type: getStatusType(row.current_status),
        size: 'small',
        style: {
          padding: '0 8px',
          fontSize: '12px',
          borderRadius: '4px'
        }
      }, {
        default: () => getStatusLabel(row.current_status)
      })
    }
  },
  {
    title: '操作',
    key: 'action',
    width: 120,
    render: (row: TaskEntity) => {
      return h('div', {}, [
        h(
          NPopover,
          { trigger: 'click' },
          {
            trigger: () => h(NButton, {
              size: 'small',
              type: 'primary',
              loading: updatingTask.value === row.serial,
              style: {
                fontSize: '12px',
                padding: '4px 8px'
              }
            }, { default: () => '更改状态' }),
            default: () => h(
              NSelect,
              {
                value: row.current_status,
                options: [
                  { label: 'planned', value: TaskStatus.PLANNED },
                  { label: 'progress', value: TaskStatus.PROGRESS },
                  { label: 'completed', value: TaskStatus.COMPLETED },
                  { label: 'halted', value: TaskStatus.HALTED }
                ],
                onUpdateValue: (value: TaskStatusType) => updateTaskStatus(row, value),
                style: 'width: 120px; font-size: 12px;'
              }
            )
          }
        )
      ])
    }
  }
]

const taskColumns = createTaskColumns()

const loadData = async () => {
  loading.value = true
  error.value = ''

  try {
    const id = Number(route.query.id)
    if (!id) {
      error.value = '无效的ID参数'
      return
    }

    const type = route.query.type as 'project' | 'require' | 'task' || 'require'
    const detailResult = await client.searchDetailBySerial(id, type)

    projectList.value = detailResult.project || []

    // 处理需求数据
    if (detailResult.require) {
      requireData.value = detailResult.require
    }

    // 处理任务数据
    if (detailResult.task) {
      for (let i = 0; i < projectList.value.length; i++) {
        const project = projectList.value[i]
        projectTaskMap.value[project.serial] = detailResult.task[i] || []
      }
    }
  } catch (err) {
    error.value = '数据加载失败'
    console.error('加载详情失败:', err)
  } finally {
    loading.value = false
  }
}

const loadProjectTasks = async (projectSerial: number) => {
  loadingTasks.value[projectSerial] = true
  taskPageMap.value[projectSerial] = 1
  try {
    const tasks = await client.searchTasktByLink(projectSerial)
    projectTaskMap.value[projectSerial] = Array.isArray(tasks) ? tasks : []
  } catch (err) {
    console.error(`加载项目任务失败:`, err)
    projectTaskMap.value[projectSerial] = []
  } finally {
    loadingTasks.value[projectSerial] = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.require-card {
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.require-meta {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
}

.project-section {
  margin-top: 5px;
}

.project-card-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 10px;
}

.project-card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  overflow: hidden;
}

.project-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-card-content {
  padding: 15px 0;
}

.project-meta {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
}

.task-toggle {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.task-panel {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #121213;
}

.task-table-wrapper {
  margin-top: 15px;
  padding: 15px;
  background-color: #141414;
  border-radius: 6px;
}

.task-pagination {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

.project-pagination {
  margin-top: 30px;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  padding: 15px;
  background-color: #121213;
  border-radius: 6px;
}

.empty-state {
  padding: 40px 0;
  text-align: center;
  background-color: #151616;
  border-radius: 8px;
  margin: 10px 0;
}

.empty-state.small {
  padding: 20px 0;
  border-radius: 8px;
  margin: 10px 0;
}

h1 {
  text-align: center;
  margin-bottom: 10px;
  color: #333;
}

h3 {
  margin-bottom: 15px;
  color: #333;
}
</style>
