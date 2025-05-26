/**
 * @file            dish.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default {
  title: 'Dish Management',
  table: {
    dishId: 'Dish ID',
    dishName: 'Dish Name',
    category: 'Category',
    price: 'Price',
    stock: 'Stock',
    imageUrl: 'Image',
    status: 'Status',
    operations: 'Operations',
  },
  form: {
    dishName: 'Dish Name',
    category: 'Category',
    price: 'Price',
    stock: 'Stock',
    imageUrl: 'Image URL',
    placeholder: {
      dishName: 'Enter dish name',
      price: 'Enter price',
      stock: 'Enter available stock',
      imageUrl: 'Paste image URL or upload',
    },
  },
  status: {
    available: 'Available',
    unavailable: 'Unavailable',
    soldOut: 'Sold Out',
  },
  message: {
    addSuccess: 'Dish added successfully!',
    updateSuccess: 'Dish updated!',
    deleteConfirm: 'Are you sure to delete this dish?',
  },
}
