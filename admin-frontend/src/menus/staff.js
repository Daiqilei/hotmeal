/**
 * @file            staff.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */
export default [
  {
    index: '1',
    label: '员工首页',
    icon: 'HomeFilled',
    path: '/staff/dashboard',
  },
  {
    index: '2',
    label: '上架管理',
    icon: 'Dish',
    children: [
      { index: '2-1', label: '新增菜品', path: '/staff/dish/add' },
      { index: '2-2', label: '菜品列表', path: '/staff/dish' },
    ],
  },
  {
    index: '3',
    label: '订单处理',
    icon: 'ShoppingCart',
    path: '/staff/order',
  },
  {
    index: '4',
    label: '个人中心',
    icon: 'UserFilled',
    path: '/staff/profile',
  },
]
