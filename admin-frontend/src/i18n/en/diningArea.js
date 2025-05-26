/**
 * @file            diningArea.js
 * @description
 * @author          taichilei
 * @date            2025-04-21
 * @version         1.0.0
 */

export default {
  title: 'Dining Area Management',
  table: {
    areaId: 'Area ID',
    areaName: 'Area Name',
    maxCapacity: 'Max Capacity',
    currentStatus: 'Current Status',
    operations: 'Operations',
  },
  form: {
    areaName: 'Area Name',
    maxCapacity: 'Max Capacity',
    placeholder: {
      areaName: 'Enter dining area name',
      maxCapacity: 'Enter max capacity',
    },
  },
  status: {
    available: 'Available',
    full: 'Full',
    closed: 'Closed',
  },
  message: {
    addSuccess: 'Dining area added successfully!',
    updateSuccess: 'Dining area updated!',
    deleteConfirm: 'Are you sure to delete this dining area?',
  },
}
