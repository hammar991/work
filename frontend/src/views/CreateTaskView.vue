<template>
  <n-card>
    <template #header>
      <n-text>创建任务</n-text>
    </template>

    <n-form ref="formRef" :label-width="80" :model="taskMeta">
      <n-form-item label="任务名称" path="user.name">
        <n-input v-model:value="taskMeta.title" placeholder="输入任务" />
      </n-form-item>

      <n-form-item label="关联项目" path="user.name">
        <n-select
          v-model:value="taskMeta.link"
          filterable
          placeholder="选择关联项目"
          :options="options"
        />
      </n-form-item>

      <n-form-item label="任务描述" path="user.content">
        <n-input v-model:value="taskMeta.content" placeholder="输入任务描述" type="textarea" />
      </n-form-item>
      <n-form-item>
        <n-button attr-type="button" @click="submitTask"> 提交 </n-button>
      </n-form-item>
    </n-form>

    <pre>{{ taskMeta }}</pre>
  </n-card>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { CreateTaskDTO, UniOptionsEntity } from '@/types/dto'
import { useClient } from '@/client/client'

const client = useClient()


const taskMeta = reactive<CreateTaskDTO>({
  title: '',
  link: -1,
  content: ''
})


const options = ref<Array<UniOptionsEntity>>([])

client.listProject().then((data) => {
  options.value = []
  data.forEach((i) => {
    options.value.push({
      label: i.title,
      value: i.serial,
    })
  })
})


const submitTask = async () => {
  await client.createTask(taskMeta)
}
</script>
