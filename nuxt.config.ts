// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxt/ui'],
  ui: {
    primary: 'teal',
    gray: 'slate'
  },
  nitro: {
    prerender: {
      routes: ['/']
    }
  },
  ssr: false, // Disable SSR for static generation
  target: 'static' // Enable static generation
})
