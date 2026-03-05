<template>
  <n-card>
    <template #header>
      <n-text>项目列表</n-text>
    </template>

    <div v-for="item, index in projectList" :key="index">
      <n-card>
        <template #header>
          <n-text
            type="primary"
            @click="goToDetail(item.title)"
            >{{ item.title }}</n-text>
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
import { useRouter } from 'vue-router'

const router = useRouter()
const client = useClient()
const projectList = ref<Array<ProjectEntity>>([])

// projectList.value = await client.listProject().then(data => data)

client.listProject().then(data => {
  projectList.value = data
})


const goToDetail = (keyword: string) => {
  console.log(keyword)
  router.push({ name: '项目详情', params: { keyword } })
}
</script>
