<template>
  <nav class="nav">
    <div class="container">
      <!-- <div class="search">
        <input v-model="keyword" type="search" name="search" id="search">
        <button @click="onClick">搜索</button>
      </div> -->
      <menu class="menu">
        <ul class="menu-list">
          <li class="menu-item">
            <RouterLink to="/">首页</RouterLink>
          </li>
          <li class="menu-item">
            <RouterLink to="/doc">文档管理</RouterLink>
          </li>
          <li class="menu-item">
            <RouterLink to="/download">数据下载</RouterLink>
          </li>
          <li class="menu-item">
            <RouterLink to="/paper">资料管理</RouterLink>
          </li>
        </ul>
      </menu>
    </div>
  </nav>
</template>
<script setup>
// import { ref, defineProps, defineEmits, computed } from 'vue'
import { RouterLink } from 'vue-router'
// import context from '../core/context.js'

// const props = defineProps({
//   modelValue: String,
// })

// const emit = defineEmits(['search', 'update:modelValue'])

// const keyword = computed({
//   get: () => props.modelValue,
//   set: (value) => {
//     emit('update:modelValue', value)
//   }
// })


// const onClick = () => {
//   if (!keyword.value) {
//     return
//   }
//   context.setKeyword(keyword.value)
//   emit('search', keyword.value)
// }


</script>
