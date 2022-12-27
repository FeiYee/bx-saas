<template>
  <div class="">
    <!-- <el-row>
      <el-col :span="24">
        <el-collapse :model-value="1" @change="handleChange">
          <el-collapse-item title="查询" :name="1">
            <el-form :inline="true" :model="formInline" class="demo-form-inline">
              <el-form-item label="用户名">
                <el-input v-model="formInline.user" placeholder="Approved by" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit">查询</el-button>
              </el-form-item>
            </el-form>
          </el-collapse-item>
        </el-collapse>
      </el-col>
    </el-row> -->

    <el-row class="view-title">
      <el-col :span="12">
        <h4>用户</h4>
      </el-col>
      <el-col :span="12" class="align-right">
        <el-button type="primary" plain size="small" @click="onCreate">新增</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-table :data="userList" border stripe style="width: 100%">
          <el-table-column prop="username" label="用户名" width="180" />
          <el-table-column prop="password" label="密码" width="180" />
          <el-table-column prop="name" label="名称" width="180" />
          <el-table-column prop="is_admin" label="管理员" width="70">
            <template #default="scope">
              <el-switch v-model="scope.row.is_admin" size="small" disabled/>
            </template>
          </el-table-column>
          <el-table-column prop="email" label="邮箱" show-overflow-tooltip />
          <el-table-column fixed="right" label="操作" width="98">
            <template #default="scope">
              <!-- <el-button link type="primary" size="small" @click="handleClick">查看</el-button> -->
              <el-button link type="warning" size="small" @click="onUpdate(scope.row)">编辑</el-button>
              <el-button link type="danger" size="small" @click="onDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <!-- <el-row>
      <el-col :span="24">
        <el-pagination background small layout="prev, pager, next" :total="1000" />
      </el-col>
    </el-row> -->

    <el-dialog v-model="dialogVisible" title="用户">
      <el-form :model="user" label-width="70px">
        <el-form-item label="用户名">
          <el-input v-model="user.username" autocomplete="off" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="user.password" autocomplete="off" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="user.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="user.email" autocomplete="off" />
        </el-form-item>
        <el-form-item label="管理员">
          <el-switch v-model="user.is_admin" size="small" />
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
import systemService from '../../services/system.js'

const dialogVisible = ref(false)

const user = reactive({
  id: null,
  username: "",
  password: "",
  name: "",
  email: "",
  is_admin: false
})

const userList = ref([])

const userCondition = reactive({
  username: '',
})

const setUser = (data) => {
  user.id = data ? data.id : null
  user.username = data ? data.username : ''
  user.password = data ? data.password : ''
  user.name = data ? data.name : ''
  user.email = data ? data.email : ''
  user.is_admin = data ? data.is_admin : false
}

const onUpdate = async (row) => {
  setUser(row)
  dialogVisible.value = true
}

const onDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `此操作将删除用户【${row.username}】, 是否继续?`,
      '删除确认',
      {
        confirmButtonText: '确 认',
        cancelButtonText: '取 消',
        type: 'error',
      }
    )
    try {
      await systemService.deleteUser(row.id)
      await getUsers()
      ElMessage({type: 'success', message: '删除成功'})
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
  if (user.id) {
    updateUser()
  } else {
    createUser()
  }
}

const onCancel = () => {
  dialogVisible.value = false
  setUser()
}

const getUsers = async () => {
  let data = toRaw(user)
  let users = await systemService.getUsers(data)
  userList.value = users
}

const createUser = async () => {
  let data = toRaw(user)
  try {
    await systemService.createUser(data)
    setUser()
    getUsers()
    ElMessage({type: 'success', message: '新增成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '新增失败'})
  }
}

const updateUser = async () => {
  let data = toRaw(user)
  try {
    await systemService.updateUser(data)
    setUser()
    getUsers()
    ElMessage({type: 'success', message: '更新成功'})
  } catch(e) {
    ElMessage({type: 'error', message: '更新失败'})
  }
}


getUsers()

</script>

