<template>
  <div class="login">
    <el-container>
      <el-header></el-header>
      <el-main>
        <div class="box">
          <h3 class="title">欢迎登录</h3>
          <el-form
            ref="loginForm"
            :model="auth"
            :rules="rules"
            label-width="60px"
            :size="formSize"
            status-icon>
            <el-form-item label="账号" prop="username">
              <el-input v-model="auth.username" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="auth.password" type="password"/>
            </el-form-item>
            <!-- <el-form-item label="记住密码" prop="type">
            <el-checkbox-group v-model="auth.type">
              <el-checkbox label="记住密码" name="type" />
            </el-checkbox-group>
          </el-form-item> -->
            <el-form-item>
              <el-button type="primary" @click="onLogin(loginForm)">登录</el-button>
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
const loginForm = ref()
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

const onLogin = async (loginForm) => {
  await loginForm.validate(async (valid, fields) => {
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
    }
    let userDetail = await authService.getUserDetail()

    context.setUser(userDetail)
    router.push('/')
  } catch (err) {
    console.log(err)
    ElMessage({
      message: err.detail || '登录失败',
      type: 'warning',
    })
  }

}
</script>
<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
