<template>
  <div class="">
    <!-- <el-row class="search-box" >
      <el-col :span="24">
        <el-collapse :model-value="1">
          <el-collapse-item title="查询" :name="1">
            <el-form :inline="true" :model="paperSearch">
              <el-form-item label="用户" required>
                <el-select v-model="paperSearch.user_id" placeholder="选择" >
                  <el-option v-for="item in userList" :key="item.id" :label="item.username" :value="item.id" />
                </el-select>
              </el-form-item>
            </el-form>
          </el-collapse-item>
        </el-collapse>
      </el-col>
    </el-row> -->

    <el-row class="view-title">
      <el-col :span="12">
        <h4>用户资料</h4>
      </el-col>
      <el-col :span="12" class="align-right">
        <el-button type="primary" plain size="small" @click="onCreate">新增</el-button>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="24">
        <el-table :data="paperList" border stripe style="width: 100%">
          <el-table-column prop="name" label="名称" show-overflow-tooltip/>
          <el-table-column prop="description" label="描述" show-overflow-tooltip/>
          <!-- <el-table-column prop="url" label="url" show-overflow-tooltip/> -->
          <el-table-column prop="type" label="类型" show-overflow-tooltip>
            <template #default="scope">
              <span>{{ fileUtil.getFileType(scope.row.type) }}</span>
              <!-- <el-tag class="ml-2" type="info">{{ fileUtil.getFileType(scope.row.type) }}</el-tag> -->
            </template>
          </el-table-column>
          <el-table-column prop="file_name" label="文件名" width="180" show-overflow-tooltip/>
          <!-- <el-table-column prop="file_path" label="文件路径" width="180" show-overflow-tooltip/> -->
          <el-table-column prop="file_size" label="文件大小" width="90" show-overflow-tooltip/>
          <el-table-column prop="user_id" label="用户" show-overflow-tooltip/>
          <el-table-column fixed="right" label="操作" width="140">
            <template #default="scope">
              <!-- <el-button link type="success" size="small" @click="onDetail(scope.row)">详情</el-button> -->
              <el-button link type="warning" size="small" @click="onUpdate(scope.row)">编辑</el-button>
              <el-button link type="danger" size="small" @click="onDelete(scope.row)">删除</el-button>
              <el-button link type="primary" size="small" @click="onDetailDatum(scope.row)">附件</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="用户资料">
      <el-form :model="paper" label-width="60px">
        <el-form-item label="用户" required>
          <el-select v-model="paper.user_id" placeholder="选择" >
            <el-option v-for="item in userList" :key="item.id" :label="item.username" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="paper.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="paper.description" autocomplete="off" />
        </el-form-item>
        <el-form-item label="文件">
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
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel">取 消</el-button>
          <el-button type="primary" @click="onConfirm">确 认</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="dialogDatumVisible" @close="onCloseDatum()"
      title="资料附件" width="75vw" :close-on-click-modal="false">
      <PaperDatum v-model="paper" />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancelDatum">关 闭</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>
<script  setup>
import { reactive, ref, toRaw, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
// import { getFileType } from '../../core/file.js'
import { fileUtil, paperService, systemService } from 'lib'
import PaperDatum from '../../components/PaperDatum.vue'

const dialogVisible = ref(false)
const dialogDatumVisible = ref(false)

const paperSearch = reactive({
  id: null,
  name: "",
  description: "",
  user_id: "",
})

const paper = reactive({
  id: null,
  name: "",
  description: "",
  file: null,
  user_id: "",
})

const paperList = ref([])
const userList = ref([])
const files = ref([])

// watch(
//   () => dialogDatumVisible,
//   value => {
//     setPaper()
//   }
// )

const setPaper = (data) => {
  paper.id = data ? data.id || null : null
  paper.name = data ? data.name || '' : ''
  paper.description = data ? data.description || '' : ''
  paper.user_id = data ? data.user_id || '' : ''
  paper.file = data ? data.file || null : null
  files.value = data && data.id ? [{name: data.file_name, url: data.url}] : [];
}


const onDetail = async (row) => {
  console.log(row)
  setPaper(row)
  dialogVisible.value = true
}

const onUpdate = async (row) => {
  console.log(row)
  setPaper(row)
  dialogVisible.value = true
}

const onDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `此操作将删除文件【${row.file_name}】, 是否继续?`,
      '删除确认',
      {
        confirmButtonText: '确 认',
        cancelButtonText: '取 消',
        type: 'error',
      }
    )
    try {
      await paperService.deletePaper(row.id)
      await getPapers()
      ElMessage({type: 'success', message: '删除成功'})
    } catch (e) {
      ElMessage({type: 'error', message: '删除失败'})
    }
  } catch {
    ElMessage({type: 'info', message: '已取消删除'})
  }
}


const onDetailDatum = async (row) => {
  console.log(row)
  setPaper(row)
  dialogDatumVisible.value = true
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


const onCancelDatum = () => {
  console.log(paper)
  dialogDatumVisible.value = false
  // setPaper()
}

const onCloseDatum = () => {
  setPaper()
}


const getPapers = async () => {
  let papers = await paperService.getPapers()
  paperList.value = papers
}

const createPaper = async () => {
  let data = toRaw(paper)
  console.log(data)
  try {
    await paperService.createPaper(data)
    setPaper()
    getPapers()
    ElMessage({type: 'success', message: '新增成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '新增失败'})
  }
}

const updatePaper = async () => {
  let data = toRaw(paper)
  if (!data.file) {
    delete data.file
  }
  try {
    await paperService.updatePaper(data)
    setPaper()
    getPapers()
    ElMessage({type: 'success', message: '更新成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '更新失败'})
  }
}

const getUsers = async () => {
  let users = await systemService.getUsers()
  userList.value = users
}

const init = async () => {
  getPapers()
  getUsers()
}

init()

</script>
<style>
.paper-title {
  width: 100%;
}
</style>
