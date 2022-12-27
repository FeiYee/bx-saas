<template>
<section class="keyword">
  <div class="container">
    <!-- <h3 class="keyword-title">热词</h3> -->
    <div>
      <ul class="keyword-list">
        <!-- <li class="keyword-item">百令胶囊</li>
        <li class="keyword-item">虫草素</li>
        <li class="keyword-item">虫草素</li>
        <li class="keyword-item">虫草素</li>
        <li class="keyword-item">虫草素</li> -->
        <li class="keyword-item" v-for="keyword in keywords" :key="keyword.id" :class="{'is-preset': keyword.is_preset}"  :title="keyword.keyword" @click="onClick(keyword.keyword)">
          <el-tag
           :closable="keyword.is_preset ? false : true"
           :type="keyword.is_preset ? 'info' : 'success'"
           @close="onTagClose(keyword)">
           {{keyword.keyword}}
          </el-tag>
        </li>
      </ul>
    </div>
  </div>
</section>
</template>
<script setup>
import {defineProps, defineEmits} from 'vue'
import keywordService from '../services/keyword.js'
import context from '../core/context.js'

const props = defineProps({
  keywords: Array
})

const emit = defineEmits(['click', 'reload'])

const onClick = keyword => {
  context.setKeyword(keyword)
  emit('click', keyword)
}

const onTagClose = async (keyword) => {
  let keywordId = keyword.id
  if (keyword.keyword === context.getKeyword()) {
    context.setKeyword('')
  }
  let res = await keywordService.deleteKeyword(keywordId)
  emit('reload')
}
</script>
