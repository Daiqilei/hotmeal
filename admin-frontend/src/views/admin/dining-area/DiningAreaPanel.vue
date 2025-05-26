<template>
  <ContentPanel
    ref="panelRef"
    :fetchData="fetchAreaList"
    @update:selected="handleSelected"
    @row:edit="handleEdit"
  >
    <!-- 搜索区域 -->
    <template #search-form="{ form, onSearch, onReset }">
      <el-form-item label="餐区名称">
        <el-input v-model="form.keyword" clearable placeholder="请输入餐区名称" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">搜索</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </template>

    <!-- 工具栏 -->
    <template #toolbar="{ selected }">
      <el-button type="success" @click="handleAdd">新增餐区</el-button>
      <el-button :disabled="!selected.length" type="danger" @click="handleDelete(selected)"
        >删除
      </el-button>
    </template>

    <!-- 表格列 -->
    <template #columns>
      <el-table-column label="餐区号" prop="area_id" width="80" />
      <el-table-column label="名称" prop="area_name" width="80" />
      <el-table-column label="最大容量" prop="max_capacity" />
      <el-table-column label="状态" prop="state" />
      <el-table-column label="绑定用户" prop="userId" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button type="warning" size="small" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </template>
  </ContentPanel>

  <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑餐区' : '新增餐区'" width="400px">
    <el-form :model="form" label-width="80px">
      <el-form-item label="区域名称">
        <el-input v-model="form.area_name" placeholder="请输入区域名称" />
      </el-form-item>
      <el-form-item label="区域类型">
        <el-select v-model="form.area_type" placeholder="请选择区域类型">
          <el-option label="包间" value="PRIVATE" />
          <el-option label="桌台" value="TABLE" />
          <el-option label="吧台" value="BAR" />
        </el-select>
      </el-form-item>
      <el-form-item label="最大容量">
        <el-input v-model="form.max_capacity" placeholder="请输入最大容量" type="number" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitForm">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
  import { reactive, ref } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import ContentPanel from '@/components/common/ContentPanel.vue'
  import {
    addDiningArea,
    deleteDiningArea,
    getDiningAreaList,
    updateDiningArea,
  } from '@/api/diningArea'

  const panelRef = ref(null)

  // 开始加载数据
  const fetchAreaList = async (query) => {
    const res = await getDiningAreaList(query)
    console.log('🎯 DiningAreaPanel fetch response:', res)
    const rawData = res.data
    const payload = Array.isArray(rawData)
      ? rawData
      : (rawData?.data ?? // 内层 data
        rawData?.list ?? // 或 list
        rawData) // 或整个 data 本身
    const list = Array.isArray(payload) ? payload : Array.isArray(payload.list) ? payload.list : []
    const total = typeof payload.total === 'number' ? payload.total : list.length
    return { list, total }
  }

  const dialogVisible = ref(false)

  // 表单数据
  const form = reactive({
    area_id: null,
    area_name: '',
    area_type: '',
    max_capacity: null,
  })

  const isEdit = ref(false)

  // 提交表单,新增
  const submitForm = async () => {
    if (!form.max_capacity || form.max_capacity <= 0) {
      ElMessage.error('请输入有效的最大容量')
      return
    }
    try {
      if (isEdit.value) {
        await updateDiningArea({
          area_id: form.area_id,
          area_name: form.area_name,
          area_type: form.area_type,
          max_capacity: Number(form.max_capacity),
        })
        ElMessage.success('更新成功')
      } else {
        const payload = {
          area_name: form.area_name,
          area_type: form.area_type,
          max_capacity: Number(form.max_capacity),
        }
        console.log('🎯 Add DiningArea Payload:', payload)

        const res = await addDiningArea(payload)
        console.log('🎯 DiningAreaPanel add response:', res)
        ElMessage.success('新增成功')
      }
      dialogVisible.value = false

      panelRef.value?.fetchData()
    } catch (err) {
      console.error('❌ 提交失败:', err?.response?.data || err)
      ElMessage.error(isEdit.value ? '更新失败' : '新增失败')
    }
  }

  // 新增
  const handleAdd = () => {
    isEdit.value = false
    form.area_id = null
    form.area_name = ''
    form.area_type = ''
    form.max_capacity = null
    dialogVisible.value = true
  }

  // 编辑
  const handleEdit = (row) => {
    form.area_id = row.area_id
    form.area_name = row.area_name
    form.area_type = row.area_type
    form.max_capacity = row.max_capacity
    isEdit.value = true
    dialogVisible.value = true
  }

  // 删除
  const handleDelete = (selected) => {
    ElMessageBox.confirm('确定删除选中的餐区？', '警告', { type: 'warning' }).then(async () => {
      for (const area of selected) {
        await deleteDiningArea(area.area_id)
      }
      ElMessage.success('删除成功')
    })
  }

  // 选中
  const handleSelected = (val) => {
    console.log('选中的餐区:', val)
  }
</script>

<style scoped></style>
