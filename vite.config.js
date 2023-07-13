import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    port: 8030,
    hmr: true,
    usePolling: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:9090',
        // target: 'http://43.154.134.150:9000',
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '/api')
      },
      '/file': {
        target: 'http://127.0.0.1:9090',
        // target: 'http://43.154.134.150:9000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/file/, '')
      },
    }
  }
})
