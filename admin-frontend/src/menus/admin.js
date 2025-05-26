/**
 * @file            admin.js
 * @description     Admin Sidebar Menu Configuration
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.2 - Separate User and Dish Management SubMenus
 */

// 建议：使用显式导入图标以获得更好的体验
// import { HomeFilled, User, Dish, OfficeBuilding, List, PieChart } from '@element-plus/icons-vue';

export default [
  {
    // 首页 (Top Level Item)
    label: '首页',
    // icon: HomeFilled,
    icon: 'HomeFilled', // 使用字符串或导入的组件
    path: '/admin/dashboard',
  },
  {
    // 用户管理 (Top Level SubMenu)
    label: '用户管理', // el-sub-menu 的标题
    // icon: User,
    icon: 'User',
    path: '/admin/user-management', // 父级 SubMenu 的唯一 index/path
    children: [
      {
        // 客户管理 (Child Item)
        title: '客户管理', // el-menu-item 的文本 (使用 title)
        path: '/admin/user', // 指向客户列表/管理页面 (基于你的 views/admin/user/index.vue)
      },
      {
        // 员工管理 (Child Item)
        title: '员工管理',
        path: '/admin/staff', // TODO: 确认员工管理的实际路由路径
        // 如果没有单独的员工管理页面，可能需要调整或移除此项
      },
    ],
  },
  {
    // 菜品管理 (Top Level SubMenu)
    label: '菜品管理', // el-sub-menu 的标题
    // icon: Dish,
    icon: 'Dish',
    path: '/admin/dish-management', // 父级 SubMenu 的唯一 index/path
    children: [
      {
        // 菜品列表/明细管理 (Child Item)
        title: '菜品列表', // el-menu-item 的文本 (使用 title)
        // 你原来写的是 '全部菜品', path: '/admin/dish'
        path: '/admin/dish', // 指向菜品列表页面 (基于你的 views/admin/dish/DishList.vue)
      },
      {
        // 分类管理 (Child Item)
        title: '分类管理', // el-menu-item 的文本 (使用 title)
        path: '/admin/category', // 指向分类管理页面 (基于你的 views/admin/category/CategoryPanel.vue)
      },
    ],
  },
  {
    // 餐区管理 (Top Level Item)
    label: '餐区管理',
    // icon: OfficeBuilding,
    icon: 'OfficeBuilding', // 替换 'diningArea'
    path: '/admin/dining-area', // 路径更正为匹配 views 文件夹
  },
  {
    // 订单管理 (Top Level Item)
    label: '订单管理',
    // icon: List,
    icon: 'List',
    path: '/admin/orders',
  },
  {
    // 数据看板 (Top Level Item)
    label: '数据看板',
    // icon: PieChart,
    icon: 'Chart',
    path: '/admin/charts',
  },
]
