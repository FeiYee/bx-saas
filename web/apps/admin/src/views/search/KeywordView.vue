<template>
  <div class="">
    <el-row class="view-title">
      <el-col :span="12">
        <h4>关键词</h4>
      </el-col>
      <el-col :span="12" class="align-right">
        <el-button type="primary" plain size="small" @click="onCreate">新增</el-button>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="24">
        <el-table :data="keywordList" border stripe style="width: 100%">
          <el-table-column prop="keyword" label="关键词" show-overflow-tooltip/>
          <el-table-column prop="weight" label="权重"  width="120"/>
          <!-- <el-table-column prop="type" label="类型"  width="60"/> -->
          <el-table-column prop="is_preset" label="预置" width="60">
            <template #default="scope">
              <el-switch v-model="scope.row.is_preset" size="small" disabled/>
            </template>
          </el-table-column>
          <el-table-column prop="org_id" label="组织" show-overflow-tooltip />
          <el-table-column prop="user_id" label="用户" show-overflow-tooltip />
          <el-table-column fixed="right" label="操作" width="98">
            <template #default="scope">
              <el-button link type="warning" size="small" @click="onUpdate(scope.row)">编辑</el-button>
              <el-button link type="danger" size="small" @click="onDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="关键词">
      <el-form :model="keyword" :label-width="formLabelWidth">
        <el-form-item label="关键词">
          <el-input v-model="keyword.keyword" autocomplete="off" />
        </el-form-item>
        <el-form-item label="权重">
          <el-input-number v-model="keyword.weight" autocomplete="off" />
        </el-form-item>
        <!-- <el-form-item label="类型">
          <el-select v-model="keyword.type" class="m-2" placeholder="Select">
            <el-option label="图谱" :value="0"/>
            <el-option label="文章" :value="1"/>
          </el-select>
        </el-form-item> -->
        <el-form-item label="预置">
          <el-switch v-model="keyword.is_preset" size="small" />
        </el-form-item>
        <el-form-item label="组织">
          <!-- <el-input v-model="keyword.password" autocomplete="off" /> -->
          <el-select v-model="keyword.org_id" class="m-2" placeholder="Select">
            <el-option
              v-for="item in orgList"
              :key="item.id"
              :label="item.name"
              :value="item.id"/>
          </el-select>
        </el-form-item>
        <el-form-item label="用户">
          <!-- <el-input v-model="keyword.name" autocomplete="off" /> -->
          <el-select v-model="keyword.user_id" class="m-2" placeholder="Select">
            <el-option
              v-for="item in userList"
              :key="item.id"
              :label="item.username"
              :value="item.id"/>
          </el-select>
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
// import searchService from '../../services/search.js'
// import systemService from '../../services/system.js'
import { context, searchService, systemService } from 'lib'

const dialogVisible = ref(false)
const formLabelWidth = '80px'

const keyword = reactive({
  id: null,
  keyword: "",
  weight: 0,
  // type: 0,
  is_preset: true,
  user_id: "",
  org_id: "",
})

const keywordList = ref([])
const orgList = ref([])
const userList = ref([])

const setKeyword = (data) => {
  keyword.id = data ? data.id : null
  keyword.keyword = data ? data.keyword : ''
  keyword.weight = data ? data.weight : 0
  keyword.is_preset = data ? data.is_preset : true
  keyword.user_id = data ? data.user_id : ''
  keyword.org_id = data ? data.org_id : ''
}

const onUpdate = async (row) => {
  setKeyword(row)
  dialogVisible.value = true
}

const onDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `此操作将删除关键词【${row.keyword}】, 是否继续?`,
      '删除确认',
      {
        confirmButtonText: '确 认',
        cancelButtonText: '取 消',
        type: 'error',
      }
    )
    try {
      await searchService.deleteKeyword(row.id)
      await getKeywords()
      ElMessage({type: 'success', message: '删除成功'})
    } catch (e) {
      console.log(e)
      ElMessage({type: 'error', message: '删除失败'})
    }
  } catch {
    ElMessage({type: 'info', message: '已取消删除'})
  }
}

const onCreate = () => {
  dialogVisible.value = true
}

const onConfirm = () => {
  dialogVisible.value = false
  if (keyword.id) {
    updateKeyword()
  } else {
    createKeyword()
  }
}

const onCancel = () => {
  dialogVisible.value = false
  setKeyword()
}

const getKeywords = async () => {
  let data = {}
  let keywords = await searchService.getKeywords(data)
  keywordList.value = keywords
}

const createKeyword = async () => {
  let data = toRaw(keyword)
  try {
    await searchService.createKeyword(data)
    setKeyword()
    getKeywords()
    ElMessage({type: 'success', message: '新增成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '新增失败'})
  }
}

const updateKeyword = async () => {
  let data = toRaw(keyword)
  try {
    await searchService.updateKeyword(data)
    setKeyword()
    getKeywords()
    ElMessage({type: 'success', message: '更新成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '更新失败'})
  }
}

const getOrgs = async () => {
  let data = {}
  let orgs = await systemService.getOrgs(data)
  orgList.value = orgs
}

const getUsers = async () => {
  let data = {}
  let users = await systemService.getUsers(data)
  userList.value = users
}

getKeywords()
getOrgs()
getUsers()


</script>
