<template>
  <div class="register">
    <el-container>
      <el-header></el-header>
      <el-main>
        <div class="box">
          <div class="box-header">
            <h3 class="title">Welcome BAIX</h3>
            <div class="title-tip">
              <span>Have account?  </span>
              <el-link type="success" @click="onClick" >Log in</el-link>
            </div>
          </div>
          <el-form
            ref="registerForm"
            :model="auth"
            :rules="rules"
            label-width="90px"
            :size="formSize"
            status-icon>
            <el-form-item label="Account" prop="username">
              <el-input v-model="auth.username" />
            </el-form-item>
            <el-form-item label="Password" prop="password">
              <el-input v-model="auth.password" type="password"/>
            </el-form-item>
            <!-- <el-form-item label="确认密码" prop="password">
              <el-input v-model="auth.password1" type="password"/>
            </el-form-item> -->
            <el-form-item label="Email" prop="email">
              <el-input v-model="auth.email" type="email"/>
            </el-form-item>
            <el-form-item label="Domain" prop="domain">
              <el-input v-model="auth.domain"/>
            </el-form-item>
            <!-- <el-form-item label="记住密码" prop="type">
            <el-checkbox-group v-model="auth.type">
              <el-checkbox label="记住密码" name="type" />
            </el-checkbox-group>
          </el-form-item> -->
            <el-form-item>
              <el-button type="success" @click="onRegister(registerForm)">Register</el-button>
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
import authService from '../services/auth.js'

const router = useRouter()

const formSize = ref('default')
const registerForm = ref()
const auth = reactive({
  username: '',
  password: '',
  email: '',
  domain: '',
})

const rules = reactive({
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
  ],
  domain: [
    { required: true, message: '请输入域', trigger: 'blur' },
  ],
})

const onClick = () => {
  router.push('/login')
}

const onRegister = async (registerForm) => {
  await registerForm.validate(async (valid, fields) => {
    if (valid) {
      await register(toRaw(auth))
    } else {
      console.log('error submit!', fields)
    }
  })
}

const register = async (data) => {
  try {
    let user = await authService.register(data)
    if (user && user.id) {
      ElMessage({
      message: '注册成功, 请登录',
      type: 'success',
    })
      router.push('/login')
    }
  } catch (err) {
    console.log(err)
    ElMessage({
      message: err.detail || '注册失败',
      type: 'warning',
    })
  }
};

</script>
<style>

</style>
