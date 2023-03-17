<template>
  <div class="">
    <el-row>
      <el-col :span="24">
        <el-collapse :model-value="1">
          <el-collapse-item title="选择组织" :name="1">
            <el-form :inline="true" :model="org">
              <el-form-item label="组织" required>
                <el-select v-model="org.id" placeholder="选择" @change="onChange" >
                  <el-option v-for="item in orgList" :key="item.id" :label="item.name" :value="item.id" />
                </el-select>
              </el-form-item>
            </el-form>
          </el-collapse-item>
        </el-collapse>
      </el-col>
    </el-row>
    <el-row class="view-title">
      <el-col :span="12">
        <h4>组织用户</h4>
      </el-col>
      <el-col :span="12" class="align-right">
        <el-button type="primary" plain size="small" @click="onCreate">新增</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-table :data="orgUserList" border stripe style="width: 100%">
          <el-table-column prop="org_name" label="组织" show-overflow-tooltip/>
          <el-table-column prop="user_name" label="用户" show-overflow-tooltip/>
          <el-table-column prop="org_id" label="组织ID" show-overflow-tooltip/>
          <el-table-column prop="user_id" label="用户ID" show-overflow-tooltip/>
          <el-table-column fixed="right" label="操作" width="56">
            <template #default="scope">
              <el-button link type="danger" size="small" @click="onDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="用户">
      <el-table :data="userList" ref="userTableRef" border stripe style="width: 100%">
          <el-table-column type="selection" width="40" />
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="name" label="名称" />
        </el-table>
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
import { context, systemService } from 'lib'

// import systemService from '../../services/system.js'

const dialogVisible = ref(false)
const userTableRef = ref('')

const org = reactive({
  id: null,

})

const orgList = ref([])
const orgUserList = ref([])
const userList = ref([])

const setOrg = (data) => {
  org.id = data ? data.id : null
  org.name = data ? data.name : ''
  org.code = data ? data.code : ''
  org.abbreviation = data ? data.abbreviation : ''
  org.logo = data ? data.logo : ''
}

const onChange = async (orgId) => {
  console.log(orgId)
  getOrgUsers(org)
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

  // userTableRef.value.clearSelection()
}

const onConfirm = async () => {
  let rows = userTableRef.value.getSelectionRows()
  let userIdList = []
  rows.forEach(item => {
    userIdList.push(item.id)
  })
  console.log(userIdList)
  await createOrgUser(userIdList)
  return
  dialogVisible.value = false
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

const getOrgUsers = async (orgId) => {
  let data = toRaw(org)
  let orgs = await systemService.getOrgUsers(data)
  orgUserList.value = orgs
}

const getUsers = async () => {
  // let data = toRaw(user)
  let data = {}
  let users = await systemService.getUsers(data)
  userList.value = users
}


const createOrgUser = async (userIdList) => {
  let data = toRaw(org)
  let orgId = data.id
  try {
    await systemService.createOrgUser(orgId, userIdList)
    getOrgUsers()
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
getUsers()

</script>

