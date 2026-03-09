<template>
  <div class="project-detail-container">
    <h1>项目详情搜索</h1>
    <n-text class="search-keyword">搜索关键词: {{ keyword }}</n-text>

    <!-- 加载状态 -->
    <n-skeleton v-if="loading" text :rows="15" />

    <!-- 错误提示 -->
    <n-alert v-else-if="error" type="error" title="加载失败" :content="error" />

    <!-- 项目列表 -->
    <div v-else class="project-list">
      <div v-if="projectList.length === 0" class="empty-state">
        <n-empty description="未找到相关项目" />
      </div>

      <n-card
        v-for="project, index in projectList"
        :key="index"
        class="project-card"
        hoverable
      >
        <template #header>
          <div class="project-header">
            <n-text type="primary" strong>{{ project.title }}</n-text>
            <n-text class="project-id">ID: {{ project.serial }}</n-text>
          </div>
        </template>

        <!-- 项目详情 -->
        <div class="project-info">
          <n-text>{{ project.content }}</n-text>
          <div class="project-meta">
            <n-text>创建人: {{ project.create_by }}</n-text>
            <n-text>创建时间: {{ formatDate(project.create_time) }}</n-text>
          </div>
        </div>

        <!-- 关联需求 -->
        <div class="related-section">
          <n-divider title="关联需求" />
          <n-skeleton v-if="loadingRequires[project.serial]" text :rows="3" />
          <div v-else-if="projectRequireMap[project.serial]" class="require-info">
            <n-card class="require-card">
              <template #header>
                <n-text type="success">{{ projectRequireMap[project.serial]?.title || '' }}</n-text>
              </template>
              <n-text>{{ projectRequireMap[project.serial]?.content || '' }}</n-text>
            </n-card>
          </div>
          <div v-else class="empty-state small">
            <n-empty description="未找到关联需求" />
          </div>
        </div>

        <!-- 关联任务 -->
        <div class="related-section">
          <n-divider title="关联任务" />
          <n-skeleton v-if="loadingTasks[project.serial]" text :rows="5" />
          <div v-else-if="projectTaskMap[project.serial]?.length" class="task-list">
            <n-card
              v-for="task in projectTaskMap[project.serial]"
              :key="task.serial"
              class="task-card"
            >
              <template #header>
                <div class="task-header">
                  <n-text type="warning">{{ task.title }}</n-text>

                  <NSpace>
                    <n-tag :type="getStatusType(task.current_status)">
                      {{ task.current_status }}
                    </n-tag>
                    <NPopover>
                      <template #trigger>
                        <NButton
                          size="small"
                          type="primary"
                          :loading="updatingTask === task.serial"
                        >
                          更改状态
                        </NButton>
                      </template>
                      <NSelect
                        :value="task.current_status"
                        :options="taskStatusOptions"
                        @update:value="(value) => updateTaskStatus(task, value)"
                        placeholder="选择状态"
                      />
                    </NPopover>
                  </NSpace>


                </div>
              </template>
              <n-text>{{ task.content }}</n-text>
              <div class="task-meta">
                <n-text >负责人: {{ task.owner }}</n-text>
              </div>
            </n-card>
          </div>
          <div v-else class="empty-state small">
            <n-empty description="未找到关联任务" />
          </div>
        </div>
      </n-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useClient } from '@/client/client'
import { useRoute } from 'vue-router'
import { NEmpty, NSkeleton, NAlert, NDivider, NTag, NSelect, NSpace, NButton, NPopover,useMessage } from 'naive-ui'

import { TaskStatus} from '@/types/dto'
import type { TagProps } from 'naive-ui'
import type { RequireEntity, ProjectEntity, TaskEntity,TaskStatusType, UpdateTaskStatusDTO } from '@/types/dto'

const route = useRoute()
const keyword = route.params.keyword as string

const client = useClient()
const message = useMessage()
const projectList = ref<Array<ProjectEntity>>([])
const projectRequireMap = ref<Record<number, RequireEntity>>({})
const projectTaskMap = ref<Record<number, Array<TaskEntity>>>({})
const loading = ref(true)
const loadingRequires = ref<Record<number, boolean>>({})    // 加载状态
const loadingTasks = ref<Record<number, boolean>>({})
const error = ref('')
const updateTaskStatusPayload = ref<UpdateTaskStatusDTO>()

// 任务状态选项
const taskStatusOptions = [
  { label: TaskStatus.PLANNED, value: TaskStatus.PLANNED },
  { label: TaskStatus.PROGRESS, value: TaskStatus.PROGRESS },
  { label: TaskStatus.COMPLETED, value: TaskStatus.COMPLETED },
  { label: TaskStatus.HALTED, value: TaskStatus.HALTED }
]

// 正在更新的任务ID
const updatingTask = ref<number | null>(null)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 获取任务状态标签类型
const getStatusType = (status: string): TagProps['type'] => {
  const statusMap: Record<string, TagProps['type']> = {
    planned: 'info',
    progress: 'warning',
    completed: 'success',
    halted: 'error'
  }
  return statusMap[status] || 'default'
}



// 更新任务状态
const updateTaskStatus = async (task: TaskEntity, newStatus: TaskStatusType) => {
  if (updatingTask.value === task.serial) return    // 避免重复点击

  updatingTask.value = task.serial
  try {
    updateTaskStatusPayload.value = {
      serial: task.serial,
      status: newStatus
    }
    await client.updateTaskStatus(updateTaskStatusPayload.value!)

    // 更新本地任务状态
    if (projectTaskMap.value[task.link] && projectTaskMap.value[task.link] !== undefined) {
      const taskList = projectTaskMap.value[task.link]!
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

// 加载项目数据
const loadProjects = async () => {
  loading.value = true
  error.value = ''

  try {
    const projects = await client.searchProjectByTitle(keyword)
    projectList.value = projects

    // 为每个项目加载关联的需求和任务
    for (const project of projects) {
      loadProjectRelatedData(project)
    }
  } catch (err) {
    error.value = '项目数据加载失败'
    console.error('加载项目失败:', err)
  } finally {
    loading.value = false
  }
}

// 加载项目关联数据
const loadProjectRelatedData = async (project: ProjectEntity) => {
  // 加载关联需求
  loadingRequires.value[project.serial] = true      // 加载中
  try {
    const require = await client.searchRequireBySerial(project.link)
    if (require) {
      projectRequireMap.value[project.serial] = require
    }
  } catch (err) {
    console.error(`加载项目 ${project.title} 的需求失败:`, err)
  } finally {
    loadingRequires.value[project.serial] = false      // 加载完成
  }

  // 加载关联任务
  loadingTasks.value[project.serial] = true      // 加载中
  try {
    const tasks = await client.searchTasktByLink(project.serial)
    if (tasks) {
      projectTaskMap.value[project.serial] = Array.isArray(tasks) ? tasks : [tasks]
    }
  } catch (err) {
    console.error(`加载项目 ${project.title} 的任务失败:`, err)
  } finally {
    loadingTasks.value[project.serial] = false
  }
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.project-detail-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.search-keyword {
  display: block;
  margin-bottom: 20px;
  font-size: 16px;
  color: #666;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.project-card {
  padding: 20px;
  border-radius: 8px;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.project-id {
  font-size: 14px;
  color: #999;
}

.project-info {
  margin-bottom: 20px;
}

.project-meta {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
  display: flex;
  justify-content: space-between;
}

.related-section {
  margin-top: 20px;
}

.require-card {
  margin-top: 10px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.task-card {
  padding: 15px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.task-meta {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
  display: flex;
  justify-content: space-between;
}

.empty-state {
  padding: 40px 0;
  text-align: center;
}

.empty-state.small {
  padding: 20px 0;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}
</style>
