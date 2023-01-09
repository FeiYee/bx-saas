// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,

  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=500, initial-scale=1',
      title: 'BAIX',
      meta: [
        // <meta name="description" content="My amazing site">
        { name: 'description', content: 'BAIX.' }
      ],
    }
  },
  // vite: {
  //   css: {
  //     preprocessorOptions: {
  //       scss: {
  //         additionalData: '@use "@/assets/main.scss" as *;'
  //       }
  //     }
  //   }
  // }
})
