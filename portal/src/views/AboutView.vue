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
    </el-row>

    <el-row>
      <el-col :span="12">
        <h4>用户</h4>
      </el-col>
      <el-col :span="12">
        <el-button type="primary" plain size="small">新增</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-table :data="tableData" border stripe style="width: 100%">
          <el-table-column prop="date" label="Date" width="180" />
          <el-table-column prop="name" label="Name" width="180" />
          <el-table-column prop="address" label="Address" />
          <el-table-column fixed="right" label="Operations" width="140">
            <template #default>
              <el-button link type="primary" size="small" @click="handleClick">查看</el-button>
              <el-button link type="warning" size="small">编辑</el-button>
              <el-button link type="danger" size="small">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-pagination background small layout="prev, pager, next" :total="1000" />
      </el-col>
    </el-row>

    <el-dialog v-model="dialogFormVisible" title="Shipping address">
      <el-form :model="form">
        <el-form-item label="Promotion name" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Zones" :label-width="formLabelWidth">
          <el-select v-model="form.region" placeholder="Please select a zone">
            <el-option label="Zone No.1" value="shanghai" />
            <el-option label="Zone No.2" value="beijing" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">Cancel</el-button>
          <el-button type="primary" @click="dialogFormVisible = false">
            Confirm
          </el-button>
        </span>
      </template>
    </el-dialog> -->

  </div>
</template>
<script  setup>
import { reactive, ref } from 'vue'
import systemService from '../services/system.js'

const dialogTableVisible = ref(false)
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'

const form = reactive({
  name: '',
  region: '',
  date1: '',
  date2: '',
  delivery: false,
  type: [],
  resource: '',
  desc: '',
})
const formInline = reactive({
  user: '',
  region: '',
})

const onSubmit = () => {
  console.log('submit!')
}
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]

// systemService.getUser({
//   id: "str",
//   username: "str",
//   password: "str",
//   name: "str",
//   email: "str",
// })
</script>
<style>

</style>
