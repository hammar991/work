<template>
  <n-card>
    <template #header>
      <n-text>项目列表</n-text>
    </template>

    <div v-for="item, index in projectList" :key="index">
      <n-card>
        <template #header>
          <n-text type="primary">{{ item.title }}</n-text>
        </template>
        <n-text>{{ item.content }}</n-text>
      </n-card>
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useClient } from '@/client/client'
import type { ProjectEntity } from '@/types/dto'

const client = useClient()
const projectList = ref<Array<ProjectEntity>>([])

// projectList.value = await client.listProject().then(data => data)

client.listProject().then(data => {
  projectList.value = data
})
</script>
