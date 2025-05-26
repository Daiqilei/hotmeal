/**
 * @file            dish.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default {
  title: '菜品管理',
  table: {
    dishId: '菜品编号',
    dishName: '菜品名称',
    category: '分类',
    price: '价格',
    stock: '库存',
    imageUrl: '图片',
    status: '状态',
    operations: '操作',
  },
  form: {
    dishName: '菜品名称',
    category: '分类',
    price: '价格',
    stock: '库存',
    imageUrl: '图片链接',
    placeholder: {
      dishName: '请输入菜品名称',
      price: '请输入价格',
      stock: '请输入库存数量',
      imageUrl: '粘贴图片链接或上传图片',
    },
  },
  status: {
    available: '上架中',
    unavailable: '已下架',
    soldOut: '已售罄',
  },
  message: {
    addSuccess: '菜品添加成功！',
    updateSuccess: '菜品更新成功！',
    deleteConfirm: '确定要删除该菜品吗？',
  },
}
