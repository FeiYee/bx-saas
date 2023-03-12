<template>
  <div class="">

    <el-row class="view-title">
      <el-col :span="12">
        <h4>{{ modelValue.name }}</h4>
      </el-col>
      <el-col :span="12" class="align-right">
        <el-button type="primary" plain size="small" @click="onCreate">新增</el-button>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="24">
        <el-table :data="paperDatumList" border stripe style="width: 100%">
          <el-table-column prop="name" label="名称" show-overflow-tooltip/>
          <el-table-column prop="description" label="描述" show-overflow-tooltip/>
          <!-- <el-table-column prop="url" label="url" show-overflow-tooltip/> -->
          <el-table-column prop="type" label="类型" show-overflow-tooltip>
            <template #default="scope">
              <span>{{ getFileType(scope.row.type) }}</span>
              <!-- <el-tag class="ml-2" type="info">{{ getFileType(scope.row.type) }}</el-tag> -->
            </template>
          </el-table-column>
          <el-table-column prop="file_name" label="文件名" width="180" show-overflow-tooltip/>
          <!-- <el-table-column prop="file_path" label="文件路径" width="180" show-overflow-tooltip/> -->
          <el-table-column prop="file_size" label="文件大小" width="90" show-overflow-tooltip/>
          <el-table-column fixed="right" label="操作" width="98">
            <template #default="scope">
              <!-- <el-button link type="success" size="small" @click="onDetail(scope.row)">详情</el-button> -->
              <el-button link type="warning" size="small" @click="onUpdate(scope.row)">编辑</el-button>
              <el-button link type="danger" size="small" @click="onDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="用户资料">
      <el-form :model="paperDatum" label-width="60px">
        <el-form-item label="名称">
          <el-input v-model="paperDatum.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="paperDatum.description" autocomplete="off" />
        </el-form-item>
        <el-form-item label="文件">
          <el-upload
            class="paper-upload"
            v-model:file-list="files"
            :auto-upload="false"
            :limit="1"
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

  </div>
</template>
<script  setup>
import { defineEmits, reactive, ref, toRaw, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getFileType } from '../core/file.js'
import paperDatumService from '../services/paper-datum.js'

const props = defineProps({
  modelValue: Object,
});

const dialogVisible = ref(false)

const paperDatum = reactive({
  id: null,
  name: "",
  description: "",
  file: null,
})

const paperDatumList = ref([])
const files = ref([])


const emit = defineEmits(['update:modelValue']);

watch(
  () => props.modelValue,
  value => {
    console.log(value)
    if (value && value.id) {
      getPaperDatums()
    }
  },
  {
    deep: true
  }
)

watch(
  () => files,
  value => {
    console.log(value)
  }
)

const setPaperDatum = (data) => {
  paperDatum.id = data ? data.id : null
  paperDatum.name = data ? data.name : ''
  paperDatum.description = data ? data.description : ''
  paperDatum.file = data ? data.file : null

  files.value = data && data.id ? [{name: data.file_name, url: data.url}] : [];
}


const onDetail = async (row) => {
  console.log(row)
  setPaperDatum(row)
  dialogVisible.value = true
}

const onUpdate = async (row) => {
  console.log(row)
  setPaperDatum(row)
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
      await paperDatumService.deletePaperDatum(row.id)
      await getPaperDatums()
      ElMessage({type: 'success', message: '删除成功'})
    } catch (e) {
      ElMessage({type: 'error', message: '删除失败'})
    }
  } catch {
    ElMessage({type: 'info', message: '已取消删除'})
  }
}

const onCreate = () => {
  setPaperDatum()
  dialogVisible.value = true
}

const onConfirm = () => {
  dialogVisible.value = false
  if (paperDatum.id) {
    updatePaperDatum()
  } else {
    createPaperDatum()
  }
}

const onCancel = () => {
  dialogVisible.value = false
  setPaperDatum()
}

const onFileChange = file => {
  paperDatum.file = file.raw
  console.log(files)
}

const onFileRemove = file => {
  paperDatum.file = null
}

const getPaperDatums = async () => {
  let paperId = props.modelValue.id
  if (!paperId) {
    return
  }
  let paperDatums = await paperDatumService.getPaperDatums(paperId)
  paperDatumList.value = paperDatums
}

const createPaperDatum = async () => {
  let paperId = props.modelValue.id
  let data = toRaw(paperDatum)
  console.log(data)
  try {
    await paperDatumService.createPaperDatum(paperId, data)
    setPaperDatum()
    getPaperDatums()
    ElMessage({type: 'success', message: '新增成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '新增失败'})
  }
}

const updatePaperDatum = async () => {
  let data = toRaw(paperDatum)
  if (!data.file) {
    delete data.file
  }
  try {
    await paperDatumService.updatePaperDatum(data)
    setPaperDatum()
    getPaperDatums()
    ElMessage({type: 'success', message: '更新成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '更新失败'})
  }
}


getPaperDatums()

</script>
<style>
.paper-title {
  width: 100%;
}
</style>
