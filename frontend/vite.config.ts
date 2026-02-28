import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

import AutoImport from 'unplugin-auto-import/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'
// vite.config.ts

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      imports: [
        'vue',
        {
          'naive-ui': ['useDialog', 'useMessage', 'useNotification', 'useLoadingBar'],
        },
      ],
    }),
    Components({
      resolvers: [NaiveUiResolver()],
    }),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    // 代理配置
    proxy: {
      // 匹配所有以 '/api' 开头的请求
      '/api': {
        // 后端服务器的真实地址
        target: 'http://127.0.0.1:8000',

        // 开启代理：允许将请求转发到目标服务器
        changeOrigin: true,

        // (可选) 重写路径
        // 如果后端接口路径中没有 '/api' 前缀，可以用正则将其移除
        // 例如：前端请求 /api/users -> 后端接收 /users
        // rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
