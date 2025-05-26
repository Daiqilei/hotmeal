<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import * as echarts from 'echarts'

  const chartRef = ref(null)

  const option = {
    title: { text: '收入趋势（本月）' },
    tooltip: { trigger: 'axis' },
    legend: { data: ['收入'] },
    xAxis: {
      type: 'category',
      data: ['5/1', '5/2', '5/3', '5/4', '5/5', '5/6', '5/7'],
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '收入',
        type: 'line',
        data: [1200, 1600, 900, 1400, 1800, 1300, 1700],
        smooth: true,
      },
    ],
  }

  onMounted(() => {
    const chartInstance = echarts.init(chartRef.value)
    chartInstance.setOption(option)
  })
</script>

<style scoped>
  .chart-container {
    width: 100%;
    height: 300px;
  }

  .chart {
    width: 100%;
    height: 100%;
  }
</style>
