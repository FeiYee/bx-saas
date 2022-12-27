import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as echarts from 'echarts'

import App from './App.vue'
import router from './router'

import './assets/main.scss'

const app = createApp(App)


app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.config.globalProperties.$echarts = echarts

app.mount('#app')
