<template>
  <n-card>
    <template #header>
      <n-text>创建项目</n-text>
    </template>

    <n-form ref="formRef" :label-width="80" :model="projectMeta">
      <n-form-item label="项目名称" path="user.name">
        <n-input v-model:value="projectMeta.name" placeholder="输入项目" />
      </n-form-item>
      <n-form-item label="项目描述" path="user.content">
        <n-input v-model:value="projectMeta.content" placeholder="输入项目描述" type="textarea" />
      </n-form-item>
      <n-form-item>
        <n-button attr-type="button" @click="submitProject"> 提交 </n-button>
      </n-form-item>
    </n-form>

    <pre>{{ projectMeta }}</pre>
    <pre>{{ actualProjectMeta }}</pre>
  </n-card>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const projectMeta = reactive({
  name: '',
  content: '',
})

const actualProjectMeta = reactive({
  content: '',
})
const submitProject = async () => {
  actualProjectMeta.content = `# ${projectMeta.name}\n\n${projectMeta.content}`
}
</script>
