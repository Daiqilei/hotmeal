<template>
  <div id="main" class="chart-container"></div>
  <div id="main2" class="chart-container"></div>
  <div id="ring-chart" class="chart-container"></div>
</template>

<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { useI18n } from 'vue-i18n'
  import * as echarts from 'echarts'
  import { getMonthlyRevenue, getCategoryVolume, getCategoryCount } from '@/api/chart'

  const { t } = useI18n()

  const charts = ref(null)
  const barr = ref(null)
  const ringChartInstance = ref(null)

  const opinionData = reactive({
    title: { text: t('chart.monthlyDishSalesTrend') },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: { backgroundColor: '#6a7985' },
      },
    },
    legend: { data: [t('chart.dailyOrderVolume')] },
    toolbox: {
      feature: { restore: {}, saveAsImage: {} },
    },
    grid: { left: '0%', right: '0%', bottom: '2%', containLabel: true },
    xAxis: [
      {
        type: 'category',
        boundaryGap: false,
        data: Array.from({ length: 30 }, (_, i) => i + 1),
      },
    ],
    yAxis: [
      {
        type: 'value',
        axisLabel: { formatter: '{value} 个' },
      },
    ],
    series: [
      {
        name: '近一月每日总量',
        type: 'line',
        stack: 'Total',
        label: { show: true, position: 'top' },
        markPoint: {
          data: [
            { type: 'max', name: 'Max' },
            { type: 'min', name: 'Min' },
          ],
        },
        markLine: { data: [{ type: 'average', name: 'Avg' }] },
        areaStyle: {},
        emphasis: { focus: 'series' },
        data: [],
      },
    ],
  })

  const categoryData = reactive({
    title: { text: t('chart.monthlyCategorySales') },
    grid: { left: '0%', right: '0%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['浙江菜', '淮扬菜', '鲁菜', '粤菜', '川菜', '闽菜', '安徽菜', '湘菜'],
    },
    yAxis: {
      type: 'value',
      axisLabel: { formatter: '{value} 个' },
    },
    series: [
      {
        data: [120, 200, 150, 80, 70, 110, 130],
        type: 'bar',
        showBackground: true,
        backgroundStyle: { color: 'rgba(180, 180, 180, 0.2)' },
      },
    ],
  })

  const ringChartData = reactive({
    title: { text: t('chart.categoryShare'), left: 'center' },
    tooltip: { trigger: 'item' },
    legend: { top: '5%', left: 'center' },
    series: [
      {
        name: t('chart.outputShare'),
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: { show: false, position: 'center' },
        emphasis: {
          label: { show: true, fontSize: 40, fontWeight: 'bold' },
        },
        labelLine: { show: false },
        data: [
          { value: 1048, name: 'Search Engine' },
          { value: 735, name: 'Direct' },
          { value: 580, name: 'Email' },
          { value: 484, name: 'Union Ads' },
          { value: 300, name: 'Video Ads' },
        ],
      },
    ],
  })

  function drawLine(id) {
    charts.value = echarts.init(document.getElementById(id))
    getMonthlyRevenue().then((res) => {
      opinionData.series[0].data = res.data
      charts.value.setOption(opinionData)
    })
  }

  function initBar(id) {
    barr.value = echarts.init(document.getElementById(id))
    getCategoryVolume().then((res) => {
      categoryData.series[0].data = res.data
      barr.value.setOption(categoryData)
    })
  }

  function initRing() {
    ringChartInstance.value = echarts.init(document.getElementById('ring-chart'))
    getCategoryCount().then((res) => {
      ringChartData.series[0].data = res.data
      ringChartInstance.value.setOption(ringChartData)
    })
  }

  onMounted(() => {
    drawLine('main')
    initBar('main2')
    initRing()
  })
</script>
<style scoped>
  .chart-container {
    width: 100%;
    height: 300px;
    margin-bottom: 16px;
  }
</style>
