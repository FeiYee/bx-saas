<template>
  <div class="login">
    <el-container>
      <el-header>
        <el-row class="view-title">
        <el-col :span="12">
          <h1>BX-SaaS管理系统</h1>
        </el-col>
      </el-row>
      </el-header>
      <el-main>
        <div class="box">
          <h3 class="title">欢迎登录</h3>
          <el-form ref="ruleFormRef" :model="auth" :rules="rules" label-width="60px"
            :size="formSize" status-icon>
            <el-form-item label="账号" prop="username">
              <el-input v-model="auth.username" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="auth.password" type="password"/>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm(ruleFormRef)">登录</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-main>
    </el-container>
  </div>
</template>
<script setup>
import { reactive, ref, toRaw } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import context from '../core/context.js'
import authService from '../services/auth.js'

const router = useRouter()

const formSize = ref('default')
const ruleFormRef = ref()
const auth = reactive({
  username: 'admin',
  password: '123',
  // username: '',
  // password: '',
})

const rules = reactive({
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
})

const submitForm = async (formEl) => {
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      await login(toRaw(auth))

    } else {
      console.log('error submit!', fields)
    }
  })
}

const login = async (data) => {
  try {
    let token = await authService.login(data)
    if (token && token.access_token) {
      context.setToken(token.access_token)

      let userDetail = await authService.getUserDetail()
      if (!userDetail || !userDetail.user.is_admin) {
        ElMessage({
          message: '此用户不是管理员',
          type: 'warning',
        })
        return
      }
      context.setUser(userDetail)
      router.push('/')
    } else {
      ElMessage({
        message: '登录失败',
        type: 'warning',
      })
    }
  } catch (err) {
    console.log(err)
    ElMessage({
      message: err.detail || '登录失败',
      type: 'warning',
    })
  }

}

</script>
<style lang="scss">
.login {
  height: 100vh;
  background-image: url('/bg.png');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;

  .el-main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 60px);
    min-height: 300px;
  }

  .box {
    width: 400px;
    padding: 2rem;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;

    .title {
      margin: 0;
      padding-bottom: 2rem;
    }
    button {
      width: 100%;
    }
  }
}

</style>
