<template>
  <ContentPanel :fetchData="fetchUserList" @update:selected="handleSelected">
    <!-- 搜索表单插槽 -->
    <template #search-form="{ form, onSearch, onReset }">
      <el-form-item label="账号">
        <el-input v-model="form.keyword" clearable placeholder="请输入账号关键字" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">搜索</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </template>

    <!-- 工具栏插槽 -->
    <template #toolbar="{ selected }">
      <el-button type="success" @click="handleAdd">新增用户</el-button>
      <el-button :disabled="!selected.length" type="danger" @click="handleDelete(selected)"
        >删除
      </el-button>
    </template>

    <!-- 表格列插槽 -->
    <template #columns>
      <el-table-column label="账号" prop="account" />
      <el-table-column label="昵称" prop="username" />
      <el-table-column label="角色" prop="role" />
      <el-table-column label="状态" prop="status" />
      <el-table-column label="创建时间" prop="created_at" />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </template>
  </ContentPanel>

  <el-dialog v-model="dialogVisible" title="新增用户" width="400px">
    <el-form :model="newUser" label-width="80px">
      <el-form-item label="账号">
        <el-input v-model="newUser.account" />
      </el-form-item>
      <el-form-item label="昵称">
        <el-input v-model="newUser.username" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitAdd">提交</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="editDialogVisible" title="编辑用户" width="400px">
    <el-form :model="editUser" label-width="80px">
      <el-form-item label="账号">
        <el-input v-model="editUser.account" />
      </el-form-item>
      <el-form-item label="昵称">
        <el-input v-model="editUser.username" />
      </el-form-item>
      <el-form-item label="角色">
        <el-select v-model="editUser.role" placeholder="请选择角色">
          <el-option label="管理员" value="ADMIN" />
          <el-option label="员工" value="STAFF" />
          <el-option label="用户" value="USER" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="editDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitEdit">提交</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
  import { ElMessage, ElMessageBox } from 'element-plus'
  import ContentPanel from '@/components/common/ContentPanel.vue'
  import { addUser, deleteUser, getUserList, updateUser } from '@/api/user'
  import { reactive, ref } from 'vue'

  console.log('[UserPanel] mounted')

  const fetchUserList = async (query) => {
    console.log('[UserPanel] fetchUserList query:', query)
    const res = await getUserList(query)
    console.log('[UserPanel] getUserList response:', res)

    const isArray = Array.isArray(res.data)
    const list = isArray ? res.data : (res.data?.data ?? res.data?.list ?? [])

    return {
      list,
      total: res.data?.total ?? list.length,
    }
  }

  const dialogVisible = ref(false)
  const newUser = reactive({
    account: '',
    username: '',
    role: 'user',
  })

  const handleAdd = () => {
    console.log('[UserPanel] handleAdd')
    dialogVisible.value = true
  }

  const submitAdd = async () => {
    try {
      await addUser(newUser)
      ElMessage.success('添加成功')
      dialogVisible.value = false
    } catch (err) {
      ElMessage.error('添加失败')
    }
  }

  const handleDelete = (selected) => {
    console.log('[UserPanel] handleDelete selected:', selected)
    ElMessageBox.confirm('确定删除选中的用户？', '警告', { type: 'warning' }).then(async () => {
      for (const user of selected) {
        await deleteUser(user.user_id)
      }
      ElMessage.success('删除成功')
    })
  }

  const handleSelected = (val) => {
    console.log('[UserPanel] selected:', val)
  }

  const editDialogVisible = ref(false)
  const editUser = reactive({
    user_id: null,
    account: '',
    username: '',
    role: '',
  })

  const handleEdit = (row) => {
    if (!row.user_id) {
      console.error('[UserPanel] handleEdit: user_id is missing in row:', row)
      return
    }
    editUser.user_id = row.user_id
    editUser.account = row.account
    editUser.username = row.username
    editUser.role = row.role
    editDialogVisible.value = true
  }

  const submitEdit = async () => {
    if (!editUser.user_id) {
      ElMessage.error('无法识别用户ID')
      return
    }
    try {
      console.log('[UserPanel] submitEdit payload:', {
        user_id: editUser.user_id,
        account: editUser.account,
        username: editUser.username,
        role: editUser.role,
      })

      const updateData = {
        account: editUser.account,
        username: editUser.username,
        role: editUser.role,
      }
      console.log('[UserPanel] updateUser', updateData)

      await updateUser(editUser.user_id, updateData)

      ElMessage.success('更新成功')
      editDialogVisible.value = false
    } catch (err) {
      console.error('[UserPanel] 更新失败', err)
      ElMessage.error('更新失败')
    }
  }
</script>

<style scoped></style>
