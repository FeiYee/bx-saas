<template>
  <Search @search="onSearch" :isSearchDone="isSearchDone" />
  <Nav />
  <main class="home content">
    <div class="container">
      <div class="content-primary">
        <section class="content-graph" :class="{full: showType === 1}" v-show="showType === 0 || showType === 1">
          <h3 class="content-title">
            <span style="padding-left:2rem;">知识图谱</span>
            <el-icon @click="onClickShow(1)" v-show="showType === 0"><ArrowRight color="#ffffff"/></el-icon>
          </h3>
          <div class="content-stat">
            <div class="content-stat__total">
              <span>共检索到文章数量：{{ articleCount }}</span>
            </div>
          </div>
          <div class="graph-box">
            <div id="chartRelationship" class="chart-relationship"></div>
          </div>
        </section>
        <section class="content-detail" :class="{full: showType === 2}" v-show="showType === 0 || showType === 2">
          <h3 class="content-title">
            <el-icon @click="onClickShow(2)" v-show="showType === 0"><ArrowLeft color="#ffffff" :size="62"/></el-icon>
            <span style="padding-right:2rem;">内容简述</span>
          </h3>
          <div style="padding: 20px;">
            <Preview v-model="articleExtracts" @export="onExport"/>
          </div>
          <div class="file-original">
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :limit="2"
              :on-change="onFileChange"
              :on-remove="onFileRemove"
              action="/" >
              <el-button type="success">上传论文原文PDF文件</el-button>
            </el-upload>
          </div>
        </section>
      </div>

      <!-- 药厂版本不显示 -->
      <!-- <div class="content-operate">
        <div class="operate-btn" @click="onClickShow(1)">知识图谱</div>
        <div class="operate-btn" @click="onClickShow(2)">内容</div>
        <div class="operate-btn" @click="onClickShow(0)">内容 + 知识图谱</div>
      </div> -->

      <div>
        <ul class="content-article-list">
          <li class="content-article-item">
            <article class="content-article" v-show="!!article.title">
              <h3 class="article__title">题目：{{ article.title }}</h3>
              <div class="article__info">
                <span>
                  <span class="info-title">作者：</span>
                  <span class="info-content__author" :title="article.author">{{ article.author }}</span>
                </span>
                <span>
                  <span class="info-title">刊名：</span>
                  <span class="info-content__name" :title="article.name">{{ article.name }}</span></span>
                <span>
                  <span class="info-title">日期：</span>
                  <span class="info-content__year" :title="article.year">{{ article.year }}</span>
                </span>
              </div>
              <div class="article__summary">
                {{ article.abstract }}
              </div>
              <div class="article__link">
                <button @click="onOriginalArticle">原文获取</button>
              </div>
              <table class="article__detail">
                <thead>
                  <tr>
                    <th>药物</th>
                    <th>疾病</th>
                    <th>通路/靶标</th>
                    <th>指标</th>
                    <th>结论</th>
                    <th v-show="!!article.side_effect">副作用</th>
                    <th v-show="!!article.group">分组</th>
                    <th v-show="!!article.other">其他</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ article.drugs }}</td>
                    <td>{{ article.disease }}</td>
                    <td>{{ article.pathway_target}}</td>
                    <td>{{ article.indicator }}</td>
                    <td>{{ article.result }}</td>
                    <td v-show="!!article.side_effect">{{ article.side_effect}}</td>
                    <td v-show="!!article.group">{{ article.group }}</td>
                    <td v-show="!!article.other">{{ article.other }}</td>
                  </tr>
                </tbody>
              </table>
            </article>
          </li>
        </ul>
      </div>
    </div>

  </main>
</template>
<script setup>
import { ref, reactive, toRaw, inject, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import Search from '../components/Search.vue'
import Nav from '../components/Nav.vue'
import Preview from '../components/Preview.vue'

import { downloadFile } from '../core/download.js'
import { filePrefix } from '../core/config.js'

import searchService from '../services/search.js'
import keywordService from '../services/keyword.js'
import datumService from '../services/datum.js'
import articleExtractService from '../services/article-extract.js'
import articleDatumService from '../services/article-datum.js'

import { getRelationData } from '../chart/chart.js'
import { relationChart } from '../chart/relation.js'
import context from '../core/context'


let isSearchDone = ref(false)
const showType = ref(1); // 0->内容 + 知识图谱; 1->知识图谱; 2->内容
const uploadRef = ref()

let articleExtracts = ref([])
let articleExtractExport = ref(null)

const articleDatum = reactive({
  article_id: "",
  keyword: "",
  file: null,
});

const article = reactive({
  id: '',
  title: '',   // 文章名
  name: '',
  summary: '', // 摘要
  content: '',
  author: '',   // 作者
  date: '',
  molecular: '', // 机理
  journal: '',
  doi: '',
  pmid: '',
  relate_count: '',
  result: '',   // 结论
  effect: '',
  sample_count: '', // 样本量
  indicator: '', // 指标
  group: '', // 分组
  drugs: '', // 药物
  disease: '',
  side_effect: '',  // 副作用
  microbe: '',
  cell: '',
  gene: '',
  pathway_target: '', // 通路/靶标
  other:'',
  year:''
})

let articleCount = ref(0)
let linkCount = ref(0)
let nodeCount = ref(0)

const chartRelationshipDomId = 'chartRelationship'

let chartRelationship = null

const onSearch = async (keyword) => {
  isSearchDone.value = false;
  articleDatum.keyword = keyword;

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

      let relationData = getRelationData(data)

      if (chartRelationship) {
        chartRelationship.dispose()
      }
      // chartRelationship = setChartRelation(relationData, chartRelationshipDomId, handleNodeClick)
      relationChart(relationData, handleNodeClick)

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


const onClickShow = async (type) => {
  showType.value = type;
}

const onFileChange = file => {
  articleDatum.file = file.raw;
  console.log(articleDatum)
  uploadArticleDatum();
}

const onFileRemove = file => {
  articleDatum.file = null
}

const onOriginalArticle = async () => {
  if (!article.id) {
    console.log(article)
    ElMessage({
      message: '未找到原文',
      type: 'warning',
    })
  }
  let data = await datumService.getDatumByArticle(article.id)
  if (!data) {
    ElMessage({
      message: '未找到原文',
      type: 'warning',
    })
    return
  }
  downloadFile(data.url, data.file_name)
};

const onExport = () => {
  console.log(articleExtractExport.value);
  if (!articleExtractExport.value) {
    ElMessage({
      message: '导出文件不存在',
      type: 'warning',
    });
    return
  }
  downloadFile(articleExtractExport.value.url, articleExtractExport.value.file_name)
}

const handleNodeClick = (node) => {
  console.log(node)
  article.id = node.article_id  // 文章ID
  article.title = node.title  // 文章名
  article.name = node.name
  article.summary = node.summary
  article.content = node.content
  article.author = node.author
  article.date = node.date
  article.molecular = node.molecular // 机理
  article.journal = node.journal
  article.doi = node.doi
  article.pmid = node.pmid
  article.relate_count = node.relate_count
  article.result = node.result   // 结论
  article.effect = node.effect
  article.sample_count = node.sample_count // 样本量
  article.indicator = node.indicator // 指标
  article.group = node.group // 分组
  article.drugs = node.drugs // 药物
  article.disease = node.disease
  article.side_effect = node.side_effect   // 副作用
  article.microbe = node.microbe
  article.cell = node.cell
  article.gene = node.gene
  article.other=node.other
  article.year=node.date
  article.pathway_target = node.pathway_target // 通路/靶标
  articleDatum.article_id = node.article_id || node.id || '';

  getArticleExtracts(node.id)
};


const getArticleExtracts = async (articleId) => {
  articleExtractExport.value = null;
  let list = await articleExtractService.getArticleExtracts(articleId)
  let datas = []
  list.forEach(item => {
    item.url = filePrefix + item.url;
    if (item.type === 3) {
      articleExtractExport.value = item;
      return;
    }
    datas.push(item);
  })
  articleExtracts.value = datas
};


const uploadArticleDatum = async () => {
  console.log(toRaw(articleDatum))
  try {
    let res = await articleDatumService.uploadArticleDatum(toRaw(articleDatum));
    articleDatum.file = null;
    uploadRef.value.clearFiles();
    if (res) {
      ElMessage({
        message: '原文上传成功',
        type: 'success',
      })
    }
  } catch (e) {
    console.log(e)
  }
};


onBeforeUnmount(() => {
  if (chartRelationship) {
    chartRelationship.dispose()
  }
})


</script>
