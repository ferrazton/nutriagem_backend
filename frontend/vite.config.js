// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: 'localhost',
    fs: {
      strict: true
    }
  },
  optimizeDeps: {
    include: ['react', 'react-dom/client']
  }
})
