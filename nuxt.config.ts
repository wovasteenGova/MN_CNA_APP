// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxt/ui'],
  ui: {
    primary: 'teal',
    gray: 'slate'
  },
  ssr: true, // Enable SSR for proper routing
  app: {
    head: {
      title: 'MN CNA APP',
      meta: [
        { name: 'description', content: 'Minnesota CNA Study App - Master your Certified Nursing Assistant exam with confidence' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' },
        { name: 'format-detection', content: 'telephone=no' }
      ]
    }
  }
})
