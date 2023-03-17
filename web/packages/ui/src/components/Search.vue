<template>
<div class="search-container">
  <div class="container">
    <div class="search">
      <input v-model="keyword" type="search" name="search" id="search">
      <button @click="onSearch">搜索</button>
    </div>
    <section class="keyword">
        <!-- <h3 class="keyword-title">热词</h3> -->
        <div class="keyword-list-box">
          <ul class="keyword-list">
            <!-- <li class="keyword-item">百令胶囊</li> -->
            <li class="keyword-item"
              v-for="keyword in keywords"
              :key="keyword.id"
              :class="{'is-preset': keyword.is_preset}"
              :title="keyword.keyword"
              @click="onKeywordClick(keyword.keyword)">
              <el-tag
              :closable="keyword.is_preset ? false : true"
              :type="keyword.is_preset ? 'info' : 'success'"
              @close="onKeywordClose(keyword)">
                {{keyword.keyword}}
              </el-tag>
            </li>
          </ul>
        </div>
    </section>
  </div>
</div>
</template>
<script setup>
import { ref, reactive, watch } from 'vue'
import context from '../core/context.js'
import keywordService from '../services/keyword.js'

const props = defineProps({
  isSearchDone: Boolean
})

const keyword = ref('')
const keywords = ref([])

const emit = defineEmits(['search'])

watch(
  () => props.isSearchDone,
  value => {
    if (value) {
      getKeywords()
    }
  }
)

const onSearch = () => {
  if (!keyword.value) {
    // return
  }
  context.setKeyword(keyword.value)
  emit('search', keyword.value)
}

const onKeywordClick = keywordText => {
  keyword.value = keywordText
  context.setKeyword(keywordText)
  emit('search', keywordText)
}

const getKeywords = async () => {
  keywords.value = await keywordService.getUserKeywords(0)
}

const onKeywordClose = async (keyword) => {
  let keywordId = keyword.id
  if (keyword.keyword === context.getKeyword()) {
    context.setKeyword('')
  }
  await keywordService.deleteKeyword(keywordId)
  await getKeywords()
}

const init = async () => {
  await getKeywords()
  let keywordText = context.getKeyword()

  if (!keywordText && keywords.value.length) {
    keywordText = keywords.value[0].keyword
  }
  if (keywordText) {
    keyword.value = keywordText
    emit('search', keywordText)
  }
}

init()

</script>
