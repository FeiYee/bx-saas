<template>
  <div class="app">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { provide } from 'vue'
import * as echarts from 'echarts'

provide('echarts', echarts)
</script>
