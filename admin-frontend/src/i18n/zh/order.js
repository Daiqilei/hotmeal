/**
 * @file            order.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default {
  title: '订单管理',
  table: {
    orderId: '订单编号',
    user: '下单用户',
    area: '就餐区域',
    price: '订单总价',
    state: '订单状态',
    paymentMethod: '支付方式',
    imageUrl: '支付凭证',
    createdAt: '创建时间',
    updatedAt: '更新时间',
    operations: '操作',
  },
  form: {
    state: '订单状态',
    paymentMethod: '支付方式',
    imageUrl: '支付图片链接',
    placeholder: {
      imageUrl: '粘贴图片链接或上传',
    },
  },
  status: {
    pending: '待支付',
    paid: '已支付',
    canceled: '已取消',
    completed: '已完成',
  },
  message: {
    updateSuccess: '订单更新成功！',
    cancelConfirm: '确定要取消该订单吗？',
    deleteConfirm: '确定要删除该订单吗？',
  },
}
