<template>
  <h2 style="width: 200px">菜品上架</h2>
  <div class="adddish">
    <el-form :model="form" label-width="80px">
      <el-form-item label="菜品名称">
        <el-input v-model="form.dishName"></el-input>
      </el-form-item>
      <el-form-item label="菜品种类">
        <el-select v-model="form.cate" placeholder="菜品种类">
          <el-option label="图书" value="图书"></el-option>
          <el-option label="电子产品" value="电子产品"></el-option>
          <el-option label="文具" value="文具"></el-option>
          <el-option label="衣服" value="衣服"></el-option>
          <el-option label="化妆品" value="化妆品"></el-option>
          <el-option label="食品" value="食品"></el-option>
          <el-option label="户外运动" value="户外运动"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="上架数量">
        <el-input v-model="form.all"></el-input>
      </el-form-item>
      <el-form-item label="菜品单价">
        <el-input v-model="form.price"></el-input>
      </el-form-item>
      <el-form-item label="菜品图">
        <el-input v-model="form.imageUrl"></el-input>
      </el-form-item>
      <el-form-item label="菜品描述">
        <el-input type="textarea" v-model="form.desc"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即创建</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script setup>
  import { reactive } from 'vue'
  import { addDish } from '@/api/dish'
  import { ElNotification } from 'element-plus'

  const form = reactive({
    dishName: '',
    cate: '',
    all: '',
    price: '',
    imageUrl: '',
    desc: '',
  })

  const onSubmit = () => {
    addDish({
      dishName: form.dishName,
      cate: form.cate,
      all: form.all,
      price: form.price,
      imageUrl: form.imageUrl,
      desc: form.desc,
      userid: sessionStorage.getItem('userid'),
      username: sessionStorage.getItem('username'),
    }).then((res) => {
      if (res !== '') {
        ElNotification({
          title: '成功',
          message: '添加成功,请等待管理员审核',
          type: 'success',
        })
      } else {
        ElNotification({
          title: '失败',
          message: '添加失败',
          type: 'error',
        })
      }
    })
    console.log('submit!')
  }
</script>
<style>
  .adddish {
    margin-top: 20%;
    margin-left: -30%;
    width: 120%;
  }
</style>
