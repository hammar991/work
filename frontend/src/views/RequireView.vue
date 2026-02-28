<template>
  <n-card>
    <template #header>
      <n-text>需求列表</n-text>
    </template>

    <pre>{{ requireMeta }}</pre>
  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useClient } from '@/client/client'

const client = useClient()

const requireMeta = ref([])

requireMeta.value = await client.listRequire()
</script>
