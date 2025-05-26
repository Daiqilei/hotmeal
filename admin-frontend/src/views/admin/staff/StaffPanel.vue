<template>
  <ContentPanel :fetchData="fetchStaffList" @update:selected="handleSelected">
    <!-- 搜索区域 -->
    <template #search-form="{ form, onSearch, onReset }">
      <el-form-item label="账号">
        <el-input v-model="form.keyword" placeholder="请输入账号关键字" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">搜索</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </template>

    <!-- 操作按钮 -->
    <template #toolbar="{ selected }">
      <el-button type="success" @click="handleAdd">新增员工</el-button>
      <el-button type="danger" :disabled="!selected.length" @click="handleDelete(selected)"
        >删除</el-button
      >
    </template>

    <!-- 表格列 -->
    <template #columns>
      <el-table-column prop="account" label="账号" />
      <el-table-column prop="username" label="姓名" />
      <el-table-column prop="role" label="角色" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="created_at" label="入职时间" />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </template>
  </ContentPanel>

  <el-dialog v-model="editDialogVisible" title="编辑员工" width="400px">
    <el-form :model="editStaff">
      <el-form-item label="账号"><el-input v-model="editStaff.account" disabled /></el-form-item>
      <el-form-item label="姓名"><el-input v-model="editStaff.username" /></el-form-item>
      <el-form-item label="角色">
        <el-select v-model="editStaff.role">
          <el-option label="管理员" value="ADMIN" />
          <el-option label="员工" value="STAFF" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="editDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitEdit">提交</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="addDialogVisible" title="新增员工" width="400px">
    <el-form :model="newStaff">
      <el-form-item label="账号"><el-input v-model="newStaff.account" /></el-form-item>
      <el-form-item label="姓名"><el-input v-model="newStaff.username" /></el-form-item>
      <el-form-item label="角色">
        <el-select v-model="newStaff.role">
          <el-option label="管理员" value="ADMIN" />
          <el-option label="员工" value="STAFF" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="addDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitAdd">提交</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { reactive, ref } from 'vue'
  import ContentPanel from '@/components/common/ContentPanel.vue'
  import { getStaffList, deleteStaff, updateStaff, addStaff } from '@/api/staff'

  const tableData = ref([])

  // 确认组件加载
  console.log('[StaffPanel] mounted')

  // 获取员工列表
  const fetchStaffList = async (query) => {
    console.log('[StaffPanel] fetchStaffList query:', query)
    const res = await getStaffList(query)
    console.log('[StaffPanel] getStaffList response:', res)
    // 兼容 mocks 的 data 数组 和 后端返回的 list 字段
    const dataArr = res.data.data || res.data.list || []
    return {
      list: dataArr,
      total: res.data.total ?? dataArr.length,
    }
  }

  // 新增员工弹窗相关
  const addDialogVisible = ref(false)
  const newStaff = reactive({
    account: '',
    username: '',
    role: 'STAFF',
  })

  // 新增按钮
  const handleAdd = () => {
    newStaff.account = ''
    newStaff.username = ''
    newStaff.role = 'STAFF'
    addDialogVisible.value = true
  }

  const submitAdd = async () => {
    try {
      await addStaff({ ...newStaff })
      ElMessage.success('新增 成功')
      addDialogVisible.value = false
      // 刷新列表数据
      if (typeof fetchData === 'function') {
        await fetchData()
      }
    } catch (err) {
      console.error('[StaffPanel] 新增失败', err)
      ElMessage.error('新增失败')
    }
  }

  // 删除操作
  const handleDelete = (selected) => {
    console.log('[StaffPanel] handleDelete selected:', selected)
    ElMessageBox.confirm('确定删除选中的员工？', '警告', { type: 'warning' }).then(async () => {
      for (const staff of selected) {
        await deleteStaff(staff.account)
      }
      ElMessage.success('删除成功')
      // 删除后刷新列表数据
      if (typeof fetchData === 'function') {
        await fetchData()
      }
    })
  }

  // 选中项变化
  const handleSelected = (val) => {
    console.log('[StaffPanel] selected:', val)
  }

  const editStaff = reactive({
    staff_id: null,
    account: '',
    username: '',
    role: '',
  })
  const editDialogVisible = ref(false)

  const handleEdit = (row) => {
    editStaff.staff_id = row.staff_id || row.user_id
    editStaff.account = row.account
    editStaff.username = row.username
    editStaff.role = row.role
    editDialogVisible.value = true
  }

  const submitEdit = async () => {
    if (!editStaff.staff_id) {
      ElMessage.error('无法识别员工ID')
      return
    }
    try {
      const updateData = {
        account: editStaff.account,
        username: editStaff.username,
        role: editStaff.role,
      }
      await updateStaff(editStaff.staff_id, updateData)
      ElMessage.success('更新成功')
      editDialogVisible.value = false
      if (typeof fetchData === 'function') {
        await fetchData()
      }
    } catch (err) {
      console.error('[StaffPanel] 更新失败', err)
      ElMessage.error('更新失败')
    }
  }
</script>

<style scoped>
  /* 可根据需要添加样式 */
</style>
