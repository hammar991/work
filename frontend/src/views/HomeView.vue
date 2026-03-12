<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { routerMeta } from '@/router/index.ts'
</script>


<template>
  主页
  <n-button v-for="(i, index) in routerMeta" :key="index">
    <RouterLink :to="i.path">{{ i.name }}</RouterLink>
  </n-button>
</template>
