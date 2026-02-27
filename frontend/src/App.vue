<script setup lang="ts">
import { RouterView } from 'vue-router'

import { darkTheme } from 'naive-ui'

import { zhCN, dateZhCN } from 'naive-ui'
</script>

<template>
  <n-config-provider :theme="darkTheme" :locale="zhCN" :date-locale="dateZhCN">
    <RouterView />
  </n-config-provider>
</template>
