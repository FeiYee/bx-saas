import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    port: 8000,
    hmr: true,
    usePolling: true,
    proxy: {
      '/api': {
        target: 'http://116.198.202.249:8080',
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '/api')
      },
      '/file': {
        target: 'http://116.198.202.249:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/file/, '')
      },
    }
  }
})
