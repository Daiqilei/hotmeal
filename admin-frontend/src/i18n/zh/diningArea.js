/****
 * @file            diningArea.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default {
  title: '餐区管理',
  table: {
    areaId: '餐区编号',
    areaName: '餐区名称',
    maxCapacity: '最大容纳人数',
    currentStatus: '当前状态',
    operations: '操作',
  },
  form: {
    areaName: '餐区名称',
    maxCapacity: '最大容纳人数',
    placeholder: {
      areaName: '请输入餐区名称',
      maxCapacity: '请输入最大容纳人数',
    },
  },
  status: {
    available: '可用',
    full: '已满',
    closed: '已关闭',
  },
  message: {
    addSuccess: '餐区添加成功！',
    updateSuccess: '餐区信息已更新！',
    deleteConfirm: '确定要删除该餐区吗？',
  },
}
