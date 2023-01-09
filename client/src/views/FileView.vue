<template>
  <Search @search="onSearch" :isSearchDone="isSearchDone" />
  <Nav />
  <main class="file content">
    <div class="container">
      <section class="content-primary">
        <h3 class="content-title">论文文档</h3>

        <div class="content-main">

          <ul class="file-list">
            <li class="file-item" v-for="item in fileList" :key="item.id">
              <div class="file-check">
                <input type="checkbox" name="" id="">
              </div>
              <div class="file-name" :class="{summary: item.type==1}">{{ item.name }}</div>
            </li>
            <li class="file-item">
              <div class="file-check">
                <input type="checkbox" name="" id="">
              </div>
              <div class="file-name summary">dfsfsdf</div>
            </li>
          </ul>

        </div>

        <div class="file-info">
          <div class="file-operate">
            <div class="operate-item">
              <input type="checkbox" name="selectAll" id="selectAll">
              <label for="selectAll" @click="onSelectAll">全选</label>
            </div>
            <div class="operate-item">
              <ElIcon><Delete /></ElIcon>
              <span @click="onDelete">删除</span>
            </div>
          </div>
          <div class="file-label">
            <div class="label-title">属性</div>
            <div class="label-item">
              <div class="label-color"></div>
              <span>论文全文</span>
            </div>
            <div class="label-item">
              <div class="label-color gray"></div>
              <span>论文摘要</span>
            </div>
          </div>

        </div>

        <div class="article__page">
          <span class="first-page" @click="onFirstPage">首页</span>
          <el-pagination
            @current-change="onPageChange"
            v-model:current-page="pageCurrent"
            background
            layout="prev, pager, next"
            :total="pageCount" />
          <span class="last-page" @click="onLastPage">尾页</span>
        </div>

      </section>
    </div>
  </main>
</template>
<script setup>
import { ref } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import Search from '../components/Search.vue'
import Nav from '../components/Nav.vue'
import searchService from '../services/search.js'
import context from '../core/context'

const keyword = ref('')
const fileList = ref([])

const isSearchDone = ref(false)

const pageSize = ref(10)
const pageCount = ref(0)
const pageCurrent = ref(1)


const onSearch = async (keywordText) => {
  keyword.value = keywordText
  await search()
}

const onSelectAll = async () => {

}

const onDelete = async () => {

}


const search = async () => {
  isSearchDone.value = false
  const loading = ElLoading.service({
    lock: true,
    text: '搜索中...',
    background: 'rgba(255, 255, 255, 0.7)',
  })

  try {
    getFiles()
  } catch (err) {
    console.log(err)
    ElMessage({
      message: '未找到数据',
      type: 'warning',
    })
  } finally {
    loading.close()
    isSearchDone.value = true
  }
}


const getFiles = async () => {
  fileList.value = [
    {
      name: 'dsdsdsdsdsds.pdf',
      id: '1222',
      type: 0,
    },
    {
      name: 'ddsdsdsdsdsds.pdf',
      id: '122d2',
      type: 1,

    },
    {
      name: 'dsdsxdsdsdsds.pdf',
      id: '12x22',
      type: 0,
    },
  ]
  return
  let page = pageCurrent.value
  let start = (page - 1) * pageSize.value
  let end = page * pageSize.value

  let data = await searchService.searchArticle(keyword.value, topLevel.value)
  articleCount.value = data.number_article
  articleOriginalList.value = data.table
  articleList.value = Array.from(articleOriginalList.value)
  articleExcel.value = data.file_name
  pageCount.value = data.table.length
}

const onPageChange = (page) => {
  pageCurrent.value = page
  getFiles()
}

const onFirstPage = () => {
  pageCurrent.value = 1
  getFiles()
}

const onLastPage = () => {
  pageCurrent.value = Math.ceil(pageCount.value / pageSize.value)
  getFiles()
}


const init = () => {
}

init()

</script>
