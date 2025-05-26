/**
 * @file         src/stores/cart.js
 * @author       taichilei
 * @date         2025-04-29
 * @description
 */
import {defineStore} from 'pinia'
import {computed, ref} from 'vue'

export const useCartStore = defineStore('cart', () => {
    const cartList = ref([])

    // 添加商品到购物车
    function addToCart(dish) {
        const existing = cartList.value.find(item => item.dishId === dish.dishId)
        if (existing) {
            existing.quantity += 1
        } else {
            cartList.value.push({
                dishId: dish.dishId,
                name: dish.name,
                imageUrl: dish.imageUrl,
                price: dish.price,
                quantity: 1
            })
        }
    }

    function increaseQuantity(dishId) {
        const item = cartList.value.find(item => item.dishId === dishId)
        if (item) {
            item.quantity += 1
        }
    }

    // 减少商品数量
    function decreaseQuantity(dishId) {
        const item = cartList.value.find(item => item.dishId === dishId)
        if (item) {
            if (item.quantity > 1) {
                item.quantity -= 1
            } else {
                removeFromCart(dishId)
            }
        }
    }

    // 删除商品
    function removeFromCart(dishId) {
        cartList.value = cartList.value.filter(item => item.dishId !== dishId)
    }

    // 清空购物车
    function clearCart() {
        cartList.value = []
    }

    // 购物车总数量
    const totalCount = computed(() => {
        return cartList.value.reduce((sum, item) => sum + item.quantity, 0)
    })

    // 购物车总价
    const totalPrice = computed(() => {
        return cartList.value.reduce((sum, item) => sum + item.quantity * item.price, 0).toFixed(2)
    })

    return {
        cartList,
        addToCart,
        increaseQuantity,
        decreaseQuantity,
        removeFromCart,
        clearCart,
        totalCount,
        totalPrice
    }
}, {
    persist: true
})