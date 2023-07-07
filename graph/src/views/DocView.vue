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
                <input v-model="item.checked" type="checkbox" name="" id="">
              </div>
              <div class="file-name" :class="{summary: item.type==1}">{{ item.file_name }}</div>
            </li>
            <!-- <li class="file-item">
              <div class="file-check">
                <input type="checkbox" name="" id="">
              </div>
              <div class="file-name summary">dfsfsdf</div>
            </li> -->
          </ul>

        </div>

        <div class="file-info">
          <div class="file-operate">
            <div class="operate-item">
              <input v-model="isSelectAll" type="checkbox" name="selectAll" id="selectAll" @change="onSelectAllChange">
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
import { ref, reactive, toRaw, unref } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import Search from '../components/Search.vue'
import Nav from '../components/Nav.vue'
import articleDatumService from '../services/article-datum.js'
import context from '../core/context'

const keyword = ref('')
const fileList = ref([])
const isSelectAll = ref(false)

const articleDatum = reactive({
  article_id: "",
  keyword: "",
});

const isSearchDone = ref(false)

const pageSize = ref(10)
const pageCount = ref(0)
const pageCurrent = ref(1)


const onSearch = async (keywordText) => {
  keyword.value = keywordText
  articleDatum.keyword = keywordText
  await search()
}


const onSelectAllChange = async () => {
  fileList.value.forEach(item => {
    item.checked = isSelectAll.value
  })
}

const onSelectAll = async () => {
  // isSelectAll.value = !isSelectAll.value;
  fileList.value.forEach(item => {
    item.checked = isSelectAll.value
  })
}

const onDelete = async () => {
  const checkedList = fileList.value.filter(item => {
    return item.checked
  })
  const loading = ElLoading.service({
    lock: true,
    text: '搜索中...',
    background: 'rgba(255, 255, 255, 0.7)',
  })

  try {
    checkedList.forEach(async (item) => {
      await articleDatumService.deleteArticleDatum(item.id)
    })
  } catch (err) {
    console.log(err)
    ElMessage({
      message: '删除失败',
      type: 'warning',
    })
  }  finally {
    loading.close()
  }

  console.log(checkedList)

  isSelectAll.value = false
  await search()
}


const search = async () => {
  isSearchDone.value = false
  const loading = ElLoading.service({
    lock: true,
    text: '搜索中...',
    background: 'rgba(255, 255, 255, 0.7)',
  })

  try {
    await getFiles()
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
  try {
    let data = await articleDatumService.getArticleDatumsByUser(toRaw(articleDatum))
    fileList.value = data;

  } catch (e) {

  }
};

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
  search();
}

init()

</script>
