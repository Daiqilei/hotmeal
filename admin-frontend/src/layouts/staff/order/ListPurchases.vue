<template>
  <div class="adsebu">
    <el-icon color="#409EFF" size="27px"><Search /></el-icon>
    <el-input class="adsebuinput" placeholder="请输入订单编号" v-model="input1"> </el-input>
    <el-button class="adsebu-button" @click="search" type="primary">查询</el-button>
    <el-button class="adsebu-reload" @click="reload" type="primary">重置</el-button>
  </div>
  <div class="adbuli">
    <el-table class="adbutable" :data="tableData" height="400" style="width: 100%">
      <el-table-column fixed prop="id" label="订单编号" width="100%" />
      <el-table-column prop="dishId" label="菜品编号" width="100%" />
      <el-table-column prop="dishName" label="菜品名称" width="100%" />
      <el-table-column prop="imageUrl" label="图片">
        <template v-slot="scope">
          <el-image :src="scope.row.imageUrl" :preview-src-list="[scope.row.imageUrl]"></el-image>
        </template>
      </el-table-column>
      <el-table-column prop="sellerid" label="商家编号" width="100%" />
      <el-table-column prop="addtime" label="下单时间" width="100%" />
      <el-table-column prop="price" label="价格" width="100%" />
      <el-table-column prop="address" label="地址" width="100%" />
      <el-table-column prop="status" label="订单状态" width="100%" />
      <el-table-column prop="price" label="价格" width="100%" />
    </el-table>
  </div>
  <!-- 添加抽屉组件 -->
</template>
<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { Search } from '@element-plus/icons-vue'
  import { getSellerOrders, searchOrderByIdOrName } from '@/api/order'

  const drawer = reactive({ visible: false, row: null })
  const direction = ref('rtl')
  const tableData = ref([])
  const input1 = ref('')

  const init = () => {
    getSellerOrders({ userid: sessionStorage.getItem('userid') }).then((res) => {
      tableData.value = res.data
    })
  }

  const reload = () => {
    getSellerOrders({ userid: sessionStorage.getItem('userid') }).then((res) => {
      tableData.value = res.data
    })
  }
  const search = () => {
    searchOrderByIdOrName({
      orderId: input1.value,
      username: input1.value,
    }).then((res) => {
      tableData.value = res.data
    })
  }

  onMounted(() => {
    init()
  })
</script>
<style>
  .adbutable {
    margin-left: -15%;
    margin-top: 15%;
  }

  .adsebu {
    margin-left: -15%;
    margin-top: 5%;
    width: 30%;
  }

  .adsebuinput {
    margin-left: 57%;
    margin-top: -15%;
    width: 50%;
  }

  .adsebu-button {
    margin-top: -3.9%;
    margin-left: 19%;
    position: absolute;
    z-index: 10000;
  }

  .adsebu-reload {
    position: absolute;
    left: 24%;
    margin-top: -3.9%;
  }
  .adbuli {
    width: 80%;
  }
</style>
