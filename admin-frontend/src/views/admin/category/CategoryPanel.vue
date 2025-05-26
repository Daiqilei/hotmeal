<template>
  <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑分类' : '新增分类'" width="500px">
    <el-form :model="editForm" label-width="80px">
      <el-form-item label="分类名称">
        <el-input v-model="editForm.categoryName" placeholder="请输入分类名称" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="editForm.description" placeholder="请输入描述" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="isEdit ? handleUpdate() : handleAdd()">确定</el-button>
    </template>
  </el-dialog>
  <ContentPanel
    ref="contentPanelRef"
    :fetchData="fetchCategoryList"
    @update:selected="handleSelected"
  >
    <!-- 搜索区域 -->
    <template #search-form="{ form, onSearch, onReset }">
      <el-form-item label="分类名称">
        <el-input v-model="form.keyword" clearable placeholder="请输入分类名称" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">搜索</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </template>

    <!-- 工具栏 -->
    <template #toolbar="{ selected }">
      <el-button type="success" @click="dialogVisible = true">新增分类</el-button>
      <el-button :disabled="!selected.length" type="danger" @click="handleDelete(selected)"
        >删除
      </el-button>
    </template>

    <!-- 表格列 -->
    <template #columns>
      <el-table-column label="ID" prop="category_id" width="80" />
      <el-table-column label="分类名称" prop="name" />
      <el-table-column label="描述" prop="description" />
      <el-table-column label="创建时间" prop="created_at" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </template>
  </ContentPanel>
</template>

<script setup>
  import { reactive, ref } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import ContentPanel from '@/components/common/ContentPanel.vue'
  import {
    createCategory,
    deleteCategoryById,
    getCategoryList,
    updateCategory,
  } from '@/api/category'

  // 确认组件加载
  console.log('[CategoryPanel] mounted')

  const dialogVisible = ref(false)

  const isEdit = ref(false)
  const editForm = reactive({
    categoryId: null,
    categoryName: '',
    description: '',
  })

  const contentPanelRef = ref()

  const fetchCategoryList = async (query) => {
    console.log('[CategoryPanel] fetchCategoryList query:', query)
    console.log('[CategoryPanel] calling getCategoryList')
    const res = await getCategoryList(query)
    console.log('[CategoryPanel] getCategoryList response:', res)

    // 假设后端返回 { data: [...], total: N }
    const dataArr = res.data.data || res.data.list || []
    console.log('[DEBUG] dataArr 实际数据结构:', dataArr)
    return {
      list: dataArr,

      total: res.data.total ?? dataArr.length,
    }
  }

  const reloadCategoryList = () => {
    contentPanelRef.value?.fetchData()
  }

  const handleEdit = (row) => {
    isEdit.value = true
    dialogVisible.value = true
    editForm.categoryId = row.category_id
    editForm.categoryName = row.name
    editForm.description = row.description
  }

  const handleAdd = async () => {
    if (!editForm.categoryName?.trim()) {
      ElMessage.warning('分类名称不能为空')
      return
    }
    const newCategory = {
      name: editForm.categoryName.trim(),
      description: editForm.description?.trim() || '',
      img_url: '', // 临时规避后端模型要求
      // 如果后期需要设置父分类再加，当前不传
      // parent_category_id: null,
    }
    // [DEBUG] log before try
    console.log('[DEBUG] 即将创建分类，提交数据：', JSON.stringify(newCategory, null, 2))
    try {
      const res = await createCategory(newCategory)
      console.log('[CategoryPanel] createCategory response:', res)
      dialogVisible.value = false
      ElMessage.success('新增分类成功')
      await reloadCategoryList()
    } catch (err) {
      console.error('[CategoryPanel] createCategory error:', err)
      if (err.config) {
        console.log('[DEBUG] 请求 headers:', err.config.headers)
        console.log('[DEBUG] 请求体 data:', err.config.data)
      }
      if (err.response?.status === 400) {
        ElMessage.error('请求参数有误，请检查表单填写')
      } else {
        ElMessage.error(err.message || '新增失败')
      }
    }
  }

  const handleUpdate = async () => {
    if (!editForm.categoryName?.trim()) {
      ElMessage.warning('分类名称不能为空')
      return
    }
    try {
      const payload = {
        name: editForm.categoryName.trim(),
        description: editForm.description?.trim() || '',
      }
      const res = await updateCategory(editForm.categoryId, payload)
      console.log('[CategoryPanel] updateCategory response:', res)
      dialogVisible.value = false
      ElMessage.success('更新成功')
      await reloadCategoryList()
    } catch (err) {
      console.error('[CategoryPanel] updateCategory error:', err)
      ElMessage.error(err.message || '更新失败')
    } finally {
      isEdit.value = false
    }
  }

  const handleDelete = (selected) => {
    console.log('[CategoryPanel] handleDelete selected:', selected)
    ElMessageBox.confirm('确定删除选中的分类？', '警告', { type: 'warning' }).then(async () => {
      for (const item of selected) {
        await deleteCategoryById(item.categoryId)
      }
      ElMessage.success('删除成功')
    })
  }

  const handleSelected = (val) => {
    console.log('[CategoryPanel] selected:', val)
  }
</script>

<style scoped>
  /* 根据需要添加样式 */
</style>
