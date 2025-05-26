/**
 * @file            user.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */
export default {
  title: 'User Management',
  table: {
    userId: 'User ID',
    username: 'Username',
    account: 'Account',
    role: 'Role',
    email: 'Email',
    phone: 'Phone',
    createdAt: 'Created At',
    updatedAt: 'Updated At',
    operations: 'Operations',
  },
  form: {
    username: 'Username',
    account: 'Account',
    password: 'Password',
    email: 'Email',
    phone: 'Phone',
    role: 'Role',
    placeholder: {
      username: 'Enter username',
      account: 'Enter account',
      password: 'Enter password',
      email: 'Enter email',
      phone: 'Enter phone number',
    },
  },
  role: {
    admin: 'Administrator',
    staff: 'Staff',
    user: 'User',
  },
  message: {
    addSuccess: 'User added successfully!',
    updateSuccess: 'User updated!',
    deleteConfirm: 'Are you sure to delete this user?',
  },
}
