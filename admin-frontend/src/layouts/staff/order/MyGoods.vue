<!--
@File        : Mydishes.vue
@Author      : ChiLei Tai
@Date        : 2025-04-01
@Description : Ordering System
-->
<template>
  <div class="adseus">
    <el-icon color="#409EFF" size="27px"><Search /></el-icon>
    <el-input class="adseusinput" placeholder="请输入菜品编号" v-model="input1"> </el-input>
    <el-button class="adseus-button" @click="search" type="primary">查询</el-button>
    <el-button class="adseus-reload" @click="reload" type="primary">重置</el-button>
  </div>
  <div>
    <el-table class="adustable" :data="tableData" height="400" style="width: 200%">
      <el-table-column prop="id" label="菜品编号" width="100%" />
      <el-table-column prop="dishName" label="菜品名称" width="150%" />
      <el-table-column prop="shopsource" label="商家名称" width="100%" />
      <el-table-column prop="sell" label="销量" width="100%" />
      <el-table-column prop="remain" label="库存" width="100%" />
      <el-table-column prop="cate" label="种类" width="100%" />
      <el-table-column prop="price" label="价格" width="100%" />
      <el-table-column prop="imageUrl" label="图片">
        <template v-slot="scope">
          <el-image :src="scope.row.imageUrl" :preview-src-list="[scope.row.imageUrl]"></el-image>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" min-width="200%">
        <template #default="scope">
          <el-button @click="drawer = { visible: true, row: scope.row }" size="small" type="primary"
            >修改</el-button
          >
          <el-button type="danger" size="small" @click="Delete(scope.row)"> 删除 </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <!-- 添加抽屉组件 -->
  <el-drawer title="修改物资信息" v-model="drawer.visible" :direction="direction">
    <div>
      <el-form :model="drawer.row">
        <el-form-item label="菜品名称">
          <el-input v-model="drawer.row.dishName"></el-input>
        </el-form-item>
        <el-form-item label="菜品种类">
          <el-input v-model="drawer.row.cate"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="update" @click="update(drawer.row)">修改</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-drawer>
</template>
<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { getStoreDishes, updateDish, removeDish, searchDish } from '@/api/dish'
  import { ElMessageBox, ElMessage } from 'element-plus'
  import { Search } from '@element-plus/icons-vue'

  const drawer = reactive({ visible: false, row: null })
  const direction = ref('rtl')
  const tableData = ref([])
  const input1 = ref('')

  const init = () => {
    getStoreDishes({ userid: sessionStorage.getItem('userid') }).then((res) => {
      tableData.value = res.data
    })
  }

  const reload = () => {
    init()
  }

  const update = (row) => {
    updateDish({ dishId: row.id, dishName: row.dishName, cate: row.cate }).then(() => {
      ElMessage.success('修改成功')
      init()
    })
  }

  const Delete = (row) => {
    ElMessageBox.confirm('是否确认删除？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
      .then(() => {
        removeDish({ id: row.id, dishName: row.dishName, cate: row.cate }).then(() => {
          ElMessage.success('删除成功')
          init()
        })
      })
      .catch(() => {
        ElMessage.info('已取消删除')
      })
  }

  const search = () => {
    searchDish({ dishId: input1.value, dishName: input1.value }).then((res) => {
      tableData.value = res.data
    })
  }

  onMounted(() => {
    init()
  })
</script>
<style>
  .adustable {
    margin-left: -15%;
    margin-top: 15%;
  }
  .adseus {
    margin-left: -15%;
    margin-top: 5%;
    width: 30%;
  }
  .adseusinput {
    margin-left: 60%;
    margin-top: -17%;
    width: 50%;
  }
  .adseus-button {
    margin-top: -4.5%;
    margin-left: 20%;
    position: absolute;
    z-index: 10000;
  }
  .update {
    margin-top: 20px;
    margin-left: 40%;
  }
  .adseus-reload {
    position: absolute;
    left: 26%;
    margin-top: -4.5%;
  }
</style>
