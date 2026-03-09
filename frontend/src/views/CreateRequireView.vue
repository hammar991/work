<template>
  <n-card>
    <template #header>
      <n-text>创建需求</n-text>
    </template>

    <n-form ref="formRef" :label-width="80" :model="requireMeta">
      <n-form-item label="需求名称" path="user.name">
        <n-input v-model:value="requireMeta.title" placeholder="输入名称" />
      </n-form-item>
      <n-form-item label="需求描述" path="user.content">
        <n-input v-model:value="requireMeta.content" placeholder="输入需求描述" type="textarea" />
      </n-form-item>
      <n-form-item>
        <n-button attr-type="button" @click="submitRequire"> 提交 </n-button>
      </n-form-item>
    </n-form>

    <pre>{{ requireMeta }}</pre>
  </n-card>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

import { useClient } from '@/client/client'
import type { CreateRequireDTO } from '@/types/dto'
import { useMessage } from 'naive-ui'
import { useRouter }  from 'vue-router'

const client = useClient()
const message = useMessage()
const router = useRouter()

const requireMeta = reactive<CreateRequireDTO>({
  title: '',
  content: '',
})

const submitRequire = async () => {
  try{
    const res = await client.submitRequire(requireMeta)
    console.log('111',res)
    if (res) {
      message.success("创建项目成功")
      router.push({ path: '/' })
    }
    else {
      message.error("创建项目失败")
    }
  } catch (err) {
    console.error("创建需求失败:", err)
  }
}
</script>
