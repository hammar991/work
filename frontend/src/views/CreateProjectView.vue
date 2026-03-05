<template>
  <n-card>
    <template #header>
      <n-text>创建项目</n-text>
    </template>

    <n-form ref="formRef" :label-width="80" :model="projectMeta">
      <n-form-item label="项目名称" path="user.name">
        <n-input v-model:value="projectMeta.title" placeholder="输入项目" />
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
import { useClient } from '@/client/client'
import { type UniOptionsEntity } from '@/types/dto'
import { useMessage } from 'naive-ui'
import { useRouter }  from 'vue-router'

const client = useClient()
const message = useMessage()
const router = useRouter()

const projectMeta = reactive({
  title: '',
  link: -1,
  content: '',
})


const options = ref<Array<UniOptionsEntity>>([])

client.listRequire().then((res) => {
  options.value = []
  res.forEach((i) => {
    options.value.push({
      label: i.title,
      value: i.serial,
    })
  })
})

const submitProject = async () => {
  try{

    const res = await client.createProject(projectMeta)
    if (res) {
      message.success("创建项目成功")
      router.push({ path: '/' })
    }
    else {
      message.error("创建项目失败")
    }
  } catch (err) {
    console.error("创建项目失败:", err)
  }
}

</script>
