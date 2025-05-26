<template>
  <ContentPanel ref="contentPanelRef" :fetchData="fetchOrderList" @update:selected="handleSelected">
    <!-- 搜索栏 -->
    <template #search-form="{ form, onSearch, onReset }">
      <el-form-item label="订单号">
        <el-input v-model="form.orderId" placeholder="请输入订单号" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">搜索</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </template>

    <!-- 工具栏 -->
    <template #toolbar="{ selected }">
      <el-button type="danger" :disabled="!selected.length" @click="handleDelete(selected)"
        >删除订单</el-button
      >
      <el-button type="primary" :disabled="selected.length !== 1" @click="handleEdit(selected[0])"
        >编辑订单</el-button
      >
    </template>

    <!-- 表格列 -->
    <template #columns>
      <el-table-column prop="order_id" label="订单号" />
      <el-table-column prop="user_name" label="用户" />
      <el-table-column prop="area_name" label="餐区" />
      <el-table-column prop="state" label="状态" />
      <el-table-column prop="price" label="金额" />
      <el-table-column prop="created_at" label="下单时间" />
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </template>
  </ContentPanel>

  <el-dialog v-model="editDialogVisible" title="编辑订单" width="500px">
    <el-form :model="currentOrder" label-width="100px">
      <el-form-item label="订单状态">
        <el-select v-model="currentOrder.state" placeholder="请选择状态">
          <el-option label="待支付" value="PENDING" />
          <el-option label="已支付" value="PAID" />
          <el-option label="已完成" value="COMPLETED" />
          <el-option label="已取消" value="CANCELED" />
        </el-select>
      </el-form-item>
      <el-form-item label="金额">
        <el-input-number v-model="currentOrder.price" :min="0" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="editDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitOrderEdit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
  import { ref } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import ContentPanel from '@/components/common/ContentPanel.vue'
  import { getOrderList, deleteOrder, updateOrder } from '@/api/order'

  const contentPanelRef = ref()

  const fetchOrderList = async (query) => {
    // 🟡 将 pageSize 映射为 per_page 以兼容后端
    const backendQuery = { ...query }
    if ('pageSize' in backendQuery) {
      backendQuery.per_page = backendQuery.pageSize
      delete backendQuery.pageSize
    }
    const res = await getOrderList(backendQuery)
    console.log('🎯 OrderPanel fetch response:', res)
    // 支持多种响应结构：res.data 直接是数组，或 res.data.data / res.data.list 包装
    const rawData = res.data
    const payload = Array.isArray(rawData) ? rawData : (rawData?.data ?? rawData?.list ?? rawData)
    const list = Array.isArray(payload) ? payload : []
    const total = typeof payload.total === 'number' ? payload.total : list.length
    return { list, total }
  }

  const reloadOrderList = () => {
    contentPanelRef.value?.fetchData()
  }

  const handleDelete = (selected) => {
    ElMessageBox.confirm('确定删除选中的订单？', '警告', { type: 'warning' }).then(async () => {
      for (const order of selected) {
        await deleteOrder(order.order_id)
      }
      ElMessage.success('删除成功')
    })
  }

  const handleSelected = (val) => {
    console.log('选中的订单：', val)
  }

  const editDialogVisible = ref(false)
  const currentOrder = ref({})

  const handleEdit = (row) => {
    currentOrder.value = { ...row }
    editDialogVisible.value = true
  }

  const submitOrderEdit = async () => {
    try {
      await updateOrder(currentOrder.value.order_id, {
        state: currentOrder.value.state,
        price: currentOrder.value.price,
      })
      ElMessage.success('订单更新成功')
      editDialogVisible.value = false
      reloadOrderList()
    } catch (error) {
      ElMessage.error('更新失败')
    }
  }
</script>

<style scoped></style>
