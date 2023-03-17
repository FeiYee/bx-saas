<template>
  <div class="">
    <el-row class="view-title">
      <el-col :span="12">
        <h4>组织</h4>
      </el-col>
      <el-col :span="12" class="align-right">
        <el-button type="primary" plain size="small" @click="onCreate">新增</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-table :data="orgList" border stripe style="width: 100%">
          <el-table-column prop="code" label="编码" width="180" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="abbreviation" label="简称" />
          <el-table-column prop="logo" label="Logo"  width="180"/>
          <el-table-column fixed="right" label="操作" width="98">
            <template #default="scope">
              <el-button link type="warning" size="small" @click="onUpdate(scope.row)">编辑</el-button>
              <el-button link type="danger" size="small" @click="onDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="组织">
      <el-form :model="org" :label-width="formLabelWidth">
        <el-form-item label="编码">
          <el-input v-model="org.code" autocomplete="off" />
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="org.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="简称">
          <el-input v-model="org.abbreviation" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Logo">
          <el-input v-model="org.logo" autocomplete="off" />
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
// import systemService from '../../services/system.js'
import { context, systemService } from 'lib'

const dialogVisible = ref(false)
const formLabelWidth = '80px'

const org = reactive({
  id: null,
  name: "",
  code: "",
  abbreviation: "",
  logo: "",
})

const orgList = ref([])

const setOrg = (data) => {
  org.id = data ? data.id : null
  org.name = data ? data.name : ''
  org.code = data ? data.code : ''
  org.abbreviation = data ? data.abbreviation : ''
  org.logo = data ? data.logo : ''
}

const onUpdate = async (row) => {
  setOrg(row)
  dialogVisible.value = true
}

const onDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `此操作将删除组织【${row.name}】, 是否继续?`,
      '删除确认',
      {
        confirmButtonText: '确 认',
        cancelButtonText: '取 消',
        type: 'error',
      }
    )
    try {
      await systemService.deleteOrg(row.id)
      ElMessage({type: 'success', message: '删除成功'})
      await getOrgs()
    } catch (e) {
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
  if (org.id) {
    updateOrg()
  } else {
    createOrg()
  }
}

const onCancel = () => {
  dialogVisible.value = false
  setOrg()
}

const getOrgs = async () => {
  let data = {}
  let orgs = await systemService.getOrgs(data)
  orgList.value = orgs
}

const createOrg = async () => {
  let data = toRaw(org)
  try {
    await systemService.createOrg(data)
    setOrg()
    getOrgs()
    ElMessage({type: 'success', message: '新增成功'})
  } catch (e) {
    ElMessage({type: 'error', message: '新增失败'})
  }
}

const updateOrg = async () => {
  let data = toRaw(org)
  try {
    await systemService.updateOrg(data)
    setOrg()
    getOrgs()
    ElMessage({type: 'success', message: '更新成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '更新失败'})
  }
}

getOrgs()
</script>

