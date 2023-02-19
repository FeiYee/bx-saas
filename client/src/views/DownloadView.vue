<template>
  <Search @search="onSearch" :isSearchDone="isSearchDone" />
  <Nav />
  <main class="download content">
    <div class="container">
      <section class="content-primary">
        <h3 class="content-title">数据下载</h3>
        <div class="content-stat">
          <div class="content-stat__total">
            <!-- <span>共检索到实体关系数量：530</span>
            <span>节点类型数量：305</span> -->
            <span>文章数量：{{articleCount}}</span>
          </div>
        </div>
        <div class="content-main">
          <div>
            <div class="article-content">

              <table class="article__detail">
                <thead>
                  <tr>
                    <th>主题</th>
                    <th>药物</th>
                    <th>机理</th>
                    <th>通路/靶标</th>
                    <th>指标</th>
                    <th>结论</th>
                    <th>副作用</th>
                    <th>分组</th>
                    <th>样本量</th>
                    <th>期刊</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="article in articles" :key="article.id">
                    <td>{{article.Title}}</td>
                    <td>{{article.Drugs}}</td>
                    <td>{{article.Molecular}}</td>
                    <td>{{article['Pathway/Target']}}</td>
                    <td>{{article.Indicator}}</td>
                    <td>{{article.Result}}</td>
                    <td>{{article['Side Effect']}}</td>
                    <td>{{article.Group}}</td>
                    <td>{{article['Sample count']}}</td>
                    <td>{{article.Year}}</td>
                  </tr>
                  <!-- <tr>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                    <td>研究人工虫草提取物和奥美沙坦</td>
                  </tr> -->
                </tbody>
              </table>
            </div>
          </div>
          <div class="content-top">
            <h4>选择</h4>
            <ul>
              <li :class="{'is-active': topLevel === 0}" @click="onTopClick(0)">全部</li>
              <li :class="{'is-active': topLevel === 30}" @click="onTopClick(30)">top30</li>
              <li :class="{'is-active': topLevel === 20}" @click="onTopClick(20)">top20</li>
              <li :class="{'is-active': topLevel === 10}" @click="onTopClick(10)">top10</li>
            </ul>
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
        <div class="download-btn">
          <button @click="onDownload">下载 Excel</button>
        </div>

      </section>
    </div>
  </main>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import Search from '../components/Search.vue'
import Nav from '../components/Nav.vue'
import searchService from '../services/search.js'
import {downloadFile} from '../core/download.js'
import context from '../core/context'

const keyword = ref('')
const articleExcel = ref('')
const articles = ref([])
const articleList = ref([])
const articleOriginalList = ref([])

const isSearchDone = ref(false)
const articleCount = ref(0)

const pageSize = ref(10)
const pageCount = ref(0)
const pageCurrent = ref(1)

const topLevel = ref(0)

const onSearch = async (keywordText) => {
  keyword.value = keywordText
  await search()
}

const onTopClick = async (level) => {
  topLevel.value = level
  context.setTopLevel(level)
  await search()

  // if (level === 30) {
  //   pageCount.value =  Math.min(articleList.value.length, 30)
  //   if (pageCount.value > 30) {
  //     articleList.value = articleOriginalList.value.slice(0, 30)
  //   } else {
  //     articleList.value = Array.from(articleOriginalList.value)
  //   }
  // } else if (level === 20) {
  //   pageCount.value = Math.min(articleList.value.length, 20)
  //   if (pageCount.value > 20) {
  //     articleList.value = articleOriginalList.value.slice(0, 20)
  //   } else {
  //     articleList.value = Array.from(articleOriginalList.value)
  //   }
  // } else if (level === 10) {
  //   pageCount.value = Math.min(articleList.value.length, 10)
  //   if (pageCount.value > 10) {
  //     articleList.value = articleOriginalList.value.slice(0, 10)
  //   } else {
  //     articleList.value = Array.from(articleOriginalList.value)
  //   }
  // } else {
  //   articleList.value = Array.from(articleOriginalList.value)
  //   pageCount.value = articleOriginalList.value.length
  // }
  // pageCurrent.value = 1
  // getArticles()
}

const search = async () => {
  isSearchDone.value = false
  // topLevel.value = 0
  const loading = ElLoading.service({
    lock: true,
    text: '搜索中...',
    background: 'rgba(255, 255, 255, 0.7)',
  })

  try {
    let data = await searchService.searchArticle(keyword.value, topLevel.value)
    articleCount.value = data.number_article
    articleOriginalList.value = data.table
    articleList.value = Array.from(articleOriginalList.value)
    articleExcel.value = data.file_name
    pageCount.value = data.table.length

    getArticles()
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


const getArticles = () => {
  let page = pageCurrent.value
  let start = (page - 1) * pageSize.value
  let end = page * pageSize.value

  if (pageCurrent * pageSize.value > pageCount) {
    articles.value = articleList.value.slice(start)
  } else {
    articles.value = articleList.value.slice(start, end)
  }
}

const onPageChange = (page) => {
  pageCurrent.value = page
  getArticles()
}

const onFirstPage = () => {
  pageCurrent.value = 1
  getArticles()
}

const onLastPage = () => {
  pageCurrent.value = Math.ceil(pageCount.value / pageSize.value)
  getArticles()
}

const onDownload = async () => {
  downloadFile(articleExcel.value, '搜索结果.xlsx')
}

const init = () => {
  topLevel.value = context.getTopLevel() || 0
}

init()
</script>
