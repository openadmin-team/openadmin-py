import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  // Must match src/api/client.ts's dev fallback / .env.development.
  const apiBase = env.VITE_API_BASE || '/admin'
  const backendUrl = env.VITE_DEV_BACKEND_URL || 'http://localhost:8000'

  return {
    base: './',
    plugins: [vue()],
    server: {
      proxy: {
        [apiBase]: {
          target: backendUrl,
          changeOrigin: true,
        },
      },
    },
  }
})
