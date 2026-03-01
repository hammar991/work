<template>
  <n-card>
    <template #header>
      <n-text>登录</n-text>
    </template>

    <n-button @click="loginOIDC">使用OIDC登录</n-button>
  </n-card>
</template>

<script setup lang="ts">
import { useClient } from '@/client/client'

const client = useClient()
import { useRoute, useRouter } from 'vue-router';


const route = useRoute();
const router = useRouter();
const code = route.query.code as string || ''
const state = route.query.state as string || ''

console.log([code, state])

if (code != '' && state != '') {
  client.callbackOIDC(code, state).then(data => {
    console.log(data)
  })
}

if (client.isAuthenticated()) {
  router.push({ path: '/' })
}

const loginOIDC = async () => {
  await client.setOidcProvider('Authentik')
  await client.loginOIDC()
}
</script>
