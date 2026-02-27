<template>
  <n-card>
    <template #header>
      <n-text>创建项目</n-text>
    </template>

    <n-form ref="formRef" :label-width="80" :model="projectMeta">
      <n-form-item label="项目名称" path="user.name">
        <n-input v-model:value="projectMeta.name" placeholder="输入项目" />
      </n-form-item>

      <n-form-item label="关联需求" path="user.name">
        <n-select
          v-model:value="projectMeta.link"
          filterable
          placeholder="选择关联需求"
          :options="options"
        />
      </n-form-item>

      <n-form-item label="项目描述" path="user.content">
        <n-input v-model:value="projectMeta.content" placeholder="输入项目描述" type="textarea" />
      </n-form-item>
      <n-form-item>
        <n-button attr-type="button" @click="submitProject"> 提交 </n-button>
      </n-form-item>
    </n-form>

    <pre>{{ projectMeta }}</pre>
  </n-card>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'

const projectMeta = reactive({
  name: '',
  link: -1,
  content: '',
})

const options = ref([
  {
    label: '需求1',
    value: 0,
  },
  {
    label: '需求2',
    value: 1,
  },
])

const submitProject = async () => {}
</script>
