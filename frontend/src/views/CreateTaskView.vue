<template>
  <n-card>
    <template #header>
      <n-text>创建任务</n-text>
    </template>

    <n-form ref="formRef" :label-width="80" :model="taskMeta">
      <n-form-item label="任务名称" path="user.name">
        <n-input v-model:value="taskMeta.name" placeholder="输入任务" />
      </n-form-item>
      <n-form-item label="任务描述" path="user.content">
        <n-input v-model:value="taskMeta.content" placeholder="输入任务描述" type="textarea" />
      </n-form-item>
      <n-form-item>
        <n-button attr-type="button" @click="submitTask"> 提交 </n-button>
      </n-form-item>
    </n-form>

    <pre>{{ taskMeta }}</pre>
    <pre>{{ actualTaskMeta }}</pre>
  </n-card>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const taskMeta = reactive({
  name: '',
  content: '',
})

const actualTaskMeta = reactive({
  content: '',
})
const submitTask = async () => {
  actualTaskMeta.content = `# ${taskMeta.name}\n\n${taskMeta.content}`
}
</script>
