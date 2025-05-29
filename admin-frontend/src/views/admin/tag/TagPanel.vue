<!--
 * @file         src/views/admin/tag/TagPanel.vue
 * @author       taichilei
 * @date         2025-05-29
 * @description  TagPanel.vue
-->

<!-- src/views/admin/tag -->

<template>
  <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑标签' : '新增标签'" width="500px">
    <el-form :model="editForm" label-width="80px">
      <el-form-item label="标签名称">
        <el-input v-model="editForm.tagName" placeholder="请输入标签名称" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="isEdit ? handleUpdate() : handleAdd()">确定</el-button>
    </template>
  </el-dialog>

  <ContentPanel
    ref="contentPanelRef"
    :fetchData="fetchTagList"
    @update:selected="handleSelected"
  >
    <template #search-form="{ form, onSearch, onReset }">
      <el-form-item label="标签名称">
        <el-input v-model="form.keyword" clearable placeholder="请输入标签名称" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">搜索</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </template>

    <template #toolbar="{ selected }">
      <el-button type="success" @click="dialogVisible = true">新增标签</el-button>
      <el-button :disabled="!selected.length" type="danger" @click="handleDelete(selected)">删除</el-button>
    </template>

    <template #columns>
      <el-table-column label="ID" prop="tag_id" width="80" />
      <el-table-column label="标签名称" prop="name" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </template>
  </ContentPanel>
</template>

<script setup>
  import { reactive, ref } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import ContentPanel from '@/components/common/ContentPanel.vue'
  import { createTag, deleteTagById, getTagList, updateTag } from '@/api/tag'

  const dialogVisible = ref(false)
  const isEdit = ref(false)

  const editForm = reactive({
    tagId: null,
    tagName: ''
  })

  const contentPanelRef = ref()

  const fetchTagList = async (query) => {
    console.log('[TagPanel] fetchTagList called with query:', query)
    const res = await getTagList(query)
    console.log('[TagPanel] getTagList response:', res)

    const raw = res.data
    const dataArr = Array.isArray(raw) ? raw : (raw.list || raw.data || [])
    dataArr.sort((a, b) => a.id - b.id)
    return {
      list: dataArr,
      total: raw.total ?? dataArr.length
    }
  }

  const reloadTagList = async () => {
    await contentPanelRef.value?.fetchData()
  }

  const handleEdit = (row) => {
    isEdit.value = true
    dialogVisible.value = true
    editForm.tagId = row.tag_id
    editForm.tagName = row.name
  }

  const handleAdd = async () => {
    if (!editForm.tagName?.trim()) {
      ElMessage.warning('标签名称不能为空')
      return
    }
    try {
      await createTag({ name: editForm.tagName.trim() })
      ElMessage.success('新增标签成功')
      dialogVisible.value = false
      await reloadTagList()
    } catch (err) {
      ElMessage.error(err.message || '新增失败')
    }
  }

  const handleUpdate = async () => {
    if (!editForm.tagName?.trim()) {
      ElMessage.warning('标签名称不能为空')
      return
    }
    try {
      await updateTag(editForm.tagId, { name: editForm.tagName.trim() })
      ElMessage.success('更新成功')
      dialogVisible.value = false
      await reloadTagList()
    } catch (err) {
      ElMessage.error(err.message || '更新失败')
    } finally {
      isEdit.value = false
    }
  }

  /**
   * @param {{ tag_id: number }[]} selected
   */
  const handleDelete = (selected) => {
    ElMessageBox.confirm('确定删除选中的标签？', '警告', { type: 'warning' }).then(async () => {
      for (const item of selected) {
        // item.tag_id: number
        await deleteTagById(item.tag_id)
      }
      ElMessage.success('删除成功')
      await reloadTagList()
    })
  }

  const handleSelected = (val) => {
    console.log('[TagPanel] selected:', val)
  }
</script>

<style scoped>
</style>
onMounted(() => {
contentPanelRef.value?.fetchData()
})

defineExpose({ fetchData: fetchTagList })