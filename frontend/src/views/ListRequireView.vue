<template>
  <n-card>
    <template #header>
      <n-text>需求列表</n-text>
    </template>

    <div v-for="require, index in requireList" :key="index">
      <n-card>
        <template #header>
          <n-text type="primary">{{ require.title }}</n-text>
        </template>
      <n-text>{{ require.content }}</n-text>
      </n-card>
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { useClient } from '@/client/client'
import { ref } from 'vue'
import type { RequireEntity } from '@/types/dto'
const client = useClient()

const requireList = ref<Array<RequireEntity>>([])

client.listRequire().then(data => {
  requireList.value = data
})
</script>
