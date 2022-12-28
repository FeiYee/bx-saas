<template>
  <Search @search="onSearch" :isSearchDone="isSearchDone"/>
  <Nav />
  <!-- <Keyword :keywords="keywords" @click="onKeywordClick" @reload="onKeywordReload"/> -->
  <!-- <div class="containers"></div> -->
  <main class="home content">
    <div class="container">
      <section class="content-primary">
        <h3 class="content-title">知识图谱</h3>
        <div class="content-stat">
          <div class="content-stat__total">
            <span>共检索到实体关系数量：{{linkCount}}</span>
            <span>节点数量：{{nodeCount}}</span>
            <!-- <span>文章数量：{{articleCount}}</span> -->
          </div>
          <!-- <div class="content-stat__node">
            <span>节点: </span>
            <span class="node-number">{{nodeCount}}</span>
          </div> -->
        </div>
        <div class="content-graph">
          <div id="chartRelationship"  class="chart-relationship"></div>
        </div>
        <ul class="content-article-list">
          <li class="content-article-item">
            <article class="content-article" v-show="!!article.title">
              <h3 class="article__title">题目：{{article.title}}</h3>
              <div class="article__info">
                <span>
                  <span class="info-title">作者：</span>
                  <span class="info-content__author" :title="article.Author">{{article.Author}}</span>
                </span>
                <span>
                  <span class="info-title">刊名：</span>
                  <span class="info-content__name" :title="article.name">{{article.name}}</span></span>
                <span>
                  <span class="info-title">日期：</span>
                  <span class="info-content__year" :title="article.Year">{{article.Year}}</span>
                </span>
              </div>
              <div class="article__summary">
                {{article.Abstract}}
              </div>
              <div class="article__link">
                <button @click="onOriginalArticle">原文获取</button>
              </div>
              <table class="article__detail">
                <thead>
                  <tr>
                    <th>药物</th>
                    <th>机理</th>
                    <th>通路/靶标</th>
                    <th>指标</th>
                    <th>结论</th>
                    <th v-show="!!article['Side Effect']">副作用</th>
                    <th v-show="!!article.Group">分组</th>
                    <th v-show="!!article['Sample count']">样本量</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{article.Drugs}}</td>
                    <td>{{article.Molecular}}</td>
                    <td>{{article['Pathway/Target']}}</td>
                    <td>{{article.Indicator}}</td>
                    <td>{{article.Result}}</td>
                    <td v-show="!!article['Side Effect']">{{article['Side Effect']}}</td>
                    <td v-show="!!article.Group">{{article.Group}}</td>
                    <td v-show="!!article['Sample count']">{{article['Sample count']}}</td>
                  </tr>
                </tbody>
              </table>
            </article>
          </li>
        </ul>
      </section>
      <section class="content-aside">
        <div>
          <h3 class="content-title">节点类型统计</h3>
          <div class="chart-box">
            <div id="chartPie" class="chart-pie"></div>
          </div>
        </div>
        <div>
          <h3 class="content-title">每日更新统计</h3>
          <div class="chart-box">
            <div id="chartBar" class="chart-bar"></div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>
<script setup>
import { ref, reactive, inject, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import Search from '../components/Search.vue'
import Nav from '../components/Nav.vue'
// import Keyword from '../components/Keyword.vue'

import {downloadFile} from '../core/download.js'

import searchService from '../services/search.js'
import keywordService from '../services/keyword.js'
import datumService from '../services/datum.js'

import {getRelationData, setChartRelation, setChartPie, setChartBar} from '../chart/chart.js'
import {relationChart} from '../chart/relation.js'
import context from '../core/context'

// const echarts = inject('echarts')

// let keyword = ref('')
// let keywords = ref([])
let isSearchDone = ref(false)

const article = reactive({
  Title: '',   // 文章名
  Author: '',   // 作者
  Abstract: '', // 摘要
  Drugs: '', // 药物
  Indicator: '', // 指标
  Molecular: '', // 机理
  Result: '',   // 结论
  Year: '',  // 发表年份
  title: '',  // 文章名
  name: '',
  Group: '', // 分组
  'Pathway/Target': '', // 通路/靶标
  'Side Effect': '',  // 副作用
  'Sample count': '', // 样本量
})

let articleCount = ref(0)
let linkCount = ref(0)
let nodeCount = ref(0)

const chartRelationshipDomId = 'chartRelationship'
const chartBarDomId = 'chartBar'
const chartPieDomId = 'chartPie'
let chartBar = null
let chartPie = null
let chartRelationship = null

const onSearch = async (keyword) => {
  isSearchDone.value = false
  const loading = ElLoading.service({
    lock: true,
    text: '搜索中...',
    background: 'rgba(255, 255, 255, 0.7)',
  })

  try {
    let data = await searchService.searchGraph(keyword)

    if (data) {
      articleCount.value = data.number_article
      linkCount.value = data.number_links
      nodeCount.value = data.number_nodes
      let nodesCount = data.nodes_count
      let upData = data.up_date

      let relationData = getRelationData(data)

      if (chartRelationship) {
        chartRelationship.dispose()
      }
      // chartRelationship = setChartRelation(relationData, chartRelationshipDomId, handleNodeClick)
      relationChart(relationData, handleNodeClick)
      chartPie = setChartPie(chartPieDomId, nodesCount)
      chartBar = setChartBar(chartBarDomId, upData)

      isSearchDone.value = true
    } else {
      ElMessage({
        message: '未找到数据',
        type: 'warning',
      })
    }

    // await getKeywords()
  } catch (err) {
    console.log(err)
  } finally {
    loading.close()

  }
}

// const onKeywordClick = async (keywordText) => {
//   console.log(keywordText)
//   keyword.value = keywordText
//   await onSearch(keywordText)
// }

// const onKeywordReload = async () => {
//   await getKeywords()
// }

const onOriginalArticle = async () => {
  if (article.title) {
    console.log(article.title)
  }
  let data = await datumService.download(article.title)
  console.log(data)
  if (!data) {
    ElMessage({
      message: '未找到原文',
      type: 'warning',
    })
    return
  }
  downloadFile(data.url, data.file_name)

}

const handleNodeClick = (node) => {
  console.log(node)
  article.title = node.title
  article.Title = node.title  // 文章名
  article.name = node.name
  article.Abstract = node.Abstract
  article.Year = node.Year
  article.Author = node.Author
  article.Drugs = node.Drugs // 药物
  article.Indicator = node.Indicator // 指标
  article.Molecular = node.Molecular // 机理
  article.Result = node.Result   // 结论
  article.Group = node.Group // 分组
  article['Pathway/Target'] = node['Pathway/Target'] // 通路/靶标
  article['Side Effect'] = node['Side Effect']   // 副作用
  article['Sample count'] = node['Sample count'] // 样本量
}

// const getKeywords = async () => {
//   keywords.value = await keywordService.getUserKeywords(0)
// }

// const init = async () => {
//   // await getKeywords()
//   let keywordText = context.getKeyword()

//   if (!keywordText && keywords.value.length) {
//     keywordText = keywords.value[0].keyword
//   }
//   if (keywordText) {
//     keyword.value = keywordText
//     onSearch(keywordText)
//   }
// }



onMounted(() => {
  // chartRelationship = setChartRelation(null, chartRelationshipDomId, handleNodeClick)
  chartBar = setChartBar(chartBarDomId)
  chartPie = setChartPie(chartPieDomId)

// relationChart({}, handleNodeClick)
})

onBeforeUnmount(() => {
  if (chartBar) {
    chartBar.dispose()
  }
  if (chartPie) {
    chartPie.dispose()
  }
  if (chartRelationship) {
    chartRelationship.dispose()
  }
})

// init()


</script>
