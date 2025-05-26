<template>
  <div class="app-container">
    <router-view class="view-container"></router-view>
  </div>
</template>

<script setup>
  import { onMounted } from 'vue'

  onMounted(() => {
    console.log('App mounted')
  })
</script>

<style>
  @import './assets/styles/global.css';

  .app-container {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    margin: 0;
    background-color: #fff;
  }

  /* 让 router-view 撑满整个页面 */
  .view-container {
    flex: 1;
    width: 100%;

    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-height: 0;
  }

  @media screen and (max-width: 480px) {
  }
</style>
