<template>
  <div class="">
    <el-row class="view-title">
      <el-col :span="12">
        <h4>文件</h4>
      </el-col>
      <el-col :span="12" class="align-right">
        <el-button type="primary" plain size="small" @click="onCreate">新增</el-button>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="24">
        <el-table :data="datumList" border stripe style="width: 100%">
          <el-table-column prop="title" label="标题" show-overflow-tooltip/>
          <el-table-column prop="file_name" label="文件名" width="180" show-overflow-tooltip/>
          <el-table-column prop="file_path" label="文件路径" width="180" show-overflow-tooltip/>
          <el-table-column prop="file_size" label="文件大小" width="90" show-overflow-tooltip/>
          <el-table-column fixed="right" label="操作" width="98">
            <template #default="scope">
              <el-button link type="warning" size="small" @click="onUpdate(scope.row)">编辑</el-button>
              <el-button link type="danger" size="small" @click="onDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="文件">
      <el-form :model="datum" label-width="60px">
        <el-form-item label="标题">
          <el-select v-model="datum.title" class="datum-title m-2" placeholder="Select">
            <el-option
              v-for="item in titleList"
              :key="item"
              :label="item"
              :value="item"/>
          </el-select>
        </el-form-item>
        <el-form-item label="文件">
          <el-upload
            class="datum-upload"
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
import { reactive, ref, toRaw } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
// import datumService from '../../services/datum.js'
import { context, datumService } from 'lib'

const dialogVisible = ref(false)

const title = ref('')

const datum = reactive({
  id: null,
  title: "",
  file: null,
  file_name: "",
})

const datumList = ref([])
const titleList = ref([])


const setDatum = (data) => {
  datum.id = data ? data.id : null
  datum.title = data ? data.title : ''
  datum.file = data ? data.file : null
  datum.file_name = data ? data.file_name : true
}


const onUpdate = async (row) => {
  console.log(row)
  setDatum(row)
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
      await datumService.deleteDatum(row.id)
      await getDatums()
      ElMessage({type: 'success', message: '删除成功'})
    } catch (e) {
      ElMessage({type: 'error', message: '删除失败'})
    }
  } catch {
    ElMessage({type: 'info', message: '已取消删除'})
  }
}

const onCreate = () => {
  setDatum()
  dialogVisible.value = true
}

const onConfirm = () => {
  dialogVisible.value = false
  if (datum.id) {
    updateDatum()
  } else {
    createDatum()
  }
}

const onCancel = () => {
  dialogVisible.value = false
  setDatum()
}

const onFileChange = file => {
  datum.file = file.raw
}

const onFileRemove = file => {
  datum.file = null
}

const getDatums = async () => {
  let datums = await datumService.getDatums()
  datumList.value = datums
}

const createDatum = async () => {
  let data = toRaw(datum)
  console.log(data)
  try {
    await datumService.createDatum(data)
    setDatum()
    getDatums()
    ElMessage({type: 'success', message: '新增成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '新增失败'})
  }
}

const updateDatum = async () => {
  let data = toRaw(datum)
  try {
    await datumService.updateDatum(data)
    setDatum()
    getDatums()
    ElMessage({type: 'success', message: '更新成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '更新失败'})
  }
}


const getArticleTitle = async () => {
  let titles = await datumService.getArticleTitle(title.value)
  titleList.value = titles
}

getDatums()
getArticleTitle()

</script>
<style>
.datum-title {
  width: 100%;
}
</style>
