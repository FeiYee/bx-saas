<template>
  <Search @search="onSearch" :isSearchDone="isSearchDone" />
  <Nav />
  <main class="file content paper">
    <div class="container">
      <div class="upload-btn">
        <ElButton type="success" @click="onCreate">上传</ElButton>
      </div>
      <section class="content-primary">

        <ElCard class="box-card" v-for="paper in papers" :key="paper.id" shadow="never">
          <template #header>
            <div class="card-header">
              <ElTooltip effect="dark" :content="paper.description" placement="top" >
                <span>{{ paper.name }}</span>
              </ElTooltip>
            </div>
          </template>
          <Preview v-model="paper.paper_datums" :is-export-disabled="true" @export="onExport"/>
        </ElCard>

      </section>
    </div>
  </main>

  <ElDialog v-model="dialogVisible" title="用户资料">
      <ElForm :model="paper" label-width="60px">
        <ElFormItem label="名称">
          <el-input v-model="paper.name" autocomplete="off" />
        </ElFormItem>
        <ElFormItem label="描述">
          <el-input v-model="paper.description" autocomplete="off" />
        </ElFormItem>
        <ElFormItem label="文件">
          <el-upload
            class="paper-upload"
            v-model:file-list="files"
            :auto-upload="false"
            :limit="2"
            drag
            :on-change="onFileChange"
            :on-remove="onFileRemove"
            action="/" >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                文件大小不超过 10M
              </div>
            </template>
          </el-upload>
        </ElFormItem>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="onCancel">取 消</ElButton>
          <ElButton type="primary" @click="onConfirm">确 认</ElButton>
        </span>
      </template>
    </ElDialog>
</template>
<script setup>
import { ref, reactive, toRaw, inject, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, ElButton, ElLoading, ElDialog, ElCard, ElForm, ElFormItem, ElTooltip } from 'element-plus'
import Search from '../components/Search.vue'
import Nav from '../components/Nav.vue'
import Preview from '../components/Preview.vue'
import paperService from '../services/paper.js'
import searchService from '../services/search.js'
import { filePrefix } from '../core/config.js'

let isSearchDone = ref(false)
const dialogVisible = ref(false)

const files = ref([])
const papers = ref([])
const paperExport = ref(null)


const paper = reactive({
  id: null,
  name: "",
  description: "",
  file: null,
})

const onSearch = async (keyword) => {
  isSearchDone.value = false;
  // articleDatum.keyword = keyword;

  const loading = ElLoading.service({
    lock: true,
    text: '搜索中...',
    background: 'rgba(255, 255, 255, 0.7)',
  })

  try {
    let data = await searchService.searchPaper(keyword)
    if (data && !data.length) {
      ElMessage({
        message: '未找到数据',
        type: 'warning',
      });
      return;
    }

    if (data) {
      let datas = []
      data.forEach(item => {
        item.url = filePrefix + item.url;
        item.paper_datums.forEach(item => {
          item.url = filePrefix + item.url;
        })
        if (item.type === 3) {
          paperExport.value = item;
          return;
        }
        datas.push(item);
      })
      papers.value = datas;
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

const onExport = () => {
  if (!paperExport.value) {
    ElMessage({
      message: '导出文件不存在',
      type: 'warning',
    });
    return
  }
  downloadFile(paperExport.value.url, paperExport.value.file_name)
}


const onCreate = () => {
  setPaper()
  dialogVisible.value = true
}

const onConfirm = () => {
  dialogVisible.value = false
  if (paper.id) {
    updatePaper()
  } else {
    createPaper()
  }
}

const onCancel = () => {
  dialogVisible.value = false
  setPaper()
}

const onFileChange = file => {
  paper.file = file.raw
  files.value = [file]
}

const onFileRemove = file => {
  paper.file = null
  files.value = []
}

const setPaper = (data) => {
  paper.id = data ? data.id || null : null
  paper.name = data ? data.name || '' : ''
  paper.description = data ? data.description || '' : ''
  paper.user_id = data ? data.user_id || '' : ''
  paper.file = data ? data.file || null : null
  files.value = data && data.id ? [{name: data.file_name, url: data.url}] : [];
}


const createPaper = async () => {
  let data = toRaw(paper)
  try {
    await paperService.createPaper(data)
    setPaper()
    onSearch()
    ElMessage({type: 'success', message: '新增成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '新增失败'})
  }
}

</script>
<style lang="scss">

.paper {
  .upload-btn {
    text-align: right;
    margin-bottom: 20px;
  }
  .content-primary {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    .el-card {
      width: 49%;
      margin-bottom: 30px;
    }

  }
  .el-popper.is-customized {
    /* Set padding to ensure the height is 32px */
    padding: 6px 12px;
    background: linear-gradient(90deg, rgb(159, 229, 151), rgb(204, 229, 129));
  }

  .el-popper.is-customized .el-popper__arrow::before {
    background: linear-gradient(45deg, #b2e68d, #bce689);
    right: 0;
  }
}

</style>
