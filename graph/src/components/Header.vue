<template>
  <header class="header">
    <div class="container">
      <a class="logo" href="/">
        <img src="/logo.png" alt="Logo" srcset="">
      </a>
      <div class="account">
        <!-- <el-avatar :size="50" :src="circleUrl" /> -->
        <el-dropdown>
        <span class="el-dropdown-link">
          <el-avatar :size="50" :src="user.avatar" />
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <span style="padding-right: 10px">用户</span>
              <span>{{ user.username }}</span>
              <!-- <el-tag type="success" effect="light" >{{ user.username }}</el-tag> -->
            </el-dropdown-item>
            <el-dropdown-item v-if="!!user.name" >
              <span style="padding-right: 10px">姓名</span>
              <span>{{ user.name }}</span>
              <!-- <el-tag type="primary" effect="light" >{{ user.name }}</el-tag> -->
            </el-dropdown-item>
            <el-dropdown-item v-if="!!user.orgName" divided>
              <span style="padding-right: 10px">组织</span>
              <span>{{ user.orgName }}</span>
              <!-- <el-tag type="success" effect="light" >{{ user.orgName }}</el-tag> -->
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
        <button @click="logout">退出</button>
      </div>
    </div>
  </header>
</template>
<script setup>
import { reactive, toRefs } from 'vue'
import { useRouter } from 'vue-router'
import context from '../core/context.js'
const router = useRouter()

const user = reactive({
  username: '',
  name: '',
  avatar: '/avatar.png',
  orgName: '',
})


const { avatar } = toRefs(user)

const logout = function() {
  context.setToken('')
  router.push('/login')
}

const getUser = () => {
  if (!context.getUser() || !context.getUser().user) {
    logout()
  }
  let userData = context.getUser().user
  user.username = userData.username
  user.name = userData.name

  let orgData = context.getUser().org
  user.orgName = orgData?.name
}

getUser()

</script>
