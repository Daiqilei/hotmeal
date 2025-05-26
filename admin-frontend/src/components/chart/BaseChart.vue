<template>
  <!-- iPhone 风格浅色卡片 -->
  <div class="chart-card">
    <!-- 通用图表容器 -->
    <div ref="chartRef" :style="{ width: '100%', height: height + 'px' }"></div>
  </div>
</template>

<script setup>
  import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
  import * as echarts from 'echarts'

  // props:
  // - options: 完整的 ECharts 配置对象，用于初始化和更新图表
  // - height:  图表容器高度（单位 px），默认 300
  const props = defineProps({
    options: {
      type: Object,
      required: true,
    },
    height: {
      type: Number,
      default: 300,
    },
  })

  const chartRef = ref(null)
  let chartInstance = null

  // 初始化图表
  onMounted(() => {
    if (chartRef.value) {
      chartInstance = echarts.init(chartRef.value)
      chartInstance.setOption(props.options)
      window.addEventListener('resize', resizeChart)
    }
  })

  // 监听配置变更
  watch(
    () => props.options,
    (newOptions) => {
      if (chartInstance) {
        chartInstance.setOption(newOptions, true)
      }
    },
    { deep: true },
  )

  // 自适应窗口变化
  function resizeChart() {
    if (chartInstance) {
      chartInstance.resize()
    }
  }

  // 销毁时清理
  onBeforeUnmount(() => {
    window.removeEventListener('resize', resizeChart)
    if (chartInstance) {
      chartInstance.dispose()
      chartInstance = null
    }
  })
</script>

<style scoped>
  .chart-card {
    background-color: #f2f2f7; /* iOS 浅色背景 */
    border-radius: 16px; /* iPhone 样式圆角 */
    padding: 16px;
  }
  /* 确保容器占满父级宽度 */
  div[ref='chartRef'] {
    width: 100%;
  }
</style>
