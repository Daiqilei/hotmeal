/**
 * @file            order.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default {
  title: 'Order Management',
  table: {
    orderId: 'Order ID',
    user: 'User',
    area: 'Dining Area',
    price: 'Total Price',
    state: 'Order Status',
    paymentMethod: 'Payment Method',
    imageUrl: 'Payment Proof',
    createdAt: 'Created Time',
    updatedAt: 'Updated Time',
    operations: 'Operations',
  },
  form: {
    state: 'Order Status',
    paymentMethod: 'Payment Method',
    imageUrl: 'Payment Image URL',
    placeholder: {
      imageUrl: 'Paste image URL or upload',
    },
  },
  status: {
    pending: 'Pending',
    paid: 'Paid',
    canceled: 'Canceled',
    completed: 'Completed',
  },
  message: {
    updateSuccess: 'Order updated successfully!',
    cancelConfirm: 'Are you sure you want to cancel this order?',
    deleteConfirm: 'Are you sure to delete this order?',
  },
}
