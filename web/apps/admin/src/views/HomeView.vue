<template>
  <el-container>
    <el-header class="layout-header">
      <el-row class="header-box">
        <el-col :span="12">
          <h1>BX-SaaS</h1>
        </el-col>
        <el-col :span="12" class="align-right">
          <el-dropdown @command="handleCommand" style="color: #ffffff;">
            <span class="el-dropdown-link">
              {{user.username}}
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <!-- <el-dropdown-item icon="Plus">Action 1</el-dropdown-item> -->
                <!-- <el-dropdown-item divided icon="CirclePlus">Action 3</el-dropdown-item> -->
                <el-dropdown-item  command="logout" icon="SwitchButton" >注销</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-col>
      </el-row>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-scrollbar>
          <el-menu
            active-text-color="#81C784"
            class="el-menu-vertical-demo"
            :default-active="activePath"
            :default-openeds="['/search', '/datum', '/system']"
            router
            style="height: calc(100vh - 60px);">
            <el-sub-menu index="/datum">
              <template #title>
                <el-icon>
                  <Management />
                </el-icon>资料管理
              </template>
              <el-menu-item index="/datum/datum">文件管理</el-menu-item>
              <el-menu-item index="/datum/paper">用户资料</el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="/search">
              <template #title>
                <el-icon>
                  <Promotion />
                </el-icon>搜索管理
              </template>
              <el-menu-item index="/search/keyword">关键词设置</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="/system">
              <template #title>
                <el-icon>
                  <Tools />
                </el-icon>系统管理
              </template>
              <el-menu-item index="/system/user">用户管理</el-menu-item>
              <el-menu-item index="/system/org">组织管理</el-menu-item>
              <el-menu-item index="/system/orguser">组织用户</el-menu-item>

            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>
      <el-main>
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import { reactive, ref, toRaw } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { context, authService } from 'lib'

// import context from '../core/context.js'

const router = useRouter()

const activePath = ref('/')
const user = reactive({
  username: '',
  name: '',
  avatar: '/avatar.png'
})

const handleCommand = cmd => {
  logout()
}

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
}

getUser()

</script>
