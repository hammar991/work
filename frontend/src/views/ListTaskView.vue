<template>
  <n-card>
    <template #header>
      <n-text>任务列表</n-text>
    </template>

    <div v-for="item, index in task" :key="index">
      {{ item }}
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useClient } from '@/client/client'

const client = useClient()
const task = ref([1, 2, 3])

task.value = await client.listTask()

</script>
