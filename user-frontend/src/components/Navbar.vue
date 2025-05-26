<!--
 * @file         src/components/Navbar.vue
 * @author       taichilei
 * @date         2025-04-29
 * @description  通用导航栏组件，实现标题显示、返回按钮（可选）、右侧 slot、自定义样式
-->

<!-- src/components -->

<template>
  <u-navbar
      :custom-style="customStyle"
      :left-icon="showBack ? 'arrow-left' : ''"
      :title="title"
      @leftClick="handleBack"
  >
    <template #right>
      <slot name="right"/>
    </template>
  </u-navbar>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  showBack: {
    type: Boolean,
    default: true
  },
  customStyle: {
    type: String,
    default: ''
  }
})

const handleBack = () => {
  uni.navigateBack()
}
</script>

<style scoped>
/* 可根据需要补充样式 */
</style>