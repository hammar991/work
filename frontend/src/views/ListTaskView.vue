<template>
  <n-card>
    <template #header>
      <n-text>任务列表</n-text>
    </template>

    <div v-for="item, index in taskList" :key="index">
      <n-card>
        <template #header>
          <n-text
            type="primary"
            @click="toProjectDetail(item.link)"
            >{{ item.title }}</n-text>
        </template>
        <n-text>{{ item.content }}</n-text>
        <br />
        <n-text>负责人: {{ item.owner }}</n-text>
      </n-card>
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useClient } from '@/client/client'
import type { TaskEntity } from '@/types/dto'
import { useRouter }  from 'vue-router'

const client = useClient()
const router = useRouter()
const taskList = ref<Array<TaskEntity>>([])

client.listTask().then(data => {
  taskList.value = data
})

const toProjectDetail = async (link: number) => {
  const res = await client.searchProjectBySerial(link)
  router.push({ path: `/project-detail/${res.title}` })
}
</script>
