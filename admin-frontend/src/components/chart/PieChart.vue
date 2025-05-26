<template>
  <!-- 图表容器 -->
  <div class="pie-card" ref="chartRef" :style="{ width: '100%', height: height + 'px' }"></div>
</template>

<script setup>
  import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
  import * as echarts from 'echarts'

  // props:
  // - options: 完整的 ECharts 配置对象，用于自定义图表标题、图例、系列等设置
  // - height:  图表容器高度（单位 px），默认 300
  const props = defineProps({
    options: {
      type: Object,
      default: () => ({}),
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

  // 监听配置变更，更新图表
  watch(
    () => props.options,
    (newOpt) => {
      if (chartInstance) {
        chartInstance.setOption(newOpt, true)
      }
    },
    { deep: true },
  )

  // 窗口尺寸变化时自适应
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
  .pie-card {
    background-color: #81d8d0;
    border-radius: 16px;
    padding: 16px;
  }
</style>
