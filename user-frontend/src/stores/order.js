/**
 * @file         src/stores/order.js
 * @author       taichilei
 * @date         2025-04-29
 * @description  This file defines the store of order.
 */
import {defineStore} from 'pinia'
import {ref} from 'vue'

export const useOrderStore = defineStore('order', () => {
    const currentOrder = ref(null)

    const draftOrder = ref({
        dish_list: [],
        area_id: null
    })

    const draftDisplayList = ref([])

    function setOrder(order) {
        currentOrder.value = order
    }

    function clearOrder() {
        currentOrder.value = null
    }

    function setDraftOrderData(dishList, areaId = null) {
        draftOrder.value = {
            dish_list: dishList,
            area_id: areaId
        }
    }

    function setDraftDisplayList(displayData) {
        draftDisplayList.value = displayData
    }

    function clearDraftOrder() {
        draftOrder.value = {
            dish_list: [],
            area_id: null
        }
        draftDisplayList.value = []
    }

    return {
        currentOrder,
        setOrder,
        clearOrder,
        draftOrder,
        draftDisplayList,
        setDraftOrderData,
        setDraftDisplayList,
        clearDraftOrder
    }
}, {
    persist: true
    // persist: {
    //     paths: ['draftOrder', 'draftDisplayList']
    // }
})