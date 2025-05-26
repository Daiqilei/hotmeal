/****
 * @file            vite.config.js
 * @description     vite config file
 * @author          taichilei
 * @date            2025-04-23
 * @version         1.0.0
 */

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ command }) => ({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5000,
    open: true,
    proxy: {
      '/api': {
        target: 'https://127.0.0.1:5000',
        secure: false, // 仅调试 https 时使用，<=== 关键：忽略自签名证书
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'), // 保持路径一致
      },
    },
  },
}))
