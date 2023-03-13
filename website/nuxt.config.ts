// https://nuxt.com/docs/api/configuration/nuxt-config

// import ElementPlus from 'unplugin-element-plus/vite'

export default defineNuxtConfig({
  ssr: false,

  app: {
    baseURL: '/',
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1.0',
      title: 'BAIX',
      meta: [
        // <meta name="description" content="My amazing site">
        { name: 'description', content: 'BAIX.' }
      ],
    },

  },
  devServer: {
    port: 8020
  },
  vite: {
    // plugins: [ElementPlus({})],
    // css: {
    //   preprocessorOptions: {
    //     scss: {
    //       additionalData: '@use "@/assets/main.scss" as *;'
    //     }
    //   }
    // }
  }
})
