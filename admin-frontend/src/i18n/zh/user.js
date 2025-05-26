/**
 * @file            user.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */
export default {
  title: '用户管理',
  table: {
    userId: '用户编号',
    username: '用户名',
    account: '账号',
    role: '角色',
    email: '邮箱',
    phone: '电话',
    createdAt: '创建时间',
    updatedAt: '更新时间',
    operations: '操作',
  },
  form: {
    username: '用户名',
    account: '账号',
    password: '密码',
    email: '邮箱',
    phone: '电话',
    role: '角色',
    placeholder: {
      username: '请输入用户名',
      account: '请输入账号',
      password: '请输入密码',
      email: '请输入邮箱地址',
      phone: '请输入电话号码',
    },
  },
  role: {
    admin: '管理员',
    staff: '员工',
    user: '用户',
  },
  message: {
    addSuccess: '用户添加成功！',
    updateSuccess: '用户更新成功！',
    deleteConfirm: '确定要删除该用户吗？',
  },
}
